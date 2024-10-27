CREATE DATABASE broker;
USE broker;

#tabla usuario

CREATE TABLE Usuario (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    saldo DECIMAL(15, 2) DEFAULT 0.00
);