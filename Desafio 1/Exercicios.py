import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

# Carrega as variáveis do arquivo .env
load_dotenv()

# Obtém as variáveis do ambiente
db_host = os.getenv('DB_HOST')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')

# Verifica se todas as variáveis foram carregadas corretamente
if not all([db_host, db_user, db_password, db_name]):
    print("Erro: Certifique-se de que todas as variáveis de ambiente estão definidas no arquivo .env.")
else:
    # Cria a string de conexão usando o host especificado
    connection_string = f"mysql+mysqlconnector://{
        db_user}:{db_password}@{db_host}/{db_name}"

    # Cria a engine do SQLAlchemy
    engine = create_engine(connection_string)

    try:
        # Verifica se a conexão é bem-sucedida
        with engine.connect() as connection:
            # Usar a instrução SQL para obter o nome do banco de dados
            result = connection.execute(text("SELECT DATABASE()"))
            database_name = result.scalar()  # Obtém o resultado da consulta
            print(f"Conectado ao banco de dados: {database_name}")
        print("Conexão com o banco de dados foi bem-sucedida!")
    except Exception as e:
        print(f"Falha na conexão com o banco de dados: {e}")

    # Caminho para a pasta onde os arquivos CSV estão localizados
    caminho_dataset = r'\Desafio 1\dataset'

    # Verifica se o caminho da pasta é correto
    if not os.path.exists(caminho_dataset):
        print(f"O caminho '{caminho_dataset}' não foi encontrado.")
    else:
        print("Pasta encontrada, carregando dados...")

        # Função para formatar o AnnualIncome
        def format_income(income):
            return float(income.replace('$', '').replace(',', ''))

        # Função para ajustar o formato da data
        def adjust_date_format(df, date_column, date_format):
            df[date_column] = pd.to_datetime(
                df[date_column], format=date_format, errors='coerce').dt.strftime('%Y-%m-%d')
            return df

        # Função para carregar dados de CSV para tabela
        def load_data_to_table(csv_file, table_name, converters=None, encoding='ISO-8859-1', date_col=None, date_format=None):
            try:
                df = pd.read_csv(
                    csv_file, converters=converters, encoding=encoding)
                if date_col and date_format:
                    df = adjust_date_format(df, date_col, date_format)
                df.to_sql(table_name, con=engine,
                          if_exists='replace', index=False)
                print(f"")
            except Exception as e:
                print(f"Erro ao inserir dados na tabela {table_name}: {e}")

        # Função para verificar a integridade dos dados antes da inserção
        def check_data_integrity(df, table_name, key_column):
            with engine.connect() as connection:
                existing_keys = connection.execute(
                    text(f"SELECT DISTINCT {key_column} FROM {table_name}")).fetchall()
                existing_keys = set(row[0] for row in existing_keys)
                missing_keys = df[key_column].dropna().unique()
                missing_keys = set(missing_keys) - existing_keys
                if missing_keys:
                    print(f"Chaves ausentes na tabela {
                          table_name}: {missing_keys}")
                    return False
            return True

        # Carregar e inserir os dados de cada arquivo CSV
        try:
            load_data_to_table(f'{caminho_dataset}/AdventureWorks_Customers.csv',
                               'customers', converters={'AnnualIncome': format_income})
            load_data_to_table(
                f'{caminho_dataset}/AdventureWorks_Product_Categories.csv', 'product_categories')
            load_data_to_table(
                f'{caminho_dataset}/AdventureWorks_Product_Subcategories.csv', 'product_subcategory')
            load_data_to_table(
                f'{caminho_dataset}/AdventureWorks_Products.csv', 'products')

            # Verificar dados antes de inserir na tabela returnss
            df_returnss = pd.read_csv(
                f'{caminho_dataset}/AdventureWorks_Returns.csv', encoding='ISO-8859-1')
            df_returnss = adjust_date_format(
                df_returnss, 'ReturnDate', '%m/%d/%Y')

            # Verificar a integridade dos dados antes da inserção
            if check_data_integrity(df_returnss, 'products', 'ProductKey'):
                load_data_to_table(
                    f'{caminho_dataset}/AdventureWorks_Returns.csv', 'returnss', date_col='ReturnDate', date_format='%m/%d/%Y')

            load_data_to_table(
                f'{caminho_dataset}/AdventureWorks_Sales_2015.csv', 'sales_2015')
            load_data_to_table(
                f'{caminho_dataset}/AdventureWorks_Sales_2016.csv', 'sales_2016')
            load_data_to_table(
                f'{caminho_dataset}/AdventureWorks_Sales_2017.csv', 'sales_2017')
            load_data_to_table(
                f'{caminho_dataset}/AdventureWorks_Territories.csv', 'territories')

            # Convertendo e carregando o arquivo de calendário
            df_calendar = pd.read_csv(
                f'{caminho_dataset}/AdventureWorks_Calendar.csv', encoding='ISO-8859-1')
            df_calendar = adjust_date_format(df_calendar, 'Date', '%m/%d/%Y')
            df_calendar.to_sql('calendar', con=engine,
                               if_exists='replace', index=False)
            print("")
        except Exception as e:
            print(f"Erro ao inserir dados: {e}")

        # Carregar dados das tabelas em DataFrames
        '''try:
            df_customers = pd.read_sql("SELECT * FROM customers", engine)
            df_product_categories = pd.read_sql(
                "SELECT * FROM product_categories", engine)
            df_product_subcategory = pd.read_sql(
                "SELECT * FROM product_subcategory", engine)
            df_products = pd.read_sql("SELECT * FROM products", engine)
            df_returnss = pd.read_sql("SELECT * FROM returnss", engine)
            df_sales_2015 = pd.read_sql("SELECT * FROM sales_2015", engine)
            df_sales_2016 = pd.read_sql("SELECT * FROM sales_2016", engine)
            df_sales_2017 = pd.read_sql("SELECT * FROM sales_2017", engine)
            df_territories = pd.read_sql("SELECT * FROM territories", engine)

            # Exibir as primeiras linhas de cada DataFrame para verificação
            print("Customers:\n", df_customers.head())
            print("Product Categories:\n", df_product_categories.head())
            print("Product Subcategory:\n", df_product_subcategory.head())
            print("Products:\n", df_products.head())
            print("Returnss:\n", df_returnss.head())
            print("Sales_2015:\n", df_sales_2015.head())
            print("Sales_2016:\n", df_sales_2016.head())
            print("Sales_2017:\n", df_sales_2017.head())
            print("Territories:\n", df_territories.head())
        except Exception as e:
            print(f"Erro ao carregar dados das tabelas: {e}")'''


