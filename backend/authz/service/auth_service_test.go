package service

import (
	"authz/config"
	"authz/storage"
	"authz/types"
	"crypto/sha256"
	"encoding/hex"
	"fmt"
	"testing"

	"github.com/stretchr/testify/assert"
	"go.mongodb.org/mongo-driver/mongo"
)

// func Test_Verify(t *testing.T) {
// 	setup()
// 	defer teardown()
// 	authService := &AuthenticationService{}
// 	testUserDetails := &types.UserDetails{
// 		UserId:    "u_id",
// 		UserEmail: "testuser",
// 	}
// 	ss, err := authService.GenerateToken(testUserDetails)
// 	assert.NoError(t, err, "GenerateToken() should not throw error")
// 	assert.NotEmpty(t, ss, "generated token shouldn't be empty")

// 	claims, err := authService.VerifyToken(ss)
// 	assert.NoError(t, err)
// 	assert.NotNil(t, claims)

// 	config.Configs.AuthSecretKey = "newsecretkey"

// 	claims, err = authService.VerifyToken(ss)
// 	assert.Error(t, err)
// 	assert.Nil(t, claims)
// }

func Test_RequestAccess(t *testing.T) {
	setup()
	defer teardown()
	authService := &AuthenticationService{}

	requesterEmail := "testuser@email.com"
	// encrypted requester email
	requesterId, err := storage.EncryptionSvc.Encrypt(requesterEmail)
	assert.NoError(t, err, "encryption should not throw error")
	testUserDetails := &types.UserDetails{
		UserEmail: requesterEmail,
	}
	ss, err := authService.GenerateToken(testUserDetails)
	assert.NoError(t, err, "GenerateToken() should not throw error")
	assert.NotEmpty(t, ss, "generated token shouldn't be empty")
	mockedStorage := storage.StorageSvc.(*storage.IStorageServiceMock)

	// test granted
	mockUserId := "test_user_id"
	requestAccessReq := &types.RequestAccessRequest{
		RequesterToken: ss,
		UserId:         mockUserId,
		Resources:      []types.ResourceType{types.RESOURCE_USER_DETAILS, types.RESOURCE_USER_REMINDERS},
	}
	mockedStorage.GetAclsDocFunc = func(UserId string) (*types.MongoAclsDoc, error) {
		assert.Equal(t, mockUserId, UserId)
		return &types.MongoAclsDoc{
			AclId:  "aclid",
			UserId: UserId,
			Acls: map[types.ResourceType][]string{
				types.RESOURCE_USER_DETAILS:     {requesterId, "other_id"},
				types.RESOURCE_USER_PREFERENCES: {"other_id"},
				types.RESOURCE_USER_REMINDERS:   {requesterId},
			},
		}, nil
	}
	granted, err := authService.RequestAccess(requestAccessReq)
	assert.NoError(t, err)
	assert.True(t, granted)

	// test denied
	mockedStorage.GetAclsDocFunc = func(UserId string) (*types.MongoAclsDoc, error) {
		return &types.MongoAclsDoc{
			AclId:  "aclid",
			UserId: UserId,
			Acls: map[types.ResourceType][]string{
				types.RESOURCE_USER_DETAILS:     {requesterId, "other_id"},
				types.RESOURCE_USER_PREFERENCES: {"other_id"},
				types.RESOURCE_USER_REMINDERS:   {},
			},
		}, nil
	}
	granted, err = authService.RequestAccess(requestAccessReq)
	assert.NoError(t, err)
	assert.False(t, granted)

	// test unknown resource request
	mockedStorage.GetAclsDocFunc = func(UserId string) (*types.MongoAclsDoc, error) {
		return &types.MongoAclsDoc{
			AclId:  "aclid",
			UserId: UserId,
			Acls: map[types.ResourceType][]string{
				types.RESOURCE_USER_DETAILS:     {requesterId, "other_id"},
				types.RESOURCE_USER_PREFERENCES: {"other_id"},
			},
		}, nil
	}
	granted, err = authService.RequestAccess(requestAccessReq)
	assert.Error(t, err)
	assert.False(t, granted)

	// test storage error
	mockedStorage.GetAclsDocFunc = func(UserId string) (*types.MongoAclsDoc, error) {
		return nil, fmt.Errorf("some db error")
	}
	granted, err = authService.RequestAccess(requestAccessReq)
	assert.Error(t, err)
	assert.False(t, granted)

}

func Test_GenerateToken(t *testing.T) {
	setup()
	defer teardown()
	authService := &AuthenticationService{}
	testUserDetails := &types.UserDetails{
		UserEmail: "testuser@email.com",
	}
	ss, err := authService.GenerateToken(testUserDetails)
	assert.NoError(t, err, "GenerateToken() should not throw error")
	assert.NotEmpty(t, ss, "generated token shouldn't be empty")
}

