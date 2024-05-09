package main

import (
	"log"
	"net/http"
	"github.com/gin-gonic/gin"
)

func main() {
	server := gin.Default()
	server.Static("/app/assets", "./assets")
	server.LoadHTMLGlob("./*.html")

	//Endpoints
	server.GET("/admin", admin)

	err := server.Run(":8888")
	if err != nil {
		log.Fatal(err)
	}

}

func admin(c *gin.Context) {
	c.HTML(http.StatusOK, "main.html", nil)
}
