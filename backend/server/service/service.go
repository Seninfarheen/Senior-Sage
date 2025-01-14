package service

import "server/types"

type AuthenticationService struct {
}

var AuthService *AuthenticationService

func init() {
	AuthService = &AuthenticationService{}
}

func (s *AuthenticationService) GetUserDetails(userId string, userToken string) (*types.GetUserDetailsResponse, error) {
	userDetails, err := StorageSvc.GetUserDetails(userId, userToken)
	return userDetails, err
}
