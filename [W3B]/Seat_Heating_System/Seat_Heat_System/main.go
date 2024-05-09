package main

import (
	"fmt"
	"github.com/gin-gonic/gin"
	"io"
	"net/http"
	"regexp"
)

func main() {
	server := gin.Default()
	server.Static("/app/assets", "./assets")
	server.LoadHTMLGlob("/app/templates/*.html")

	//Endpoints
	server.GET("/", mainpage)
	server.GET("/robots.txt", robot)
	server.GET("/my-admin-panel", admin)
	server.GET("/my-admin-panel/also-my-admin-panel", admin2)
	server.POST("/my-admin-panel/also-my-admin-panel", ssrf)

	err := server.Run(":8080")
	if err != nil {
		fmt.Println(err)
	}
}

func mainpage(c *gin.Context) {
	c.HTML(http.StatusOK, "index.html", nil)
}

func robot(c *gin.Context) {
	c.JSON(200, gin.H{
		"message": "User-Agent: *\n Disallow: /my-admin-panel",
	})
}

func admin(c *gin.Context) {
	c.HTML(http.StatusOK, "newpanel.html", nil)
}

func admin2(c *gin.Context) {
	c.HTML(http.StatusOK, "newpanel2.html", nil)
}

func ssrf(c *gin.Context) {
	url := c.Request.FormValue("page")
	req := url
	fmt.Println(req)
	rgx, _ := regexp.MatchString("http://localhost/*", req)
	if req == "http://localhost/admin" {
		resp, err := http.Get("http://192.168.0.6:8888/admin")
		if err != nil {
			fmt.Println(err)
		}
		bodyB, _ := io.ReadAll(resp.Body)
		c.Data(http.StatusOK, "text/html, charset=utf-8", bodyB)

	} else if rgx && req != "http://localhost/admin" {

		c.JSON(404,gin.H{"code": "PAGE_NOT_FOUND", "message": "Page not found"})

	} else {
		resp, err := http.Get(req)
		if err != nil {
			fmt.Println(err)
		}

		bodyB, _ := io.ReadAll(resp.Body)
		c.Data(http.StatusOK, "text/html, charset=utf-8", bodyB)
	}
}
