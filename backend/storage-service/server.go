package main

// import gin

import (
	"fmt"

	"storage-service/config"
	"storage-service/storage"
	"storage-service/web"
)

func main() {
	// Load the configs
	config.LoadConfig()
	// Init DB connection
	storage.InitStorage()
	storage.InitEncryptionService()
	// Start the server
	r := web.GetRouter()
	err := r.Run()
	if err != nil {
		fmt.Println("Error: ", err)
	}
}
