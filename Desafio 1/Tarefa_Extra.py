import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import seaborn as sns
import os

load_dotenv()

db_host = os.getenv('DB_HOST')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')

# Cria a string de conexão usando o host especificado
connection_string = f"mysql+mysqlconnector://{
    db_user}:{db_password}@{db_host}/{db_name}"

# Cria a engine do SQLAlchemy
engine = create_engine(connection_string)

# VISUALIZAÇÃO 1
query = """
WITH MonthlySales AS (
    SELECT
        DATE_FORMAT(STR_TO_DATE(s.OrderDate, '%m/%d/%Y'), '%Y-%m') AS MonthYear,
        SUM(s.OrderQuantity * p.ProductPrice) AS TotalSales
    FROM
        (
            SELECT OrderDate, OrderQuantity, ProductKey
            FROM Sales_2015
            UNION ALL
            SELECT OrderDate, OrderQuantity, ProductKey
            FROM Sales_2016
            UNION ALL
            SELECT OrderDate, OrderQuantity, ProductKey
            FROM Sales_2017
        ) s
    JOIN Products p ON s.ProductKey = p.ProductKey
    GROUP BY MonthYear
),
Trend AS (
    SELECT
        MonthYear,
        TotalSales,
        AVG(TotalSales) OVER (ORDER BY MonthYear ROWS BETWEEN 11 PRECEDING AND CURRENT ROW) AS TrendLine
    FROM MonthlySales
)
SELECT * FROM Trend
ORDER BY MonthYear;
"""

# Executar a consulta
with engine.connect() as connection:
    result = connection.execute(text(query))
    data = result.fetchall()

# Converter os resultados para um DataFrame
df = pd.DataFrame(data, columns=['MonthYear', 'TotalSales', 'TrendLine'])

# Verificar e limpar valores ausentes
df['MonthYear'] = pd.to_datetime(
    df['MonthYear'], format='%Y-%m', errors='coerce')
df = df.dropna(subset=['MonthYear'])  # Remove linhas onde MonthYear é NaT
df['TotalSales'] = df['TotalSales'].astype(float)
df['TrendLine'] = df['TrendLine'].astype(float)

# Criar o gráfico de linha
plt.figure(figsize=(12, 6))
plt.plot(df['MonthYear'], df['TotalSales'],
         label='Vendas Totais', color='blue', marker='o')
plt.plot(df['MonthYear'], df['TrendLine'],
         label='Linha de Tendência', color='red', linestyle='--')

# Destaque os meses de pico de vendas
max_sales = df['TotalSales'].max()
peak_months = df[df['TotalSales'] == max_sales]['MonthYear']
for month in peak_months:
    if pd.notna(month):  # Verifica se month não é NaT
        plt.axvline(x=month, color='green', linestyle=':',
                    label=f'Mês de Pico: {month.strftime("%Y-%m")}')

# Adicionar título e rótulos
plt.title('Tendência de Vendas Totais ao Longo do Tempo (Mensal)')
plt.xlabel('Mês/Ano')
plt.ylabel('Vendas Totais (em unidades monetárias)')
plt.xticks(rotation=45)
plt.legend()
plt.grid(True)

# Exibir o gráfico
plt.tight_layout()
plt.show()


# VISUALIZAÇÃO 2
query = """
WITH ProductSales AS (
    SELECT
        p.ProductName,
        SUM(s.OrderQuantity) AS TotalQuantitySold,
        SUM(s.OrderQuantity * p.ProductPrice) AS TotalProfit
    FROM
        (
            SELECT OrderQuantity, ProductKey
            FROM Sales_2015
            UNION ALL
            SELECT OrderQuantity, ProductKey
            FROM Sales_2016
            UNION ALL
            SELECT OrderQuantity, ProductKey
            FROM Sales_2017
        ) s
    JOIN Products p ON s.ProductKey = p.ProductKey
    JOIN Product_Subcategory ps ON p.ProductSubCategoryKey = ps.ProductSubCategoryKey
    JOIN Product_Categories pc ON ps.ProductCategoryKey = pc.ProductCategoryKey
    WHERE pc.ProductCategoryKey = 1  -- Categoria de "Bicicletas"
    GROUP BY p.ProductName
)
SELECT
    ProductName,
    TotalQuantitySold,
    TotalProfit
FROM
    ProductSales
ORDER BY
    TotalQuantitySold DESC
LIMIT 10;
"""

