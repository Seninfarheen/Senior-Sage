package service

import (
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"server/config"
	"server/types"
	"strconv"
	"strings"
)

var AuthzClientSvc IAuthzClientService

type IAuthzClientService interface {
	VerifyToken(token string) (bool, string, error)
}

func SetAuthzClientService(svc IAuthzClientService) {
	AuthzClientSvc = svc
}

func init() {
	AuthzClientSvc = &AuthzClientService{}
}

type AuthzClientService struct {
}

func (as *AuthzClientService) VerifyToken(token string) (bool, string, error) {
	reqStr := fmt.Sprintf(`{"jwt_token": "%s"}`, token)
	req, err := http.NewRequest("GET", "http://"+config.Configs.AuthSvcConfig.Host+":"+strconv.Itoa(config.Configs.AuthSvcConfig.Port)+"/verify-token", strings.NewReader(reqStr))
	if err != nil {
		return false, "", fmt.Errorf("error in creating request to authz service: %v", err)
	}
	resp, err := http.DefaultClient.Do(req)
	if err != nil {
		return false, "", fmt.Errorf("error in making request to authz service: %v", err)
	}
	defer resp.Body.Close()
	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return false, "", fmt.Errorf("error in reading response from authz service: %v", err)
	}
	if resp.StatusCode != 200 {
		return false, "", fmt.Errorf("error in authz service: %s", body)
	}
	verifyResp := &types.GetVerifyTokenResponse{}
	err = json.Unmarshal(body, verifyResp)
	if err != nil {
		return false, "", fmt.Errorf("error in unmarshalling response from authz service: %v", err)
	}
	if verifyResp.Valid == "true" {
		return true, verifyResp.UserId, nil
	} else {
		return false, verifyResp.UserId, nil
	}
}
