package storage

import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	"storage-service/config"
	"storage-service/types"
	"time"

	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

type StorageService struct {
	client *mongo.Client
}

//go:generate moq -out storageservice_mock.go . IStorageService
type IStorageService interface {
	InsertUserDoc(userDetails *types.UserDetails) error
	UpdateUserDoc(userDetails *types.UserDetails) error
	GetUserDoc(email string) (*types.UserDetails, error)
}

var StorageSvc IStorageService

func InitStorage() error {
	log.Println("Connecting to DB")
	storageSvc := &StorageService{}
	uname := config.Configs.DBConfig.User
	pass := config.Configs.DBConfig.Password
	host := config.Configs.DBConfig.Host
	appname := config.Configs.DBConfig.AppName
	uri := "mongodb+srv://" + uname + ":" + pass + "@" + host + "/?retryWrites=true&w=majority&appName=" + appname
	ctx, cancel := context.WithTimeout(context.Background(), time.Second*10)
	defer cancel()
	client, err := mongo.Connect(ctx, options.Client().ApplyURI(uri))
	if err != nil {
		return fmt.Errorf("error connection to db: %v", err)
	}
	storageSvc.client = client
	StorageSvc = storageSvc
	return nil
}

func (s *StorageService) InsertUserDoc(userDetails *types.UserDetails) error {

	bytes, err := json.Marshal(userDetails)
	if err != nil {
		return fmt.Errorf("error marshalling user data: %v", err)
	}
	log.Printf("user details inserting: %v\n", string(bytes))
	encData, err := EncryptionSvc.Encrypt(string(bytes))
	if err != nil {
		return fmt.Errorf("error encrypting user data: %v", err)
	}
	encEmail, err := EncryptionSvc.Encrypt(userDetails.UserEmail)
	if err != nil {
		return fmt.Errorf("error encrypting user email: %v", err)
	}
	userDoc := &types.MongoUserDoc{
		Email: encEmail,
		Data:  encData,
	}
	coll := s.client.Database(config.Configs.DBConfig.DBName).Collection(config.Configs.DBConfig.UsersCollection)
	_, err = coll.InsertOne(context.Background(), userDoc)
	if err != nil {
		return fmt.Errorf("error inserting into db: %v", err)
	}
	return nil
}

func (s *StorageService) UpdateUserDoc(userDetails *types.UserDetails) error {

	bytes, err := json.Marshal(userDetails)
	if err != nil {
		return fmt.Errorf("error marshalling user data: %v", err)
	}
	log.Printf("user details updating: %v\n", string(bytes))
	encData, err := EncryptionSvc.Encrypt(string(bytes))
	if err != nil {
		return fmt.Errorf("error encrypting user data: %v", err)
	}
	encEmail, err := EncryptionSvc.Encrypt(userDetails.UserEmail)
	if err != nil {
		return fmt.Errorf("error encrypting user email: %v", err)
	}
	userDoc := &types.MongoUserDoc{
		// Email: encEmail,
		Data:  encData,
	}
	coll := s.client.Database(config.Configs.DBConfig.DBName).Collection(config.Configs.DBConfig.UsersCollection)
	_, err = coll.UpdateOne(context.Background(), bson.D{bson.E{Key: "email", Value: encEmail}}, bson.D{bson.E{Key: "$set", Value: bson.D{bson.E{Key: "data", Value: userDoc.Data}}}})
	if err != nil {
		return fmt.Errorf("error inserting into db: %v", err)
	}
	return nil
}

func (s *StorageService) GetUserDoc(email string) (*types.UserDetails, error) {
	coll := s.client.Database(config.Configs.DBConfig.DBName).Collection(config.Configs.DBConfig.UsersCollection)
	var result types.MongoUserDoc
	err := coll.FindOne(context.Background(), bson.D{bson.E{Key: "email", Value: email}}).Decode(&result)
	if err != nil {
		return nil, fmt.Errorf("error finding the user: %v", err)
	}
	userDoc := &types.UserDetails{}
	decryptedJsonData, err := EncryptionSvc.Decrypt(result.Data)
	if err != nil {
		return nil, fmt.Errorf("error decrypting user data: %v", err)
	}
	err = json.Unmarshal([]byte(decryptedJsonData), userDoc)
	if err != nil {
		return nil, fmt.Errorf("error unmarshalling user data: %v", err)
	}
	return userDoc, nil
}
