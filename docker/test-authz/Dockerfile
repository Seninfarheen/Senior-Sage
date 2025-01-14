FROM golang:1.23


WORKDIR /app

RUN go install github.com/matryer/moq@latest
COPY go.mod go.sum ./
RUN go mod download && go mod verify

COPY . .
RUN go generate ./...


CMD ["go", "test", "./..."]