package web

import (
	"authz/config"
	"authz/storage"
	"authz/types"
	"bytes"
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"

	"github.com/stretchr/testify/assert"
)

func Test_Login_Success(t *testing.T) {
	setup()
	defer teardown()
	
	mockedStorage := storage.StorageSvc.(*storage.IStorageServiceMock)
	testUserEmail := "testuser@email.com"
	mockPassword := "mypass"
	hash := sha256.New()
	hash.Write([]byte(mockPassword))
	hashedPassword := hex.EncodeToString(hash.Sum(nil))
	mockedStorage.GetUserDocFunc = func(email string) (*types.UserDetails, error) {
		return &types.UserDetails{
			UserEmail:      testUserEmail,
			Name:           "testuser",
			PasswordHash:   hashedPassword,
			VoiceSelection: "default",
		}, nil
	}

	router := GetRouter()
	w := httptest.NewRecorder()
	testLoginReq := &types.UserLoginRequest{
		UserEmail:    testUserEmail,
		UserPassword: mockPassword,
	}
	reqJson, _ := json.Marshal(testLoginReq)
	req, _ := http.NewRequest("POST", "/auth/login", bytes.NewBuffer(reqJson))
	router.ServeHTTP(w, req)

	assert.Equal(t, http.StatusOK, w.Code)
	resp := &types.UserLoginResponse{}
	err := json.Unmarshal(w.Body.Bytes(), resp)
	assert.NoError(t, err)
	assert.NotEmpty(t, resp.Token)
	assert.Equal(t, "login successful", resp.Msg)
}

func Test_Login_Fail(t *testing.T) {
	setup()
	defer teardown()
	
	mockedStorage := storage.StorageSvc.(*storage.IStorageServiceMock)
	testUserEmail := "testuser@email.com"
	mockPassword := "mypass"
	hash := sha256.New()
	hash.Write([]byte(mockPassword))
	hashedPassword := hex.EncodeToString(hash.Sum(nil))
	mockedStorage.GetUserDocFunc = func(email string) (*types.UserDetails, error) {
		return &types.UserDetails{
			UserEmail:      testUserEmail,
			Name:           "testuser",
			PasswordHash:   hashedPassword,
			VoiceSelection: "default",
		}, nil
	}

	router := GetRouter()
	w := httptest.NewRecorder()
	wrongpass := "wrongpass"
	testLoginReq := &types.UserLoginRequest{
		UserEmail:    testUserEmail,
		UserPassword: wrongpass,
	}
	reqJson, _ := json.Marshal(testLoginReq)
	req, _ := http.NewRequest("POST", "/auth/login", bytes.NewBuffer(reqJson))
	router.ServeHTTP(w, req)

	assert.Equal(t, http.StatusBadRequest, w.Code)
	resp := &types.UserLoginResponse{}
	err := json.Unmarshal(w.Body.Bytes(), resp)
	assert.NoError(t, err)
	assert.Empty(t, resp.Token)
	assert.NotEmpty(t, resp.Msg)
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
