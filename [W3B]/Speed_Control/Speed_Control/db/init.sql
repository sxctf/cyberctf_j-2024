CREATE DATABASE IF NOT EXISTS polzovateli;
USE polzovateli;

CREATE TABLE IF NOT EXISTS uchetki (
    id INT NOT NULL AUTO_INCREMENT, 
    username VARCHAR(30) UNIQUE NOT NULL,
    password VARCHAR(30) UNIQUE NOT NULL,
    PRIMARY KEY (id));

INSERT INTO uchetki (username, password) VALUES ("admin", "I0rVBBpZHSFxR24g");


CREATE USER 'mysqldbuser'@'%' IDENTIFIED BY 'mysqldbuser$123654';
GRANT ALL PRIVILEGES ON *.* TO 'mysqldbuser'@'%' WITH GRANT OPTION;
FLUSH PRIVILEGES;





