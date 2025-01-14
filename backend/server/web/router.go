package web

import (
	"log"
	"server/service"

	"github.com/gin-gonic/gin"
)

func GetRouter() *gin.Engine {
	r := gin.Default()
	r.GET("/ping", func(c *gin.Context) {
		c.JSON(200, gin.H{
			"message": "pong",
		})
	})

	// authorization - request access
	r.GET("/user-details", getUserDetails, authMiddleware)

	return r
}

func getUserDetails(c *gin.Context) {
	userId := c.GetString("user-id")
	userToken := c.GetHeader("Authorization")
	userDetails, err := service.AuthService.GetUserDetails(userId, userToken)
	if err != nil {
		log.Printf("error in getting user details: %v\n", err)
		c.JSON(500, gin.H{"error": "Internal Server Error"})
		return
	}
	c.JSON(200, userDetails)
}
