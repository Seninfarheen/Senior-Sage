package web

import (
	"log"
	"server/service"

	"github.com/gin-gonic/gin"
)

func authMiddleware(c *gin.Context) {
	token := c.GetHeader("Authorization")
	if token == "" {
		c.JSON(401, gin.H{"error": "Unauthorized"})
		c.Abort()
		return
	}
	valid, userid, err := service.AuthzClientSvc.VerifyToken(token)
	if err != nil {
		log.Printf("error in verifying token: %v", err)
		c.JSON(500, gin.H{"error": "Internal Server Error"})
		c.Abort()
		return
	}
	if !valid {
		c.JSON(401, gin.H{"error": "Unauthorized"})
		c.Abort()
		return
	}
	c.Set("user-id", userid)
	c.Next()
}
