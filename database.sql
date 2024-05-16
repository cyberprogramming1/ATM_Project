CREATE DATABASE ATMDB;
USE ATMDB;

CREATE TABLE Users (
    id INT PRIMARY KEY IDENTITY(1,1),
    username NVARCHAR(50) UNIQUE NOT NULL,
    pin NVARCHAR(4) NOT NULL
);

CREATE TABLE Accounts (
    user_id INT FOREIGN KEY REFERENCES Users(id),
    balance DECIMAL(10, 2) NOT NULL DEFAULT 0
);

CREATE TABLE Transactions (
    id INT PRIMARY KEY IDENTITY(1,1),
    user_id INT FOREIGN KEY REFERENCES Users(id),
    transaction_type NVARCHAR(50),
    amount DECIMAL(10, 2),
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

select * from Users;
select * from Accounts;
select * from Transactions;

delete Users;
delete Accounts;
delete Transactions;





DBCC CHECKIDENT ('Users', RESEED, 0);
DBCC CHECKIDENT ('Accounts', RESEED, 0);
DBCC CHECKIDENT ('Transactions', RESEED, 0);