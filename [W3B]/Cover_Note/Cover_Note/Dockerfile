FROM golang:1.22.0-alpine3.19 AS builder

WORKDIR /app

COPY go.mod ./
RUN go mod download && go mod verify 
RUN rm -rf /var/lib/apt/lists/*

COPY . ./

RUN go build -o fourthdTask ./main.go

EXPOSE 8004

CMD ["./fourthdTask"]