# Executar a consulta
with engine.connect() as connection:
    result = connection.execute(text(query))
    data = result.fetchall()

# Converter os resultados para um DataFrame
df = pd.DataFrame(data, columns=['ProductName',
                  'TotalQuantitySold', 'TotalProfit'])

# Criar o gráfico de barras
fig, ax1 = plt.subplots(figsize=(14, 8))

# Criar um gráfico de barras para a quantidade vendida
color = 'tab:blue'
ax1.set_xlabel('Produto')
ax1.set_ylabel('Quantidade Vendida', color=color)
bars1 = ax1.bar(df['ProductName'], df['TotalQuantitySold'],
                color=color, label='Quantidade Vendida')
ax1.tick_params(axis='y', labelcolor=color)
ax1.set_xticklabels(df['ProductName'], rotation=45, ha='right')

# Adicionar um eixo y secundário para o lucro
ax2 = ax1.twinx()
color = 'tab:green'
ax2.set_ylabel('Lucro Total (em unidades monetárias)', color=color)
bars2 = ax2.bar(df['ProductName'], df['TotalProfit'],
                color=color, alpha=0.5, label='Lucro Total')
ax2.tick_params(axis='y', labelcolor=color)

# Adicionar rótulos de valor nas barras
for bar in bars1:
    yval = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2.0, yval,
             int(yval), va='bottom', ha='center')

for bar in bars2:
    yval = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2.0, yval,
             f'{yval:.2f}', va='bottom', ha='center')

# Adicionar título e rótulos
plt.title('Top 10 Produtos Mais Vendidos na Categoria de Bicicletas')
fig.tight_layout()  # Ajustar layout para evitar sobreposição

# Exibir o gráfico
plt.show()


# VISUALIZAÇÃO 3

# Pergunta ao usuário pela categoria desejada
categorias_disponiveis = ['Bikes', 'Components', 'Clothing', 'Accessories']
print("Categorias disponíveis:", ', '.join(categorias_disponiveis))
categoria_selecionada = input("Digite a categoria desejada: ")

if categoria_selecionada not in categorias_disponiveis:
    print("Categoria inválida. Por favor, escolha uma das categorias disponíveis.")
