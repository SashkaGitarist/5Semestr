
def MP_automatic(G1,rul1):
    P = []
    P.append('q')
    P.append(G1[1])
    m1 = set(G1[0])
    m2 = set(G1[1])
    P.append(m1.union(m2))
    P.append(P[0])
    P.append(G1[0][0])
    P.append(None)
    rules = []
    k = 0
    for i in rul1:
        if i[0] in G1[0]:
            for j in i[1:]:
                if j == '|':
                    continue
                else:
                    rules.append([(P[0],'e', i[0]),(P[0],j)])
    for i in G1[1]:
        rules.append([(P[0],i,i),(P[0],'e')])
    print('Автомат:')
    print(P)
    print('Правила:')
    for i in rules:
        print('{0} = {1}'.format(i[0],i[1]))


if __name__ == '__main__':
    print('Обычные КС-грамматики')
    print('1)')
    G = [['S'],[0,1],'P','S']
    rul = [['S','0S1','|','e']]
    MP_automatic(G,rul)
    print()
    print('2)')
    G = [['S'], ['a','b','c'], 'P', 'S']
    rul = [['S', 'aSbS','|','aS','|','e']]
    MP_automatic(G, rul)
    print()
    print('3)')
    G = [['S','R','T','X','Y'], ['a', 'b', 'p','q','y'], 'P', 'S']
    rul = [['S', 'R','|','T'], ['R', 'pX','|','paR','|','paT','|','e'],['T', 'Tg','|','g'],['X', 'aXb'],['Y', 'aYa','|','y']]
    MP_automatic(G, rul)
    print()
    print('Грамматики в нормальной форме Хомского')
    print('1)')
    G = [['S','A'],[0,1],'P','S']
    rul = [['S','SS','|','1A0','|','10'],['A','1A0','|','10']]
    MP_automatic(G,rul)
    print()
    print('2)')
    G = [['S','A','B','R'], ['a', 'b'], 'P', 'S']
    rul = [['S', 'RR', '|', 'AB'], ['R', 'RR', '|', 'AB'], ['B', 'RB', '|', 'b'],['A', 'a',]]
    MP_automatic(G, rul)
    print()
    print('3)')
    G = [['S', 'D', 'C', 'U','A','B'], ['a', 'b'], 'P', 'S']
    rul = [['S', 'e', '|', 'AD'], ['D', 'UC', '|', 'BU', '|', 'b'], ['C', 'BU', '|', 'b'], ['U', 'BA', '|', 'AD'],['A', 'a',],['B', 'b',]]
    MP_automatic(G, rul)
    print()