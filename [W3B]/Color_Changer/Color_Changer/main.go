package main

import (

	"log"
	"net/http"
	"github.com/gin-gonic/gin"
)

func main() {
	server := gin.Default()
	server.Static("/assets", "./assets")
	server.LoadHTMLGlob("templates/*.html")
	
	//Endpoints
	server.GET("/", mainpage)
	err := server.Run(":8080")
	if err != nil{
		log.Fatal(err)
	}

}

func mainpage(c *gin.Context){
	c.HTML(http.StatusOK, "index.html", nil)
}
