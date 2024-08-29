# Exercicio 1


from itertools import chain, combinations


def gerar_asteriscos(n):
    lista_asteriscos = []

    for i in range(1, n + 1):
        lista_asteriscos.append('*' * i)

    return lista_asteriscos


n = int(input("Digite um número inteiro N: "))

resultado = gerar_asteriscos(n)

print(resultado)


# Exercicio 2


def menor_diferenca_absoluta(arr):
    arr.sort()

    menor_diferenca = float('inf')
    pares_resultantes = []

    for i in range(len(arr) - 1):
        diferenca = abs(arr[i + 1] - arr[i])

        if diferenca < menor_diferenca:
            menor_diferenca = diferenca
            pares_resultantes = [(arr[i], arr[i + 1])]
        elif diferenca == menor_diferenca:
            pares_resultantes.append((arr[i], arr[i + 1]))

    return pares_resultantes


entrada = input("Digite os números do array separados por espaço: ")

array = list(map(int, entrada.split()))

resultado = menor_diferenca_absoluta(array)

print(resultado)


# Exercicio 3


def todos_subconjuntos(conjunto):
    subconjuntos = list(chain.from_iterable(combinations(conjunto, r)
                        for r in range(len(conjunto) + 1)))
    return subconjuntos


entrada = input("Digite os números do conjunto separados por espaço: ")

conjunto = list(map(int, entrada.split()))

resultado = todos_subconjuntos(conjunto)

print(resultado)
