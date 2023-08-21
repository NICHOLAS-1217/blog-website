CREATE DATABASE blogdb;

USE blogdb;

CREATE TABLE user(
    user_ID INT NOT NULL AUTO_INCREMENT,
    user_name VARCHAR(30),
    user_email VARCHAR(50) UNIQUE NOT NULL,
    user_password VARCHAR(30),
    PRIMARY KEY(user_ID)
);

CREATE TABLE post(
    post_ID INT NOT NULL AUTO_INCREMENT,
    post_title VARCHAR(1000),
    post_content VARCHAR(15000),
    user_ID INT NOT NULL,
    post_date VARCHAR(30),
    PRIMARY KEY(post_ID),
    FOREIGN KEY(user_ID) REFERENCES user(user_ID)
);

CREATE TABLE comment(
    comment_ID INT NOT NULL AUTO_INCREMENT,
    comment_content VARCHAR(15000),
    post_ID INT NOT NULL,
    user_ID INT NOT NULL,
    comment_date VARCHAR(30),
    PRIMARY KEY(comment_ID),
    FOREIGN KEY(user_ID) REFERENCES user(user_ID),
    FOREIGN KEY(post_ID) REFERENCES post(post_ID)
);

SELECT * FROM user;

SELECT * FROM post;

SELECT * FROM comment;

DROP TABLE user;

DROP TABLE post;

DROP TABLE comment;

DROP DATABASE blogdb;