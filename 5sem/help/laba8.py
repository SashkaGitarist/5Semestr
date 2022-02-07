import csv


def lex_tree(rul1, string1):
    p = len(string1)-1
    while p >= 0:
        kk = ''
        co = p
        for i in string1[p::-1]:
            m = p
            kk += i
            co -= 1
            for k in range(len(rul1)):
                j = rul1[k][1:]
                kk2 = kk
                kk = kk[::-1]
                if kk in j:
                    tree.insert(0, [rul1[k][0], '->', string1[co+1:m+1]])
                    string1[co+1:m+1] = rul1[k][0]
                    return string1
                kk = kk2
            for k in range(len(rul1)):
                j = rul1[k][1:]
                if i in j:
                    tree.insert(0, [rul1[k][0], '->', string1[co+1]])
                    string1[co+1] = rul1[k][0]
                    return string1
        p -= 1


def file_print(tree1):
    print('---Вывод в файл---')
    file = input("В какой файл вывести (укажите название без типа файла): ")
    dictlist = []
    outfile = open('{}.csv'.format(file), 'w', newline='')
    writer = csv.writer(outfile, delimiter=';', quotechar='"')
    for i in range(len(tree1)):
        dictlist.append(tree1[i][0])
        dictlist.append(tree1[i][1])
        for j in range(len(tree1[i][2])):
            dictlist.append(tree1[i][2][j])
        j = 0
        writer.writerow(dictlist)
        j += 1
        dictlist.clear()
    outfile.close()


if __name__ == '__main__':

    # G = [['S'], ['a', '+', '*'], 'P', 'S']
    # rul = [['S', 'a', '|', 'S+S', '|', 'S*S']]
    # string = 'a+a*a+a'

    # G = [['S', 'T'], ['a', '+', 'b'], 'P', 'S']
    # rul = [['S', 'T', '|', 'T+S'], ['T', 'a', '|', 'b']]
    # string = 'a+b+a'

    G = [['S'], ['(', ')', 'e'], 'P', 'S']
    rul = [['S', 'SS', '|', '(S)', '|', 'e']]
    string = '((e))(e)'

    f = 0
    for i in string:
        if i not in G[1]:
            f = 1
    if f == 0:
        tree = []
        s = list(string)
        if len(s) == 1:
            print('---Данная строка не является элементом данной КС-грамматики---')
            f = 1
        while len(s) != 1:
            s = lex_tree(rul, s)
            if s is None:
                print('---Данная строка не является элементом данной КС-грамматики---')
                f = 1
                break
        if f == 0:
            print('---Печатаем дерево разбора---')
            for i in range(len(tree)):
                print(tree[i])
            file_print(tree)
    else:
        print('---Некорректные символы в строке---')
