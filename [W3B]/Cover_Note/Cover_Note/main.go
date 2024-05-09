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
	server.GET("/robots.txt", robot)
	server.GET("/ctf{not-flag}", flagpage)

	err := server.Run(":8080")
	if err != nil {
		log.Fatal(err)
	}

}

// API fucntions
func mainpage(c *gin.Context) {
	c.HTML(http.StatusOK, "index.html", nil)
}

func robot(c *gin.Context){
	c.JSON(200, gin.H{
		"message": "User-Agent: *\n Disallow: /Y3Rme25vdC1mbGFnfQ==",
	})
}

func flagpage(c *gin.Context) {
	c.Writer.Header().Set("FLAG", "flag{loLKtbypAWimnD70}")
	c.HTML(http.StatusOK, "flag.html", nil)
}

