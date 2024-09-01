USE dataset_db;
                
CREATE TABLE Customers (
	CustomerKey INT,
    Prefix VARCHAR(255) NULL,
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50) NOT NULL,
    BirthDate DATE,
    MaritalStatus VARCHAR(20),
    Gender VARCHAR(10),
    EmailAddress VARCHAR(50),
    AnnualIncome FLOAT,
    TotalChildren INT,
    EducationLevel VARCHAR(50),
    Occupation VARCHAR(50),
    HomeOwner VARCHAR(5),
    PRIMARY KEY (CustomerKey)
);

CREATE TABLE Product_Categories (
	ProductCategoryKey INT,
    CategoryName VARCHAR(50),
    PRIMARY KEY (ProductCategoryKey)
);

CREATE TABLE Product_Subcategory (
	ProductSubcategoryKey INT,
    SubcategoryName VARCHAR(50),
    ProductCategoryKey INT,
    PRIMARY KEY (ProductSubcategoryKey),
    FOREIGN KEY (ProductCategoryKey) REFERENCES Product_Categories (ProductCategoryKey)
);

CREATE TABLE Products (
	ProductKey INT,
    ProductSubCategoryKey INT,
    ProductSKU VARCHAR(30),
    ProductName VARCHAR(100),
    ModelName VARCHAR(100),
    ProductDescription VARCHAR(500),
    ProductColor VARCHAR(50),
    ProductSize VARCHAR(10),
    ProductStyle VARCHAR(5),
    ProductCost FLOAT,
    ProductPrice FLOAT,
    PRIMARY KEY (ProductKey),
    FOREIGN KEY (ProductSubCategoryKey) REFERENCES Product_Subcategory (ProductSubCategoryKey)
);

CREATE TABLE returnss (
	ReturnDate DATE,
    TerritoryKey INT,
    ProductKey INT,
    ReturnQuantity INT,
    PRIMARY KEY (TerritoryKey),
    FOREIGN KEY (ProductKey) REFERENCES Products (ProductKey)
);

CREATE TABLE Sales_2015 (
	OrderDate DATE,
    StockDate DATE,
    OrderNumber VARCHAR(15),
    ProductKey INT,
    CustomerKey INT,
    TerritoryKey INT,
    OrderLineItem INT,
    OrderQuantity INT,
    FOREIGN KEY (ProductKey) REFERENCES Products (ProductKey),
    FOREIGN KEY (CustomerKey) REFERENCES Customers (CustomerKey),
    FOREIGN KEY (TerritoryKey) REFERENCES Returns (TerritoryKey)
);

CREATE TABLE Sales_2016 (
	OrderDate DATE,
    StockDate DATE,
    OrderNumber VARCHAR(15),
    ProductKey INT,
    CustomerKey INT,
    TerritoryKey INT,
    OrderLineItem INT,
    OrderQuantity INT,
    FOREIGN KEY (ProductKey) REFERENCES Products (ProductKey),
    FOREIGN KEY (CustomerKey) REFERENCES Customers (CustomerKey),
    FOREIGN KEY (TerritoryKey) REFERENCES Returns (TerritoryKey)
);

CREATE TABLE Sales_2017 (
	OrderDate DATE,
    StockDate DATE,
    OrderNumber VARCHAR(15),
    ProductKey INT,
    CustomerKey INT,
    TerritoryKey INT,
    OrderLineItem INT,
    OrderQuantity INT,
    FOREIGN KEY (ProductKey) REFERENCES Products (ProductKey),
    FOREIGN KEY (CustomerKey) REFERENCES Customers (CustomerKey),
    FOREIGN KEY (TerritoryKey) REFERENCES Returns (TerritoryKey)
);

CREATE TABLE Territories (
	SalesTerritoryKey INT,
    Region VARCHAR(50),
    Country VARCHAR(50),
    Continent VARCHAR(50),
    PRIMARY KEY (SalesTerritoryKey)
);






