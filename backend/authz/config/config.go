package config

import (
	"fmt"
	"io"
	"os"

	"gopkg.in/yaml.v3"
)

type DBConfig struct {
	Host            string `yaml:"host"`
	Port            int    `yaml:"port"`
	User            string `yaml:"user"`
	Password        string `yaml:"password"`
	DBName          string `yaml:"database"`
	AppName         string `yaml:"appname"`
	UsersCollection string `yaml:"usersCollection"`
	AclsCollection  string `yaml:"aclsCollection"`
}

type Config struct {
	DBConfig      *DBConfig `yaml:"db"`
	DataEncryptionKey string      `yaml:"encryptionKey"`
	AuthSecretKey string    `yaml:"authSecretKey"`
	LLMUserEmail  string    `yaml:"llmUsername"`
}

var Configs *Config

func LoadConfig() {
	// read config from file
	Configs = &Config{}
	Configs.DBConfig = &DBConfig{}
	configFilePath := "/app/config/conf.yaml"
	f, err := os.Open(configFilePath)
	if err != nil {
		fmt.Println(err)
		os.Exit(1)
	}
	configBytes, err := io.ReadAll(f)
	if err != nil {
		fmt.Println(err)
		os.Exit(1)
	}
	yaml.Unmarshal(configBytes, Configs)
}
