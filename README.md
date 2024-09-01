Tecnologias Utilizadas:


Python: Linguagem de programação utilizada para escrever o código.

Pandas: Biblioteca Python para manipulação e análise de dados.

SQLAlchemy: Biblioteca Python para trabalhar com bancos de dados SQL.

MySQL Connector: Driver para conectar o SQLAlchemy ao MySQL.

dotenv: Biblioteca Python para carregar variáveis de ambiente a partir de um arquivo .env.
(OBS: arquivo .env foi adicionado ao gitignore por questão de segurança)

SQL: Linguagem de consulta utilizada para criar e executar queries no banco de dados.


Passo a Passo do Código:

1. Configuração do Ambiente

Importação das Bibliotecas

Carregamento das Variáveis de Ambiente: O código carrega variáveis de ambiente de um arquivo .env usando a biblioteca dotenv. Essas variáveis incluem informações de conexão ao banco de dados.

Verificação das Variáveis de Ambiente: Verifica se todas as variáveis necessárias foram carregadas corretamente.


2. Conexão com o Banco de Dados

Criação da String de Conexão e Engine: Cria uma string de conexão para o banco de dados MySQL e uma engine do SQLAlchemy para se conectar ao banco de dados.

Teste de Conexão: Testa a conexão com o banco de dados e imprime o nome do banco de dados conectado.



3. Carregamento e Manipulação dos Dados

Verificação do Caminho do Dataset: Verifica se o caminho para os arquivos CSV está correto.

Funções de Manipulação de Dados: Define funções para formatar dados e carregar dados CSV em tabelas do banco de dados.

Verificação da Integridade dos Dados: Verifica a integridade dos dados antes da inserção, comparando chaves existentes com as chaves no arquivo CSV.

Carregamento dos Dados CSV: Carrega e insere os dados de vários arquivos CSV nas tabelas correspondentes do banco de dados.

4. Execução de Queries

Query 1: Produtos Mais Vendidos
Esta query visa identificar os 10 produtos mais vendidos na categoria 'Bicicletas' nos últimos dois anos (2016 e 2017). O objetivo é analisar as vendas de produtos específicos em uma categoria ao longo de um período.


Query 2: Cliente com o Maior Número de Pedidos
Esta query busca identificar o cliente com o maior número de pedidos realizados em cada trimestre do último ano fiscal (2017). O objetivo é encontrar o cliente mais ativo em termos de pedidos.

Query 3: Vendas Totais por Região
Esta query visa calcular o total de vendas por região para o ano de 2016, agrupando os resultados para fornecer uma visão geral das vendas em diferentes regiões.

Query 4: Receita Média por Categoria de Produto
Esta query calcula a receita média por categoria de produto, ajudando a entender a média de receita gerada por cada categoria.

Query Extra: Vendas por Dia da Semana
Esta query examina as vendas por dia da semana para 2017, proporcionando uma visão sobre quais dias da semana têm mais atividade de vendas.


5. Execução e Verificação

Após definir as queries SQL, você pode executá-las usando a engine do SQLAlchemy para obter e analisar os resultados. Isso envolve o uso de funções como engine.execute() e a manipulação dos resultados retornados.

Exemplo de Execução de Queries:


with engine.connect() as connection:
    result_1 = connection.execute(text(query_1)).fetchall()
    result_2 = connection.execute(text(query_2)).fetchall()

    print("Produtos Mais Vendidos:\n", result_1)
    print("Cliente com Maior Número de Pedidos:\n", result_2)

6. Visualização dos Dados
Após a execução das queries, os resultados podem ser visualizados e analisados usando bibliotecas como Matplotlib ou Seaborn, para criar gráficos e ajudar na interpretação dos dados.

Exemplo de Visualização:

import matplotlib.pyplot as plt
import seaborn as sns