else:
    # Query SQL ajustada com base na categoria selecionada
    query = f"""
    WITH MonthlySales AS (
        SELECT
            t.Region AS TerritoryName,
            DATE_FORMAT(STR_TO_DATE(s.OrderDate, '%m/%d/%Y'), '%Y-%m') AS Month,
            SUM(s.OrderQuantity * p.ProductPrice) AS TotalSales
        FROM
            (
                SELECT OrderDate, OrderQuantity, ProductKey, TerritoryKey
                FROM Sales_2015
                UNION ALL
                SELECT OrderDate, OrderQuantity, ProductKey, TerritoryKey
                FROM Sales_2016
                UNION ALL
                SELECT OrderDate, OrderQuantity, ProductKey, TerritoryKey
                FROM Sales_2017
            ) s
        JOIN Products p ON s.ProductKey = p.ProductKey
        JOIN Product_Subcategory ps ON p.ProductSubCategoryKey = ps.ProductSubCategoryKey
        JOIN Product_Categories pc ON ps.ProductCategoryKey = pc.ProductCategoryKey
        JOIN Territories t ON s.TerritoryKey = t.SalesTerritoryKey
        WHERE pc.CategoryName = '{categoria_selecionada}'
        GROUP BY t.Region, DATE_FORMAT(STR_TO_DATE(s.OrderDate, '%m/%d/%Y'), '%Y-%m')
    )
    SELECT
        TerritoryName,
        Month,
        TotalSales
    FROM
        MonthlySales
    ORDER BY
        TerritoryName, Month;
    """

    # Executa a query
    try:
        with engine.connect() as connection:
            result = connection.execute(text(query))
            df = pd.DataFrame(result.fetchall(), columns=result.keys())

            # Verifica se o DataFrame não está vazio
            if not df.empty:
                print("Dados da consulta SQL:")
                print(df.head())

                # Ajuste na conversão da data para o formato correto
                df['Month'] = pd.to_datetime(
                    df['Month'], format='%Y-%m', errors='coerce')

                # Verifica o conteúdo da coluna 'Month'
                print("Conteúdo da coluna 'Month':")
                print(df['Month'])

                # Remove linhas com valores nulos em 'Month'
                df = df.dropna(subset=['Month'])

                # Usando pd.pivot_table
                df_pivot = pd.pivot_table(
                    df,
                    index="TerritoryName",
                    columns="Month",
                    values="TotalSales",
                    fill_value=0  # Preenche valores ausentes com 0
                )

                # Função para formatar as anotações
                def format_annotation(val):
                    # Limitar a quantidade de anotações a 3 por região
                    if len(val) > 3:
                        # Exibe os 3 primeiros caracteres
                        return f'{val:.2f}'[:3]
                    return f'{val:.2f}'

                # Verifica o DataFrame pivotado
                print("DataFrame pivotado:")
                print(df_pivot.head())

                # Verifica se o DataFrame pivotado não está vazio
                if not df_pivot.empty:
                    plt.figure(figsize=(12, 8))
                    sns.heatmap(df_pivot,
                                cmap="YlGnBu",
                                annot=True,
                                fmt="",
                                # Tamanho e peso da fonte das anotações
                                annot_kws={"size": 8, "weight": 'bold'},
                                linewidths=.5,
                                cbar_kws={'label': 'Total Sales'})
                    plt.title(
                        f"Mapa de Calor das Vendas por Região e Mês - Categoria: {categoria_selecionada}")
                    plt.xlabel("Mês")
                    plt.ylabel("Região")
                    plt.xticks(rotation=45)
                    plt.yticks(rotation=0)
                    plt.show()
                else:
                    print("DataFrame pivotado está vazio. Não há dados para plotar.")
            else:
                print("DataFrame está vazio. Verifique a consulta SQL.")
    except Exception as e:
        print(f"Erro ao executar a query ou criar o mapa de calor: {e}")


# VISUALIZAÇÃO 4

# Função para criar o gráfico de dispersão com linha de regressão
def criar_grafico_dispersao():
    query = """
    SELECT
        c.CustomerKey AS CustomerID,
        COUNT(s.OrderNumber) AS NumeroVendas,
        SUM(s.OrderQuantity * p.ProductPrice) AS ValorTotalVendas
    FROM
        Sales_2015 s
    JOIN Products p ON s.ProductKey = p.ProductKey
    JOIN Customers c ON s.CustomerKey = c.CustomerKey
    GROUP BY
        c.CustomerKey
    UNION ALL
    SELECT
        c.CustomerKey AS CustomerID,
        COUNT(s.OrderNumber) AS NumeroVendas,
        SUM(s.OrderQuantity * p.ProductPrice) AS ValorTotalVendas
    FROM
        Sales_2016 s
    JOIN Products p ON s.ProductKey = p.ProductKey
    JOIN Customers c ON s.CustomerKey = c.CustomerKey
    GROUP BY
        c.CustomerKey
    UNION ALL
    SELECT
        c.CustomerKey AS CustomerID,
        COUNT(s.OrderNumber) AS NumeroVendas,
        SUM(s.OrderQuantity * p.ProductPrice) AS ValorTotalVendas
    FROM
        Sales_2017 s
    JOIN Products p ON s.ProductKey = p.ProductKey
    JOIN Customers c ON s.CustomerKey = c.CustomerKey
    GROUP BY
        c.CustomerKey;
    """

    try:
        with engine.connect() as connection:
            result = connection.execute(text(query))
            df = pd.DataFrame(result.fetchall(), columns=result.keys())

            # Verifica se o DataFrame não está vazio
            if not df.empty:
                print("Dados da consulta SQL:")
                print(df.head())

                # Cria o gráfico de dispersão com linha de regressão
                plt.figure(figsize=(12, 8))
                sns.regplot(x='NumeroVendas', y='ValorTotalVendas', data=df, scatter_kws={
                            's': 50}, line_kws={'color': 'red'})
                plt.title(
                    'Relação entre o Número de Vendas e o Valor Total das Vendas por Cliente')
                plt.xlabel('Número de Vendas')
                plt.ylabel('Valor Total das Vendas')
                plt.grid(True)
                plt.show()
            else:
                print("DataFrame está vazio. Verifique a consulta SQL.")
    except Exception as e:
        print(f"Erro ao executar a query ou criar o gráfico de dispersão: {e}")


