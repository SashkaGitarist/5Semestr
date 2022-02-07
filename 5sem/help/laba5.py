import ast
def gen_dict(fn='test_dict.json'):
    import json
    import random

    test_dict = {}
    test_dict['type']='string4 dictionary for lab5'

    for i in range(0, random.randint(20, 80)):
        test_dict[i] = [j**2 for j in range(0, random.randint(0, 10))]
    test_dict['num_elements']=len(test_dict.keys())+1
    json.dump(test_dict, open(fn, 'w'))
    return test_dict, fn

def fix_types(result): ### if all keys are string-type, change it to int-type
    res = {}
    for k, v in result.items():
        if len(k) > 2: ### ad-hoc for a text-key
            res[k]=v
        else:
            res[int(k)]=v
    return res

td,pas = gen_dict()
json = open(pas, 'r', encoding='utf-8')
tmp = json.read()
tmp = tmp.replace('\n', ' ').replace('{','{ ').replace('}',' }').strip().split(' ')

line = []
for ch in tmp:
    if ch == '':
        pass
    else:
        ch = ch.replace('"', '').replace(',', '')
        line.append(ch)


def get_dict(result, line, i, key):
    result = dict()
    line = line[i:]
    for i in range(len(line)):
        if line[i] == '{':
            # print('его дочерний элемент:')
            i += 1
            alt_key = key
            result[alt_key], line, i, key = get_dict(result, line, i, key)
            return result, line, i, key
        elif line[i][-1] == ':':
            # print(str(line[i]), end=' ')
            key = line[i][:-1]
        elif line[i] == '}' or line[i] == '[' or line[i] == ']':
            pass
        else:
            if key in result.keys():
                result[key] = result[key] + ' ' +line[i]
            else:
                result[key] = ''
                result[key] = result[key] + ' ' + line[i]
            # print(line[i])
            pass

    return result, line, i, key



result = {}
i = 0
key = ''

result, line, i, key = get_dict(result, line[1:], i, key)
result = fix_types(result)
ff = {}
ff['type']='string4 dictionary for lab5'
t = ""
for i in range(len(result)-2):
    ff[i] = []
    for j in result[i][2:]:
        if j == '[':
            pass
        elif j == ']':
            if t != "":
                ff[i].append(int(t))
                t = ""
        elif j == ' ':
            ff[i].append(int(t))
            t = ""
        else:
            t += j
            # ff[i].append(int(j))
ff['num_elements'] = int(result['num_elements'])
print(ff)
print(td)
print(td == ff)

