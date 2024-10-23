CREATE DATABASE task6_db;
USE task6_db;

CREATE TABLE person (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    is_employed BOOLEAN NOT NULL
);

CREATE TABLE address (
    id INT AUTO_INCREMENT PRIMARY KEY,
    street VARCHAR(255) NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(50) NOT NULL,
    person_id INT,
    FOREIGN KEY (person_id) REFERENCES person(id)
);