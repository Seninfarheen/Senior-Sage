package web

import (
	"authz/service"
	"authz/types"
	"encoding/json"
	"io"
	"log"

	"github.com/gin-gonic/gin"
)

func GetRouter() *gin.Engine {
	r := gin.Default()
	r.GET("/ping", func(c *gin.Context) {
		c.JSON(200, gin.H{
			"message": "pong",
		})
	})

	authG := r.Group("/auth/")
	authG.GET("/verify", verify)
	authG.POST("/gen-token", generateToken)
	authG.POST("/login", login)
	authG.POST("/signup", signup)

	// authorization - request access
	r.GET("/request-access", requestAccess)

	return r
}

func requestAccess(c *gin.Context) {
	bytes, err := io.ReadAll(c.Request.Body)
	if err != nil {
		c.JSON(400, gin.H{
			"error": "Bad Request",
			"msg":   err.Error(),
		})
		return
	}
	requestAccessReq := &types.RequestAccessRequest{}
	err = json.Unmarshal(bytes, requestAccessReq)
	if err != nil {
		c.JSON(400, gin.H{
			"error": "Bad Request",
			"msg":   err.Error(),
		})
		return
	}
	granted, err := service.AuthService.RequestAccess(requestAccessReq)
	if err != nil {
		c.JSON(404, gin.H{
			"error": "Bad Request",
			"msg":   err.Error(),
		})
		return
	}
	if granted {
		c.JSON(200, gin.H{
			"access_request": true,
		})
	} else {
		c.JSON(200, gin.H{
			"access_request": false,
		})
	}
}

func signup(c *gin.Context) {
	bytes, err := io.ReadAll(c.Request.Body)
	if err != nil {
		c.JSON(400, gin.H{
			"error": "Bad Request",
			"msg":   err.Error(),
		})
		return
	}
	signupReq := &types.UserSignupRequest{}
	err = json.Unmarshal(bytes, signupReq)
	if err != nil {
		c.JSON(400, gin.H{
			"error": "Bad Request",
			"msg":   err.Error(),
		})
		return
	}
	token, err := service.AuthService.Signup(signupReq)
	if err != nil {
		log.Println(err)
		c.JSON(400, gin.H{
			"error": "Bad Request",
			"msg":   err.Error(),
		})
		return
	}

	c.JSON(200, gin.H{
		"token": token,
		"msg":   "signup successful",
	})
}

func login(c *gin.Context) {
	bytes, err := io.ReadAll(c.Request.Body)
	if err != nil {
		c.JSON(400, gin.H{
			"error": "Bad Request",
			"msg":   err.Error(),
		})
		return
	}
	loginReq := &types.UserLoginRequest{}
	err = json.Unmarshal(bytes, loginReq)
	if err != nil {
		resp := &types.UserLoginResponse{
			Error: "Bad Request",
			Msg:   err.Error(),
		}
		c.JSON(400, resp)
		return
	}

	token, err := service.AuthService.Login(loginReq)
	if err != nil {
		resp := &types.UserLoginResponse{
			Error: "Bad Request",
			Msg:   err.Error(),
		}
		c.JSON(400, resp)
		return
	}
	resp := &types.UserLoginResponse{
		Token: token,
		Msg:   "login successful",
	}
	c.JSON(200, resp)
}

func generateToken(c *gin.Context) {
	bytes, err := io.ReadAll(c.Request.Body)
	if err != nil {
		c.JSON(400, gin.H{
			"error": "Bad Request",
			"msg":   err.Error(),
		})
		return
	}
	tokenGenReq := &types.UserDetails{}
	err = json.Unmarshal(bytes, tokenGenReq)
	if err != nil {
		c.JSON(400, gin.H{
			"error": "Bad Request",
			"msg":   err.Error(),
		})
		return
	}
	tokenString, err := service.AuthService.GenerateToken(tokenGenReq)
	if err != nil {
		c.JSON(400, gin.H{
			"error": "Error generating token",
			"msg":   err.Error(),
		})
		return
	}
	c.JSON(200, gin.H{
		"token": tokenString,
	})
}

func verify(c *gin.Context) {
	bytes, err := io.ReadAll(c.Request.Body)
	if err != nil {
		c.JSON(400, gin.H{
			"error": "Bad Request",
			"msg":   err.Error(),
		})
		return
	}
	authReq := &types.AuthVerifyRequest{}
	err = json.Unmarshal(bytes, authReq)
	if err != nil {
		c.JSON(400, gin.H{
			"error": "Bad Request",
			"msg":   err.Error(),
		})
		return
	}

	claims, err := service.AuthService.VerifyToken(authReq.JWTToken)
	if err != nil {
		if err == types.ErrInvalidToken {
			c.JSON(200, gin.H{
				"valid": "false",
			})
			return
		}
		c.JSON(500, gin.H{
			"error": "Unknown internal error",
			"msg":   err.Error(),
		})
		return
	}

	c.JSON(200, gin.H{
		"valid":      "true",
		"user_id":    claims.UserId,
	})
}
