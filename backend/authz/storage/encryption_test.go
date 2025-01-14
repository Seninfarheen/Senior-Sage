package storage

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func Test_Encryption(t *testing.T) {
	EncryptionSvc = NewEncryptionService("test_keytest_key")
	plaintext := "{\"key\":\"value\"}"
	ciphertext, err := EncryptionSvc.Encrypt(plaintext)
	assert.NoError(t, err)
	assert.NotEqual(t, plaintext, ciphertext)

	decrypted, err := EncryptionSvc.Decrypt(ciphertext)
	assert.NoError(t, err)
	assert.Equal(t, plaintext, decrypted)
}
