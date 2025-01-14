package main

// import gin

import (
	"fmt"

	"authz/config"
	"authz/storage"
	"authz/web"
)

func main() {
	// Load the configs
	config.LoadConfig()
	// Init DB connection
	storage.InitStorage()
	// Start the server
	r := web.GetRouter()
	err := r.Run()
	if err != nil {
		fmt.Println("Error: ", err)
	}
}
