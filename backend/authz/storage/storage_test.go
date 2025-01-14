package storage

//--------THIS TEST SHOULD NOT BE RUN AS PART OF CI/CD. THIS IS JUST FOR LOCAL DB CONNECTION TESTING-------------
//--------ASK A TEAM MEMBER FOR DB PASSWORD TO TEST AND DEBUG CONNECTION----------
// func Test_GetHash(t *testing.T) {
// 	setup(t)
// 	defer teardown(t)
// 	mockhash := "fesde"
// 	hash, err := StorageSvc.GetUserHash("test@mail.com")
// 	assert.NoError(t, err)
// 	assert.Equal(t, mockhash, hash)
// }

// func setup(t *testing.T) {
// 	config.Configs = &config.Config{DBConfig: &config.DBConfig{
// 		Host: "mymongocluster.r1pcx2q.mongodb.net",
// 		User: "sage",
// 		Password: "", // INSERT DB PASSWORD HERE
// 		DBName: "sage",
// 		AppName: "MyMongoCluster",
// 		UsersCollection: "users",
// 	}}
// 	err := InitStorage()
// 	fmt.Println("done init")
// 	assert.NoError(t, err)

// }

// func teardown(t *testing.T) {
// 	err := StorageSvc.(*StorageService).client.Disconnect(context.Background())
// 	assert.NoError(t, err)
// }
/*
cat > conf.yaml <<EOF
authSecretKey: testkey
db:
  host: mymongocluster.r1pcx2q.mongodb.net
  user: sage
  password: oQZxNrwTuKBsmAgu
  database: sage
  appname: users
  users: users
EOF
*/