func Test_Login_Success(t *testing.T) {
	setup()
	defer teardown()
	authService := &AuthenticationService{}
	mockedStorage := storage.StorageSvc.(*storage.IStorageServiceMock)
	mockPassword := "mypass"
	userEmail := "testuser@mail.com"
	hash := sha256.New()
	hash.Write([]byte(mockPassword))
	hashedPassword := hex.EncodeToString(hash.Sum(nil))
	mockedStorage.GetUserDocFunc = func(email string) (*types.UserDetails, error) {
		return &types.UserDetails{
			UserEmail:    userEmail,
			PasswordHash: hashedPassword,
		}, nil
	}
	loginReq := &types.UserLoginRequest{
		UserEmail:    userEmail,
		UserPassword: mockPassword,
	}

	tkn, err := authService.Login(loginReq)
	assert.NoError(t, err, "should succeed")
	assert.NotEmpty(t, tkn, "should not be empty")
	assert.Equal(t, 1, len(mockedStorage.GetUserDocCalls()))
}

func Test_Login_Fail(t *testing.T) {
	setup()
	defer teardown()
	authService := &AuthenticationService{}
	mockedStorage := storage.StorageSvc.(*storage.IStorageServiceMock)
	mockPassword := "mypass"
	userEmail := "testuser@mail.com"
	hash := sha256.New()
	hash.Write([]byte(mockPassword))
	hashedPassword := hex.EncodeToString(hash.Sum(nil))
	mockedStorage.GetUserDocFunc = func(email string) (*types.UserDetails, error) {
		return &types.UserDetails{
			UserEmail:    userEmail,
			PasswordHash: hashedPassword,
		}, nil
	}
	loginReq := &types.UserLoginRequest{
		UserEmail: userEmail,
		// wrong password
		UserPassword: "wrongpass",
	}

	tkn, err := authService.Login(loginReq)
	assert.Error(t, err, "should succeed")
	assert.Empty(t, tkn, "should not be empty")
	assert.Equal(t, 1, len(mockedStorage.GetUserDocCalls()))
}

func Test_SignUp_InsertError(t *testing.T) {
	setup()
	defer teardown()
	authService := &AuthenticationService{}
	storageMock := storage.StorageSvc.(*storage.IStorageServiceMock)
	storageMock.GetUserDocFunc = func(s string) (*types.UserDetails, error) {
		return nil, mongo.ErrNoDocuments
	}
	storageMock.InsertUserDocFunc = func(userDetails *types.UserDetails) error {
		return fmt.Errorf("insert error")
	}
	testSignupReq := &types.UserSignupRequest{
		UserEmail:    "test@mail.com",
		UserPassword: "testpass",
	}
	tkn, err := authService.Signup(testSignupReq)
	assert.Error(t, err)
	assert.Empty(t, tkn)
	assert.Equal(t, 1, len(storageMock.GetUserDocCalls()))
	assert.Equal(t, 1, len(storageMock.InsertUserDocCalls()))
}

func Test_SignUp_Success(t *testing.T) {
	setup()
	defer teardown()
	authService := &AuthenticationService{}
	storageMock := storage.StorageSvc.(*storage.IStorageServiceMock)
	storageMock.GetUserDocFunc = func(s string) (*types.UserDetails, error) {
		return nil, mongo.ErrNoDocuments
	}
	storageMock.InsertUserDocFunc = func(userDetails *types.UserDetails) error {
		return nil
	}
	storageMock.InsertAclsDocFunc = func(aclsDoc *types.MongoAclsDoc) error {
		return nil
	}
	testSignupReq := &types.UserSignupRequest{
		VoiceSelection: "default",
		Name:           "testuser",
		UserEmail:      "test@mail.com",
		UserPassword:   "testpass",
	}
	tkn, err := authService.Signup(testSignupReq)
	assert.NoError(t, err)
	assert.NotEmpty(t, tkn)
	assert.Equal(t, 1, len(storageMock.GetUserDocCalls()))
	assert.Equal(t, 1, len(storageMock.InsertUserDocCalls()))
}

func Test_SignUp_ShouldErrorWhenExistingUserFound(t *testing.T) {
	setup()
	defer teardown()
	authService := &AuthenticationService{}
	storageMock := storage.StorageSvc.(*storage.IStorageServiceMock)
	storageMock.GetUserDocFunc = func(s string) (*types.UserDetails, error) {
		return &types.UserDetails{}, nil
	}
	testSignupReq := &types.UserSignupRequest{
		UserEmail:    "test@mail.com",
		UserPassword: "testpass",
	}
	tkn, err := authService.Signup(testSignupReq)
	assert.Error(t, err, "should error when existing email account found")
	assert.Equal(t, "user already exists", err.Error())
	assert.Empty(t, tkn)
	assert.Equal(t, 1, len(storageMock.GetUserDocCalls()))
}

func setup() {
	config.Configs = &config.Config{}
	config.Configs.DBConfig = &config.DBConfig{}
	config.Configs.AuthSecretKey = "test_secret_key"
	storage.StorageSvc = &storage.IStorageServiceMock{}
	storage.EncryptionSvc = storage.NewEncryptionService("test_keytest_key")
}

func teardown() {

}
