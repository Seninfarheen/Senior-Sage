package types

import (
	"fmt"
)

// Request types
type AuthVerifyRequest struct {
	JWTToken string `json:"jwt_token"`
}

type ResourceType string

const (
	RESOURCE_USER_DETAILS      ResourceType = "USER_DETAILS"
	RESOURCE_USER_PREFERENCES  ResourceType = "USER_PREFERENCES"
	RESOURCE_USER_REMINDERS    ResourceType = "USER_REMINDERS"
	RESOURCE_USER_CHAT_HISTORY ResourceType = "USER_CHAT_HISTORY"
	RESOURCE_RPM_READINGS      ResourceType = "RPM_READINGS"
	RESOURCE_UNKNOWN           ResourceType = "UNKNOWN"
)

var ResourceList = []ResourceType{
	RESOURCE_USER_CHAT_HISTORY,
	RESOURCE_USER_PREFERENCES,
	RESOURCE_USER_REMINDERS,
	RESOURCE_RPM_READINGS,
}

var ErrAccessDenied error = fmt.Errorf("access denied")
