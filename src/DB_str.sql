CREATE TABLE transactions (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    date CHAR(16),
    total FLOAT,
    receipt_ID CHAR(9),
    receipt_file_name CHAR(21)
);

CREATE TABLE articles (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    transaction_ID INT,
    amount FLOAT,
    tax INT,
    description CHAR(64),
    FOREIGN KEY (transaction_ID) REFERENCES transactions(ID)
);