# QUERIES

# Query 1
query = """
SELECT
    p.ProductName,
    SUM(s.OrderQuantity) AS TotalQuantitySold
FROM
    (
        SELECT
            OrderQuantity,
            ProductKey
        FROM Sales_2016

        UNION ALL

        SELECT
            OrderQuantity,
            ProductKey
        FROM Sales_2017
    ) s
JOIN
    Products p ON s.ProductKey = p.ProductKey
JOIN
    Product_Subcategory ps ON p.ProductSubCategoryKey = ps.ProductSubcategoryKey
JOIN
    Product_Categories pc ON ps.ProductCategoryKey = pc.ProductCategoryKey
WHERE
    pc.ProductCategoryKey = 1
GROUP BY
    p.ProductName
ORDER BY
    TotalQuantitySold DESC
LIMIT 10;
"""

# Executar a query
with engine.connect() as connection:
    result = connection.execute(text(query))
    top_products = result.fetchall()

print("Query 1 - Quais são os 10 produtos mais vendidos (em quantidade) na categoria 'Bicicletas', considerando apenas vendas feitas nos últimos dois anos?")

# Exibir resultados
for row in top_products:
    product_name, quantity_sold = row
    # Converter Decimal para int
    quantity_sold = int(quantity_sold)
    print(f"Produto: {product_name}, Quantidade Vendida: {quantity_sold}")


# Query 2

