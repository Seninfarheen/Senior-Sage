package service

import (
	"authz/config"
	"authz/storage"
	"authz/types"
	"crypto/sha256"
	"encoding/hex"
	"fmt"
	"time"

	"github.com/golang-jwt/jwt/v5"
	"go.mongodb.org/mongo-driver/mongo"
)

type AuthenticationService struct {
}

var AuthService *AuthenticationService

func init() {
	AuthService = &AuthenticationService{}
}

type CustomRegisteredClaims struct {
	jwt.RegisteredClaims
	UserId string `json:"user_id"`
}

func (as *AuthenticationService) GenerateToken(userDetails *types.UserDetails) (string, error) {
	signingKey := []byte(config.Configs.AuthSecretKey)
	encEmail, err := storage.EncryptionSvc.Encrypt(userDetails.UserEmail)
	if err != nil {
		return "", fmt.Errorf("error encrypting email: %v", err)
	}
	claims := &CustomRegisteredClaims{
		RegisteredClaims: jwt.RegisteredClaims{
			Issuer:    "sage-server",
			ExpiresAt: jwt.NewNumericDate(time.Now().Add(9999 * time.Hour)),
			IssuedAt:  jwt.NewNumericDate(time.Now()),
			NotBefore: jwt.NewNumericDate(time.Now()),
		},
		UserId: encEmail,
	}
	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
	ss, err := token.SignedString(signingKey)
	return ss, err
}

func checkIfUserExists(signupReq *types.UserSignupRequest) (bool, error) {
	encEmail, err := storage.EncryptionSvc.Encrypt(signupReq.UserEmail)
	if err != nil {
		return false, fmt.Errorf("error encrypting email: %v", err)
	}
	_, err = storage.StorageSvc.GetUserDoc(encEmail)
	if err == nil {
		return true, nil
	} else if err != mongo.ErrNoDocuments {
		return false, fmt.Errorf("error getting user id: %v", err)
	}
	return false, nil
}

func getUserDoc(signupReq *types.UserSignupRequest) (*types.UserDetails, error) {
	h := sha256.New()
	_, err := h.Write([]byte(signupReq.UserPassword))
	if err != nil {
		return nil, fmt.Errorf("error hashing password: %v", err)
	}
	passwordHash := hex.EncodeToString(h.Sum(nil))
	return &types.UserDetails{
		UserEmail:         signupReq.UserEmail,
		PasswordHash:      passwordHash,
		ReminderDetails:   &[]types.ReminderDetails{},
		RPMReadings:       &[]types.RPMReading{},
		Preferences:       &[]string{},
		ChatHistory:       &[]types.ChatSession{},
		QuestionResponses: &[]types.QuestionResponse{},
		VoiceSelection:    signupReq.VoiceSelection,
		Name:              signupReq.Name,
		QuestionCounts:    map[int]types.QuestionCounter{},
	}, nil
}

func getAclsDoc(signupReq *types.UserSignupRequest) (*types.MongoAclsDoc, error) {
	encEmail, err := storage.EncryptionSvc.Encrypt(signupReq.UserEmail)
	if err != nil {
		return nil, fmt.Errorf("error encrypting email: %v", err)
	}
	llmEncEmail, err := storage.EncryptionSvc.Encrypt(config.Configs.LLMUserEmail)
	if err != nil {
		return nil, fmt.Errorf("error encrypting email: %v", err)
	}
	return &types.MongoAclsDoc{
		UserId: encEmail,
		Acls: map[types.ResourceType][]string{
			types.RESOURCE_USER_DETAILS:      {llmEncEmail, encEmail},
			types.RESOURCE_USER_PREFERENCES:  {llmEncEmail},
			types.RESOURCE_USER_REMINDERS:    {llmEncEmail, encEmail},
			types.RESOURCE_USER_CHAT_HISTORY: {llmEncEmail, encEmail},
			types.RESOURCE_RPM_READINGS:      {llmEncEmail, encEmail},
		},
	}, nil
}

func (as *AuthenticationService) Signup(signupReq *types.UserSignupRequest) (string, error) {
	exists, err := checkIfUserExists(signupReq)
	if err != nil {
		return "", err
	}
	if exists {
		return "", fmt.Errorf("user already exists")
	}

	userDoc, err := getUserDoc(signupReq)
	if err != nil {
		return "", err
	}
	err = storage.StorageSvc.InsertUserDoc(userDoc)
	if err != nil {
		return "", fmt.Errorf("error inserting user: %v", err)
	}

	aclDoc, err := getAclsDoc(signupReq)
	if err != nil {
		return "", err
	}
	err = storage.StorageSvc.InsertAclsDoc(aclDoc)
	if err != nil {
		return "", fmt.Errorf("error populating ACLs: %v", err)
	}

	token, err := as.GenerateToken(userDoc)
	if err != nil {
		return "", fmt.Errorf("error generating jwt token: %v", err)
	}
	return token, nil
}

func (as *AuthenticationService) Login(loginReq *types.UserLoginRequest) (string, error) {
	encEmail, err := storage.EncryptionSvc.Encrypt(loginReq.UserEmail)
	if err != nil {
		return "", fmt.Errorf("error encrypting email: %v", err)
	}
	userDoc, err := storage.StorageSvc.GetUserDoc(encEmail)
	if err != nil {
		return "", fmt.Errorf("error getting user doc: %v", err)
	}
	h := sha256.New()
	_, err = h.Write([]byte(loginReq.UserPassword))
	if err != nil {
		return "", fmt.Errorf("error getting hash: %v", err)
	}
	if userDoc.PasswordHash != hex.EncodeToString(h.Sum(nil)) {
		return "", fmt.Errorf("incorrect username or password")
	}
	return as.GenerateToken(userDoc)
}

func (as *AuthenticationService) VerifyToken(tokenString string) (*CustomRegisteredClaims, error) {
	token, err := jwt.ParseWithClaims(tokenString, &CustomRegisteredClaims{}, func(t *jwt.Token) (interface{}, error) { return []byte(config.Configs.AuthSecretKey), nil })
	if err != nil {
		return nil, fmt.Errorf("unable to verify the token: %v", err)
	}
	if !token.Valid {
		return nil, types.ErrInvalidToken
	}
	return token.Claims.(*CustomRegisteredClaims), nil
}

func (as *AuthenticationService) RequestAccess(requestAccessReq *types.RequestAccessRequest) (bool, error) {
	claims, err := as.VerifyToken(requestAccessReq.RequesterToken)
	if err != nil {
		return false, err
	}
	requesterId := claims.UserId
	docId := requestAccessReq.UserId
	acl, err := storage.StorageSvc.GetAclsDoc(docId)
	if err != nil {
		return false, fmt.Errorf("error getting acls: %v", err)
	}
	granted := true
	for _, res := range requestAccessReq.Resources {
		ok := false
		_, ok1 := acl.Acls[res]
		if !ok1 {
			return false, fmt.Errorf("unknown resource type %v", res)
		}
		for _, uid := range acl.Acls[res] {
			if uid == requesterId {
				ok = true
				break
			}
		}
		if !ok {
			granted = false
			break
		}
	}

	if !granted {
		return false, nil
	}
	return true, nil
}
