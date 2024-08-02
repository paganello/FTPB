CREATE TABLE transaction (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    date DATETIME NOT NULL,
    total FLOAT NULL,
    receipt_ID CHAR(9) NULL,
    receipt_file_name CHAR(23) NULL
);

CREATE TABLE good (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    transaction_ID INT,
    amount FLOAT NULL,
    tax INT NULL,
    description CHAR(64) NULL,
    FOREIGN KEY (transaction_ID) REFERENCES transaction(ID)
);

CREATE TABLE store (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    transaction_ID INT,
    name CHAR(64) NULL,
    address CHAR(64) NULL,
    city CHAR(64) NULL,
    VAT CHAR(16) NULL,
    FOREIGN KEY (transaction_ID) REFERENCES transaction(ID)
);