query = """
    WITH Orders_Per_Quarter AS (
    SELECT 
        CustomerKey,
        QUARTER(STR_TO_DATE(OrderDate, '%m/%d/%Y')) AS Quarter,
        COUNT(*) AS OrdersInQuarter
    FROM 
        Sales_2017
    WHERE 
        STR_TO_DATE(OrderDate, '%m/%d/%Y') BETWEEN '2017-01-01' AND '2017-12-31'
    GROUP BY 
        CustomerKey,
        Quarter
),
Client_Orders_By_Quarter AS (
    SELECT 
        CustomerKey,
        Quarter,
        SUM(OrdersInQuarter) AS TotalOrdersInQuarter
    FROM 
        Orders_Per_Quarter
    GROUP BY 
        CustomerKey,
        Quarter
),
Max_Orders_Per_Quarter AS (
    SELECT 
        CustomerKey,
        MAX(TotalOrdersInQuarter) AS MaxOrdersInQuarter
    FROM 
        Client_Orders_By_Quarter
    GROUP BY 
        CustomerKey
),
Top_Client AS (
    SELECT 
        c.CustomerKey,
        CONCAT(c.FirstName, ' ', c.LastName) AS FullName,
        m.MaxOrdersInQuarter
    FROM 
        Max_Orders_Per_Quarter m
    JOIN 
        Customers c ON m.CustomerKey = c.CustomerKey
    ORDER BY 
        m.MaxOrdersInQuarter DESC
    LIMIT 1
)
SELECT 
    FullName,
    MaxOrdersInQuarter AS QuantityInTopQuarter
FROM 
    Top_Client;
    """

# Executar a query
with engine.connect() as connection:
    result = connection.execute(text(query))
    top_client = result.fetchall()

print("\nQuery 2 - Qual é o cliente que tem o maior número de pedidos realizados, considerando apenas clientes que fizeram pelo menos um pedido em cada trimestre do último ano fiscal?")

# Exibir resultados
for row in top_client:
    name, quantity = row
    print(f"Cliente: {name}, Quantidade no trimestre: {int(quantity)}")


# Query 3

query = """
    WITH MonthlySales AS (
        SELECT
            MONTH(STR_TO_DATE(s.OrderDate, '%m/%d/%Y')) AS Month,
            YEAR(STR_TO_DATE(s.OrderDate, '%m/%d/%Y')) AS Year,
            SUM(s.OrderQuantity * p.ProductPrice) AS TotalSales,
            AVG(s.OrderQuantity * p.ProductPrice) AS AverageSaleValue
        FROM (
            SELECT OrderDate, OrderQuantity, ProductKey FROM Sales_2015
            UNION ALL
            SELECT OrderDate, OrderQuantity, ProductKey FROM Sales_2016
            UNION ALL
            SELECT OrderDate, OrderQuantity, ProductKey FROM Sales_2017
        ) s
        JOIN Products p ON s.ProductKey = p.ProductKey
        GROUP BY
            YEAR(STR_TO_DATE(s.OrderDate, '%m/%d/%Y')),
            MONTH(STR_TO_DATE(s.OrderDate, '%m/%d/%Y'))
    )
    SELECT
        Month,
        SUM(TotalSales) AS TotalSales
    FROM
        MonthlySales
    WHERE
        AverageSaleValue > 500
    GROUP BY
        Month
    ORDER BY
        TotalSales DESC
    LIMIT 1;
    """

# Executar a query
with engine.connect() as connection:
    result = connection.execute(text(query))
    top_month_sales = result.fetchall()

print("\nQuery 3 - Em qual mês do ano ocorrem mais vendas (em valor total), considerando apenas os meses em que a receita média por venda foi superior a 500 unidades monetárias?")

# Exibir resultados
for row in top_month_sales:
    month, total_sales = row
    # Converter Decimal para float e arredondar para 2 casas decimais
    total_sales = round(float(total_sales), 2)
    print(f"Mês: {month}, Valor Total de Vendas: {total_sales:.2f}")


# Query 4

