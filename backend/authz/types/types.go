package types

type UserDetails struct {
	// UserId    string `json:"user_id"`
	Name                string                  `json:"name"`
	UserEmail           string                  `json:"username"`
	PasswordHash        string                  `json:"password_hash"`
	ReminderDetails     *[]ReminderDetails      `json:"reminders,omitempty"`
	RPMReadings         *[]RPMReading           `json:"rpm_readings,omitempty"`
	Preferences         *[]string               `json:"preferences,omitempty"`
	ChatHistory         *[]ChatSession          `json:"chat_history,omitempty"`
	RegisteredRPMDevice int64                   `json:"registered_rpm_device"`
	VoiceSelection      string                  `json:"voice_selection"`
	QuestionResponses   *[]QuestionResponse     `json:"question_responses,omitempty"`
	QuestionCounts      map[int]QuestionCounter `json:"question_counts"`
}

type QuestionResponse struct {
	QuestionId int    `json:"q_id"`
	Question   string `json:"question"`
	Date       string `json:"date"`
	Answer     string `json:"answer"`
}

type ChatSession struct {
	// iso format timestamp
	TimeStamp string         `json:"timestamp"`
	Messages  []*ChatMessage `json:"messages"`
}

type ChatMessage struct {
	// iso format timestamp
	TimeStamp   string `json:"timestamp"`
	UserMessage string `json:"user_message"`
	BotResponse string `json:"bot_response"`
}

type RPMReading struct {
	Id        int64  `json:"id"`
	Type      string `json:"type"`
	Value     string `json:"value"`
	TimeStamp int64  `json:"timestamp"`
	TimeStr   string `json:"time_str"`
}

type Reminders struct {
	ReminderFor string             `json:"reminder_for"`
	Reminder    []*ReminderDetails `json:"details"`
}

type ReminderDetails struct {
	Time      string `json:"time"`
	Frequency string `json:"frequency"`
	StartDate string `json:"start_date"`
	Cron      string `json:"cron_job"`
}

type MongoUserDoc struct {
	Email string `bson:"email,omitempty"`
	Data  string `bson:"data,omitempty"`
}
