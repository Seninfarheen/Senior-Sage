package types

import (
	"fmt"
)



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

const (
	MONGO_USER_DETAILS_FIELD     = "user_details"
	MONGO_USER_PREFERENCES_FIELD = "user_preferences"
	MONGO_USER_REMINDERS_FIELD   = "user_reminders"
)

var ResourceToMongoField map[ResourceType]string = map[ResourceType]string{
	RESOURCE_USER_DETAILS:     MONGO_USER_DETAILS_FIELD,
	RESOURCE_USER_PREFERENCES: MONGO_USER_PREFERENCES_FIELD,
	RESOURCE_USER_REMINDERS:   MONGO_USER_REMINDERS_FIELD,
}

var ResourceIdToString map[ResourceType]string = map[ResourceType]string{
	RESOURCE_USER_DETAILS:     "UserDetailsResource",
	RESOURCE_USER_PREFERENCES: "UserPreferenceResource",
	RESOURCE_USER_REMINDERS:   "UserRemindersResource",
}

type MongoAclsDoc struct {
	AclId  string                    `bson:"_id,omitempty",json:"acl_id,omitempty"`
	UserId string                    `bson:"uid,omitempty",json:"user_id,omitempty"`
	Acls   map[ResourceType][]string `bson:"acls,omitempty",json:"acls,omitempty"`
}

var ErrInvalidToken = fmt.Errorf("invalid token")
var ErrAccessDenied error = fmt.Errorf("access denied")
