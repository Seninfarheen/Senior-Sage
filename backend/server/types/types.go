package types

type GetUserDetailsResponse struct {
	Name                string             `json:"name"`
	UserEmail           string             `json:"username"`
	RegisteredRPMDevice int64              `json:"registered_rpm_device"`
	VoiceSelection      string             `json:"voice_selection"`
	ReminderDetails     *[]ReminderDetails `json:"reminders,omitempty"`
	RPMReadings         *[]RPMReading      `json:"rpm_readings,omitempty"`
}

type GetVerifyTokenResponse struct {
	Valid  string `json:"valid"`
	UserId string `json:"user_id"`
}

type ReminderDetails struct {
	Time      string `json:"time"`
	Frequency string `json:"frequency"`
	StartDate string `json:"start_date"`
	Cron      string `json:"cron_job"`
}

type RPMReading struct {
	Id        int64  `json:"id"`
	Type      string `json:"type"`
	Value     string `json:"value"`
	TimeStamp int64  `json:"timestamp"`
	TimeStr   string `json:"time_str"`
}

type GetUserDetailsRequest struct {
	UserId         string `json:"user_id"`
	RequesterToken string `json:"requester_token"`
}
