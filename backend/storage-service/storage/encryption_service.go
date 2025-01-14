package storage

import (
	"bytes"
	"crypto/aes"
	"encoding/hex"
	"errors"
	"storage-service/config"
)

type EncryptionService struct {
    key []byte
}

var EncryptionSvc *EncryptionService

func NewEncryptionService(key string) *EncryptionService {
    return &EncryptionService{
        key: []byte(key),
    }
}

func InitEncryptionService() {
	encKey := config.Configs.DataEncryptionKey
	EncryptionSvc = NewEncryptionService(encKey)
}

func (s *EncryptionService) Encrypt(plaintext string) (string, error) {
    block, err := aes.NewCipher(s.key)
    if err != nil {
        return "", err
    }

    plaintextBytes := []byte(plaintext)
    plaintextBytes = pkcs7Padding(plaintextBytes, aes.BlockSize)

    ciphertext := make([]byte, len(plaintextBytes))
    mode := NewECBEncrypter(block)
    mode.CryptBlocks(ciphertext, plaintextBytes)

    return hex.EncodeToString(ciphertext), nil
}

func (s *EncryptionService) Decrypt(ciphertext string) (string, error) {
    ciphertextBytes, err := hex.DecodeString(ciphertext)
    if err != nil {
        return "", err
    }

    block, err := aes.NewCipher(s.key)
    if err != nil {
        return "", err
    }

    if len(ciphertextBytes)%aes.BlockSize != 0 {
        return "", errors.New("ciphertext is not a multiple of the block size")
    }

    plaintext := make([]byte, len(ciphertextBytes))
    mode := NewECBDecrypter(block)
    mode.CryptBlocks(plaintext, ciphertextBytes)

    plaintext = pkcs7Unpadding(plaintext)

    return string(plaintext), nil
}

func pkcs7Padding(data []byte, blockSize int) []byte {
    padding := blockSize - len(data)%blockSize
    padtext := bytes.Repeat([]byte{byte(padding)}, padding)
    return append(data, padtext...)
}

func pkcs7Unpadding(data []byte) []byte {
    length := len(data)
    unpadding := int(data[length-1])
    return data[:(length - unpadding)]
}