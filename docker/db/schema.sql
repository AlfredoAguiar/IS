-- Customer Table
CREATE TABLE Customer (
    Customer_ID INT PRIMARY KEY AUTO_INCREMENT,
    Customer_Name VARCHAR(255) NOT NULL,
    Customer_Category VARCHAR(255) NOT NULL
);

-- Transaction Table
CREATE TABLE Transaction (
    Transaction_ID INT PRIMARY KEY,
    Customer_ID INT,
    Date DATETIME NOT NULL,
    Payment_Method VARCHAR(255) NOT NULL,
    Store_Type VARCHAR(255) NOT NULL,
    Discount_Applied BOOLEAN NOT NULL,
    Season VARCHAR(255) NOT NULL,
    Promotion VARCHAR(255),
    FOREIGN KEY (Customer_ID) REFERENCES Customer(Customer_ID)
);

-- Product Table
CREATE TABLE Product (
    Product_ID INT PRIMARY KEY AUTO_INCREMENT,
    Transaction_ID INT,
    Name VARCHAR(255) NOT NULL,
    Total_Items INT NOT NULL,
    Total_Cost DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (Transaction_ID) REFERENCES Transaction(Transaction_ID)
);

-- Local Table
CREATE TABLE Local (
    Local_ID INT PRIMARY KEY AUTO_INCREMENT,
    Transaction_ID INT,
    City VARCHAR(255) NOT NULL,
    Latitude DECIMAL(9, 6) NOT NULL,
    Longitude DECIMAL(9, 6) NOT NULL,
    FOREIGN KEY (Transaction_ID) REFERENCES Transaction(Transaction_ID)
);