# Executar a função
criar_grafico_dispersao()


# VISUALIZAÇÃO 5

# Função para criar o gráfico de barras empilhadas
def criar_grafico_barras_empilhadas(ano1, ano2):
    query = f"""
    WITH MonthlySales AS (
        SELECT
            DATE_FORMAT(STR_TO_DATE(s.OrderDate, '%m/%d/%Y'), '%Y-%m') AS Month,
            pc.CategoryName AS Category,
            SUM(s.OrderQuantity * p.ProductPrice) AS TotalSales,
            YEAR(STR_TO_DATE(s.OrderDate, '%m/%d/%Y')) AS Year
        FROM
            (
                SELECT OrderDate, OrderQuantity, ProductKey
                FROM Sales_{ano1}
                UNION ALL
                SELECT OrderDate, OrderQuantity, ProductKey
                FROM Sales_{ano2}
            ) s
        JOIN Products p ON s.ProductKey = p.ProductKey
        JOIN Product_Subcategory ps ON p.ProductSubCategoryKey = ps.ProductSubCategoryKey
        JOIN Product_Categories pc ON ps.ProductCategoryKey = pc.ProductCategoryKey
        GROUP BY
            DATE_FORMAT(STR_TO_DATE(s.OrderDate, '%m/%d/%Y'),
                        '%Y-%m'), pc.CategoryName, YEAR(STR_TO_DATE(s.OrderDate, '%m/%d/%Y'))
    )
    SELECT
        Month,
        Category,
        SUM(TotalSales) AS TotalSales,
        Year
    FROM
        MonthlySales
    WHERE
        Year IN ({ano1}, {ano2})
    GROUP BY
        Month, Category, Year
    ORDER BY
        Month, Category, Year;
    """

    try:
        with engine.connect() as connection:
            # Teste de consulta para verificação
            result = connection.execute(text(query))
            df = pd.DataFrame(result.fetchall(), columns=result.keys())

            # Verificação do DataFrame
            if not df.empty:
                print("Dados da consulta SQL:")
                print(df.head())

                # Pivotando o DataFrame para o gráfico de barras empilhadas
                df_pivot = pd.pivot_table(
                    df,
                    index='Month',
                    columns=['Year', 'Category'],
                    values='TotalSales',
                    fill_value=0
                )

                # Verifica o DataFrame pivotado
                print("DataFrame pivotado:")
                print(df_pivot.head())

                # Plotando o gráfico de barras empilhadas
                ax = df_pivot.plot(kind='bar', stacked=True, figsize=(14, 8))
                plt.title(f'Comparação das Vendas Mensais entre {
                          ano1} e {ano2}')
                plt.xlabel('Mês')
                plt.ylabel('Total de Vendas')
                plt.xticks(rotation=45)
                plt.legend(title='Ano e Categoria',
                           bbox_to_anchor=(1.05, 1), loc='upper left')
                plt.tight_layout()
                plt.show()
            else:
                print("DataFrame está vazio. Verifique a consulta SQL.")
    except Exception as e:
        print(
            f"Erro ao executar a query ou criar o gráfico de barras empilhadas: {e}")


# Executar a função para comparar 2016 e 2017
criar_grafico_barras_empilhadas(2016, 2017)
