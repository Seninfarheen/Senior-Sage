package config

import (
	"fmt"
	"io"
	"os"

	"gopkg.in/yaml.v3"
)

type StorageSvcConfig struct {
	Host string `yaml:"host"`
	Port int    `yaml:"port"`
}

type AuthSvcConfig struct {
	Host string `yaml:"host"`
	Port int    `yaml:"port"`
}

type Config struct {
	StorageSvcConfig *StorageSvcConfig `yaml:"storageConfig"`
	AuthSvcConfig    *AuthSvcConfig    `yaml:"authzConfig"`
}

var Configs *Config

func LoadConfig() {
	// read config from file
	Configs = &Config{}
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
