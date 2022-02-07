class Stack:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[len(self.items) - 1]

    def size(self):
        return len(self.items)

def csv_dict_reader(name):
    file = open(name, 'r')
    lines = file.readlines()
    arr = [list(map(str, lines[i].replace('\n', '').split(';'))) for i in range(len(lines))]
    file.close()
    step = {i[0]: i[1:] for i in arr[1:]}
    tmp = arr[0][0]
    begin = tmp[0]
    end = tmp[1]
    return step,begin,end


if __name__ == '__main__':
    step, begin, end = csv_dict_reader('lb63.csv')
    mp = Stack()
    str = '100100'
    mp.push('z')
    c = 0
    state = begin
    for nu in str:
        if state + nu + mp.peek() in step.keys():
            tt = step[state+nu+mp.peek()][0]
            state = tt[0]
            if tt[1:] == 'e':
                mp.pop()
            else:
                mp.pop()
                for i in tt[1:][::-1]:
                    mp.push(i)
        else:
            state = '10'
            break
    if state + 'e' + mp.peek() in step.keys():
        tt = step[state + 'e' + mp.peek()][0]
        state = tt[0]
        if tt[1:] == 'e':
            mp.pop()

    print(state)
    print(end)
    if state == end:
        print('Цепочка является допускающей')
    else:
        print('Цепочка не является допускающей')