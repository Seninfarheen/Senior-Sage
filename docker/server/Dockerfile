FROM golang:1.23 AS build

WORKDIR /app

# pre-copy/cache go.mod for pre-downloading dependencies and only redownloading them in subsequent builds if they change
COPY go.mod go.sum ./
RUN go mod download && go mod verify

COPY . .
# RUN go generate ./...
RUN go build -v -o server server.go


# copy build to final image
FROM golang:1.23

WORKDIR /app
COPY --from=build /app/server .

CMD ["./server"]
