def remove_outliets(n, lista):
        if not lista:
            return []
        if n < 0:
            return lista
        if n * 2 > len(lista):
            return lista

        sorted_list = sorted(lista)
        trimmed_list = sorted_list[n:-n]
        return trimmed_list

if __name__ == '__main__':
        lista = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        n = 2
        print(remove_outliets(n, lista))