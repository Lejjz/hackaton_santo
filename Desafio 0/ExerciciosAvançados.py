# Exercicio 2

from itertools import chain, combinations
from itertools import combinations


def menor_diferenca_absoluta(arr, allow_duplicates=True, sorted_pairs=True, unique_pairs=True):
    arr.sort()

    menor_diferenca = float('inf')
    pares_resultantes = []

    for (i, num1), (j, num2) in combinations(enumerate(arr), 2):
        if not allow_duplicates and num1 == num2:
            continue

        diferenca = abs(num2 - num1)

        if diferenca < menor_diferenca:
            menor_diferenca = diferenca
            pares_resultantes = [(num1, num2)]
        elif diferenca == menor_diferenca:
            if unique_pairs:
                if (num2, num1) not in pares_resultantes:
                    pares_resultantes.append((num1, num2))
            else:
                pares_resultantes.append((num1, num2))

    if sorted_pairs:
        pares_resultantes.sort()

    return pares_resultantes


entrada = input("Digite os números do array separados por espaço: ")

array = list(map(int, entrada.split()))

resultado = menor_diferenca_absoluta(
    array, allow_duplicates=False, sorted_pairs=True, unique_pairs=True)

print(resultado)


# Exercicio 3


def todos_subconjuntos(conjunto, max_size=None, min_size=0, distinct_only=True, sort_subsets=True):
    if distinct_only:
        conjunto = list(set(conjunto))

    subconjuntos = list(chain.from_iterable(combinations(conjunto, r)
                        for r in range(len(conjunto) + 1)))

    if min_size > 0 or max_size is not None:
        subconjuntos = [sub for sub in subconjuntos if (min_size <= len(
            sub) <= (max_size if max_size is not None else len(conjunto)))]

    if sort_subsets:
        subconjuntos = [tuple(sorted(sub)) for sub in subconjuntos]
        subconjuntos.sort()

    return subconjuntos


entrada = input("Digite os números do conjunto separados por espaço: ")

conjunto = list(map(int, entrada.split()))

max_size = int(input(
    "Digite o tamanho máximo dos subconjuntos (ou deixe em branco para nenhum limite): ") or 0) or None
min_size = int(input(
    "Digite o tamanho mínimo dos subconjuntos (ou deixe em branco para nenhum limite): ") or 0)
distinct_only = input(
    "Permitir elementos duplicados nos subconjuntos? (s/n): ").strip().lower() == 'n'
sort_subsets = input(
    "Ordenar os subconjuntos e elementos? (s/n): ").strip().lower() == 's'

resultado = todos_subconjuntos(conjunto, max_size=max_size, min_size=min_size,
                               distinct_only=distinct_only, sort_subsets=sort_subsets)

print(resultado)
