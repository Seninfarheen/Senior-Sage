# Senior Sage

The primary objective of this project is to enhance the **Vitalink management app** by developing a voice assistant (VA) specifically tailored for senior users in healthcare management. This voice assistant will collect health-related information through natural, conversational interactions, allowing doctors and researchers to gain insights without making users feel like they are undergoing a medical assessment. The VA will simulate a doctor-patient conversation to help seniors feel more comfortable sharing information about their well-being.

Our aim is to create short, efficient conversations that seamlessly fit into the user’s daily routine, encouraging consistent engagement. These interactions will help gather valuable data on emotions, mood, and general health, which will contribute to ongoing research on chronic conditions such as hypertension and heart failure. While the VA will not track blood pressure directly, it supports Vitalink’s broader goal of promoting healthy habits, such as regular blood pressure checks, by engaging users regularly in a natural way.

## Guidelines to set up and run the project

### React-native application setup
- Install Java, Android Studio, Android SDK, nodejs
    - Checkout this guide from official react-native website for more detailed guide to set up your environment: https://reactnative.dev/docs/set-up-your-environment
    - Additional resource: Microsoft's React Native for Android tutorial
- Clone this project
- Navigate to `app/` dir
- Run `npm install` to install all the dependencies for the project
- Connect your android device to laptop (or use emulators in android studio)
    - Ensure you have enabled debugging mode on your android phone
    - Run `adb devices` and ensure you are seeing your device connected before installing the app
- Run `npx react-native run-android` to build and install the app on your device

### Backend server setup
- Ensure you are running this in a virtual environment
- Navigate to `backend/server/flaskr/`
- Run `pip install -r requirements.txt`
- From the same directory run `flask --app server run`

### Authorization server setup
#### Set up
- `authz` service is written `golang`. So, ensure you have installed go on your local: [Install go](https://go.dev/doc/install). Requires go version `1.23`
- Navigate to dir `backend/authz` and run `go mod download` to install dependencies
- Run `go install github.com/matryer/moq@latest` to install `moq` to generate mocks for testing
- Run `go generate ./...` to generate the mocks
- Run `go test ./...` to run the tests on local


#### Run
- Run in docker
- From the root dir run `docker build -t authz -f docker/authz/Dockerfile backend/authz` to build image
- Run `docker run -it --rm -p 8080:8080 --entrypoint bash authz`
- This should open up a terminal to the docker container
- Add the `conf.yaml` file for the server:
```
mkdir config
cd config
cat > conf.yaml <<EOF
authSecretKey: testkey
llmUsername: llmuser
db:
  host: mymongocluster.r1pcx2q.mongodb.net
  user: sage
  password: oQZxNrwTuKBsmAgu
  database: sage
  appname: users
  users_collection: users
  acls_collection: acls
EOF
```
- Run `cd ../` and `./authz` to start the server
- This should start the server in the docker and expose port on local on 8080

### LLM functionalities setup
- Install ffmpeg
    - Using `chocolatey` for windows: `choco install ffmpeg`
    - Using homebrew for macOS `brew install ffmpeg`
- Navigate to `backend/llm` in your shell/terminal
- Install all the necessary python libraries using `pip install -r requirements.txt`
- Run `main.py`

## Features completed so far (Sprint 1)

- **Speech-to-Text (STT)**: The VA can understand and process user voice commands.
- **Text-to-Speech (TTS)**: Reads out health-related information back to the user in a clear, natural tone.
- **Short, Concise Responses**: Provides brief, accurate responses to user queries.
- **Clarification Handling**: Requests clarification when user input is complex or unclear.
- **Voice Interaction Deletion**: Allows users to delete saved voice interactions to ensure privacy.
- **Backend Setup**: Established the backend architecture to handle voice input processing and data management.
- **App Development Setup**: Initial setup of the app interface and integration with the VA.
- **LLM Integration Testing**: Conducted integration tests for the large language model to ensure accurate conversation flow.
- **User Interaction Logs**: Captures logs of individual user interactions for review and improvement.
- **End-of-Conversation Detection**: Detects when a conversation has naturally ended and disengages to ensure a smooth user experience.

## Features completed so far (Sprint 2)

- **Reminder for appointments**: The user is now able to set reminder for appointments with the help of voice assistant.
- **Reminder for checking BP**: The user can now set reminders for checking his BP with the help of voice assistant.
- **Reminder for medication**: The user can now set reminders for taking medication with the help of voice assistant.
- **Timesense**: The voice assistant now has a sense of what time it was yesterday, what time it is today and it remembers where we last left off our conversation.
- **CI/CD set up**: Completed CI/CD setup leveraging Github Actions. For every pull request raised to main branch, it now triggers workflows to run all tests of the repository.
- **Login & sign up functionality**: `authz` service has been added which now supports user login and signup.
- **Authorization**:  `authz` service also exposes endpoints to be used by `storage` service to check for requesting user permissions before granting access to resources in the database. This is a requirement for HIPAA compliant storage system.

### Demos

- Video demonstration of completed features: [Drive Link](https://drive.google.com/drive/u/0/folders/13SrXH7Rgg0j0vdOqyGlyub7U1ZGvrnYm)
