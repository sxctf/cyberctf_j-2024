package main

import (
	"database/sql"
	"fmt"
	"log"
	"net/http"
	"os"
	"regexp"
	"github.com/gin-gonic/gin"
	"github.com/go-sql-driver/mysql"
)

func main() {
	server := gin.Default()
	server.Static("/assets", "./assets")
	server.LoadHTMLGlob("templates/*.html")

	//Endpoints
	server.GET("/", mainpage)
	server.GET("/login", loginpage)
	server.POST("/login", loginpagecheck)
	server.GET("/myhiddenpath", adminpage)
	err := server.Run(":8080")
	if err != nil {
		log.Fatal(err)
	}

}




type users struct {
	id       int
	username string
	password string
}

func dbconn() bool {
	// Capture connection properties.
	cfg := mysql.Config{
		User:   os.Getenv("DBUSER"),
		Passwd: os.Getenv("DBPASS"),
		Net:    "tcp",
		Addr:   "mysql-db:3306",
		DBName: "polzovateli",
	}


	// Get a database handle.
	var err error
	db, err := sql.Open("mysql", cfg.FormatDSN())
	if err != nil {
		log.Fatal(err)
	}

	pingErr := db.Ping()
	if pingErr != nil {
		log.Fatal(pingErr)
		return false
	}
	fmt.Println("Connected!")
	return true
}

func check(username string, password string) string {
	cfg := mysql.Config{
		User:   os.Getenv("DBUSER"),
		Passwd: os.Getenv("DBPASS"),
		Net:    "tcp",
		Addr:   "mysql-db:3306",
		DBName: "polzovateli",
	}
	var err error
	db, err := sql.Open("mysql", cfg.FormatDSN())
	defer db.Close()
	if err != nil {
		log.Fatal(err)
	}

	var u users
	if err := db.QueryRow(fmt.Sprintf("SELECT * FROM uchetki WHERE username = '%s' AND password = '%s';", username, password)).Scan(&u.id, &u.username, &u.password); err != nil {
		fmt.Println("QUERY:", err)
		
		file, fail := os.OpenFile("app.log", os.O_CREATE|os.O_WRONLY|os.O_APPEND, 0666)
		if fail != nil {
			log.Fatal("Failed to open log file:", fail)
		}	
		log.SetOutput(file)

		if err == sql.ErrNoRows {
			log.Println("sql.ErrNoRows", err)
			return "No Rows returned"
		}
		log.Println("Invalid query", err)
		return "Invalid query"
	}
	return u.password
}

// API fucntions
func mainpage(c *gin.Context) {
	c.HTML(http.StatusOK, "index.html", nil)
}

func loginpage(c *gin.Context) {
	c.HTML(http.StatusOK, "login.html", nil)
}

func loginpagecheck(c *gin.Context) {

	err := c.Request.ParseForm()
	if err != nil {
		return
	}

	re := regexp.MustCompile(`\+|\;| |--|-- -`)

	username := c.Request.Form.Get("username")
	password := c.Request.Form.Get("password")

	username = re.ReplaceAllString(username, "cTf")
	
	if dbconn() == true {
		if password == check(username, password) {
			c.Redirect(http.StatusFound, "/static-spd/")
		} else {
			// c.IndentedJSON(http.StatusOK, "Sorry, invalid username or password, but I remember table name: uchetki")
			c.HTML(http.StatusOK, "error.html", nil)
		}
	}
	
}

func adminpage(c *gin.Context){
	c.HTML(http.StatusOK, "admin.html", nil)
}
