CREATE TABLE transaction (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    date CHAR(16),
    total FLOAT,
    receipt_ID CHAR(9),
    receipt_file_name CHAR(21)
);

CREATE TABLE good (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    transaction_ID INT,
    amount FLOAT,
    tax INT,
    description CHAR(64),
    FOREIGN KEY (transaction_ID) REFERENCES transaction(ID)
);

CREATE TABLE store (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    transaction_ID INT,
    name CHAR(64),
    address CHAR(64),
    city CHAR(64),
    VAT CHAR(9),
    FOREIGN KEY (transaction_ID) REFERENCES transaction(ID)
);