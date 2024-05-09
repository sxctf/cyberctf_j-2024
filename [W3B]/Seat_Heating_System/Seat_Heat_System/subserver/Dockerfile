FROM golang:1.22.0-alpine3.19 AS builder

WORKDIR /app/subserver
# RUN go mod download && go mod verify 
RUN rm -rf /var/lib/apt/lists/*
COPY . ./
RUN go build -o secondtask-subserver ./local.go

CMD ["./secondtask-subserver"]
