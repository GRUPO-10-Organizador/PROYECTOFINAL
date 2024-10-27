CREATE DATABASE broker;
USE broker;

#tabla usuario

CREATE TABLE Usuario (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    saldo DECIMAL(15, 2) DEFAULT 0.00
);


CREATE TABLE Empresa (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(50) NOT NULL,
    sector VARCHAR(50),
    pais VARCHAR(50)
);

CREATE TABLE Accion (
    id INT PRIMARY KEY AUTO_INCREMENT,
    simbolo VARCHAR(10) NOT NULL UNIQUE,
    nombre VARCHAR(50) NOT NULL,
    precio_actual DECIMAL(10, 2) NOT NULL,
    empresa_id INT,
    FOREIGN KEY (empresa_id) REFERENCES Empresa(id)
);

CREATE TABLE Operacion (
    id INT PRIMARY KEY AUTO_INCREMENT,
    usuario_id INT,
    accion_id INT,
    tipo ENUM('compra', 'venta') NOT NULL,
    cantidad INT NOT NULL,
    precio_unitario DECIMAL(10, 2) NOT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES Usuario(id),
    FOREIGN KEY (accion_id) REFERENCES Accion(id)
);

CREATE TABLE Portafolio (
    id INT PRIMARY KEY AUTO_INCREMENT,
    usuario_id INT,
    accion_id INT,
    cantidad INT NOT NULL DEFAULT 0,
    FOREIGN KEY (usuario_id) REFERENCES Usuario(id),
    FOREIGN KEY (accion_id) REFERENCES Accion(id)
);