# Definir a consulta SQL corrigida
query = """
WITH Sales2016 AS (
    SELECT
        TerritoryKey,
        SUM(OrderQuantity * ProductPrice) AS TotalSales2016
    FROM
        Sales_2016 s
    JOIN Products p ON s.ProductKey = p.ProductKey
    GROUP BY
        TerritoryKey
),
Sales2017 AS (
    SELECT
        TerritoryKey,
        SUM(OrderQuantity * ProductPrice) AS TotalSales2017
    FROM
        Sales_2017 s
    JOIN Products p ON s.ProductKey = p.ProductKey
    GROUP BY
        TerritoryKey
),
AverageSales2017 AS (
    SELECT
        AVG(TotalSales2017) AS AvgSales2017
    FROM
        Sales2017
),
SalesGrowth AS (
    SELECT
        s2017.TerritoryKey,
        s2016.TotalSales2016,
        s2017.TotalSales2017,
        ((s2017.TotalSales2017 - s2016.TotalSales2016) / s2016.TotalSales2016) * 100 AS GrowthPercentage
    FROM
        Sales2016 s2016
    JOIN Sales2017 s2017 ON s2016.TerritoryKey = s2017.TerritoryKey
),
AboveAverageAndGrowth AS (
    SELECT
        sg.TerritoryKey,
        sg.TotalSales2017,
        sg.GrowthPercentage
    FROM
        SalesGrowth sg
    JOIN AverageSales2017 avg ON sg.TotalSales2017 > avg.AvgSales2017
    WHERE
        sg.GrowthPercentage > 10
)
SELECT
    aag.TerritoryKey,
    aag.TotalSales2017,
    aag.GrowthPercentage
FROM
    AboveAverageAndGrowth aag
ORDER BY
    aag.TotalSales2017 DESC;
"""

# Executar a query
with engine.connect() as connection:
    result = connection.execute(text(query))
    top_sellers = result.fetchall()

print("\nQuery 4 - Quais vendedores tiveram vendas com valor acima da média no último ano fiscal e também tiveram um crescimento de vendas superior a 10% em relação ao ano anterior?")

# Exibir resultados
for row in top_sellers:
    territory_key, total_sales, growth_percentage = row
    # Arredondar para 2 casas decimais
    total_sales = round(float(total_sales), 2)
    # Arredondar para 2 casas decimais
    growth_percentage = round(float(growth_percentage), 2)
    print(f"TerritoryKey: {territory_key}, TotalSales2017: {
          total_sales:.2f}, GrowthPercentage: {growth_percentage:.2f}%")


# Query Extra

# Definir a consulta SQL
query = """
WITH Sales2016 AS (
    SELECT
        s.ProductKey,
        SUM(s.OrderQuantity * p.ProductPrice) AS TotalSales2016
    FROM
        Sales_2016 s
    JOIN Products p ON s.ProductKey = p.ProductKey
    GROUP BY
        s.ProductKey
),
Sales2017 AS (
    SELECT
        s.ProductKey,
        SUM(s.OrderQuantity * p.ProductPrice) AS TotalSales2017
    FROM
        Sales_2017 s
    JOIN Products p ON s.ProductKey = p.ProductKey
    GROUP BY
        s.ProductKey
),
SalesGrowth AS (
    SELECT
        s2017.ProductKey AS ProductKey,
        p.ProductName,
        COALESCE(s2016.TotalSales2016, 0) AS TotalSales2016,
        s2017.TotalSales2017,
        ((s2017.TotalSales2017 - COALESCE(s2016.TotalSales2016, 0)) / COALESCE(s2016.TotalSales2016, 1)) * 100 AS GrowthPercentage
    FROM
        Sales2017 s2017
    LEFT JOIN Sales2016 s2016 ON s2017.ProductKey = s2016.ProductKey
    JOIN Products p ON s2017.ProductKey = p.ProductKey
)
SELECT
    ProductName,
    TotalSales2016,
    TotalSales2017,
    ROUND(GrowthPercentage, 2) AS GrowthPercentage
FROM
    SalesGrowth
ORDER BY
    GrowthPercentage DESC
LIMIT 5;
"""

# Executar a query
with engine.connect() as connection:
    result = connection.execute(text(query))
    top_growing_products = result.fetchall()

print("\nQuery Extra - Qual foi o crescimento percentual nas vendas por produto de um ano para o outro, e quais foram os 5 produtos com o maior crescimento percentual nas vendas entre os anos de 2016 e 2017?")

# Exibir resultados
for row in top_growing_products:
    product_name, total_sales_2016, total_sales_2017, growth_percentage = row
    total_sales_2016 = round(float(total_sales_2016), 2)
    total_sales_2017 = round(float(total_sales_2017), 2)
    growth_percentage = round(float(growth_percentage), 2)
    print(f"Produto: {product_name}, Total Sales 2016: {total_sales_2016:.2f}, Total Sales 2017: {
          total_sales_2017:.2f}, Growth Percentage: {growth_percentage:.2f}%")
