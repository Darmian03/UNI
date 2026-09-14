CREATE DATABASE test;

USE test;

CREATE TABLE Product (
	maker CHAR(1),
	model CHAR(4),
	type VARCHAR(7)
);

CREATE TABLE Printer (
	code INT,
	model CHAR(4),
	color CHAR(1) DEFAULT 'n' CHECK (color IN ('y', 'n')),
	price DECIMAL(10, 2)
);

CREATE TABLE Classes (
	class VARCHAR(50),
	type CHAR(2)
);

INSERT INTO Product
VALUES ('A', '2101', 'Laptop'),
	   ('A', '3101', 'Printer'),
	   ('B', '1201', 'PC'),
	   ('C', '3302', 'Printer'),
	   ('C', '3303', 'Printer');

INSERT INTO Printer
VALUES (1, '3101', 'n', 90.00),
	   (2, '3302', 'y', 100.00),
	   (3, '3303', DEFAULT, NULL);

ALTER TABLE Classes
ADD bore FLOAT;

ALTER TABLE Printer
DROP COLUMN price;

DROP TABLE Product;
DROP TABLE Printer;
DROP TABLE Classes;

DROP DATABASE test;