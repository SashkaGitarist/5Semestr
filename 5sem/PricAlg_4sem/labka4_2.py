import sys
from collections import defaultdict
from functools import *
import functools
import copy


class RegEx:

    def __init__(self, regex_str):
        if not balanced_skobki(regex_str):
            raise Exception("Выражение неверно!!!")
        self.regex = '(' + regex_str + ')'
        self.nka = None
        self.dka = DKA.from_nka(self.get_nka())
        self.dka.minimize()

    def get_nka(self):
        alphabet = set(c for c in self.regex if c not in (')', '(', '|', '*', '+'))
        # print(alphabet)
        nka = NKA(alphabet)
        nka.set_start(0)
        nka.add_dop(len(self.regex) - 1)
        stack = list()
        N = len(self.regex)

        for i, c in enumerate(self.regex):
            ind = i
            if c in alphabet:
                nka.add_trans(i, i + 1, c)
            elif c == '(':
                nka.add_trans(i, i + 1, 'eps')
                stack.append(i)
            elif c == ')':
                nka.add_trans(i, i + 1, 'eps')
                ind = stack.pop()
                tmplist = list()
                while self.regex[ind] == '|':
                    tmplist.append(ind)
                    nka.add_trans(ind, i, 'eps')
                    ind = stack.pop()
                for n in tmplist:
                    nka.add_trans(ind, n + 1, 'eps')
            elif c == '|':
                stack.append(i)
            elif c in ('*', '+'):
                nka.add_trans(i, i + 1, 'eps')
            if i < N - 1 and self.regex[i + 1] in ('*', '+'):
                if self.regex[i + 1] == '*':
                    nka.add_trans(ind, i + 1, 'eps')
                nka.add_trans(i + 1, ind, 'eps')
        nka.sosts.remove(N)
        nka.perehod = defaultdict(set, [(k, v) for k, v in nka.perehod.items()
                                        if N not in v])
        # print(nka.perehod)
        return nka

    def proverka(self, text, index):
        index_str = 0
        sost = self.dka.start_sost
        for i, letter in enumerate(text):
            sost = self.dka.get_perehod(sost, letter)
            result = any(map(lambda s: s in sost, (f for f in self.dka.dop_sost)))
            index_str = i
            if (result == True):
                break
        # result = any(map(lambda s: s in sost, (f for f in self.dka.dop_sost)))
        return (result, text[:index_str + 1], [index, index + index_str])


class avtomat:

    def __init__(self, alphabet):
        self.perehod = defaultdict(set)
        self.sosts = set()
        self.dop_sost = set()
        self.start_sost = None
        self.alphabet = set(alphabet)

    def set_start(self, sost):
        assert isinstance(sost, int)
        self.start_sost = sost
        self.sosts.add(sost)

    def add_dop(self, sost):
        assert isinstance(sost, int)
        self.dop_sost.add(sost)
        self.sosts.add(sost)

    def add_dops(self, sosts):
        for sost in sosts:
            self.add_dop(sost)

    def add_trans(self, s1, s2, sym):
        self.sosts = self.sosts.union({s1, s2})
        self.perehod[s1, sym].add(s2)

    def add_transes(self, transes):
        for s1, a in transes:
            self.add_trans(s1, transes[s1, a], a)

    def contains_final(self, sosts):
        return any(map(lambda s: s in sosts, self.dop_sost))

    def contains_start(self, sosts):
        return any(map(lambda s: s == self.start_sost, sosts))

    def has_perehod_with(self, sost, sym):
        return (sost, sym) in self.perehod


class NKA(avtomat):

    def __init__(self, alphabet, accept_void=True):
        avtomat.__init__(self, alphabet)
        if accept_void: self.alphabet.add('eps')

    def single_perehod(self, sost, sym):
        assert isinstance(sost, int) and sost in self.sosts
        eclosure = self.epsilon_closure(sost)
        r = [list(map(self.epsilon_closure, self.perehod[s, sym]))
             for s in eclosure]
        r = sum(r, list())
        if len(r) == 0:
            return set()
        return reduce(set.union, r)

    def get_perehod(self, sost, sym):
        if isinstance(sost, int):
            return self.single_perehod(sost, sym)
        if len(sost) == 1:
            return self.single_perehod(list(sost)[0], sym)
        r = [self.single_perehod(s, sym) for s in sost]
        if len(r) == 0:
            return set()
        return reduce(set.union, r)

    def epsilon_closure(self, sost, result=set()):
        assert isinstance(sost, int) and sost in self.sosts
        result = result.union(self.perehod[sost, 'eps'] | {sost})
        for s in result:
            for s2 in self.perehod[s, 'eps']:
                if s2 not in result:
                    result = self.epsilon_closure(s2, result)
        return result


class DKA(avtomat):

    def get_perehod(self, sost, sym):
        if isinstance(sost, int):
            return self.perehod[sost, sym]
        if len([self.perehod[s, sym] for s in sost]) == 0:
            return []
        return reduce(set.union, [self.perehod[s, sym] for s in sost])

    @classmethod
    def from_nka(cls, nka):

        dka = DKA(nka.alphabet - {'eps'})
        start = frozenset(nka.epsilon_closure(0))
        sosts = {start: 0}
        to_visit = [start]
        if nka.contains_final(start):
            dka.add_dop(sosts[start])
        next_index = 0
        dka.set_start(0)
        while to_visit:
            sost = to_visit.pop(0)
            for sym in dka.alphabet:
                next = frozenset(nka.get_perehod(sost, sym))
                if next:
                    if next not in sosts:
                        next_index += 1
                        sosts[next] = next_index
                        to_visit.append(next)
                    if nka.contains_final(next):
                        dka.add_dop(sosts[next])
                    dka.add_trans(sosts[sost], sosts[next], sym)
        return dka

    def minimize(self):
        non_reachable = self.non_reachable()
        self.sosts = self.sosts - non_reachable
        self.dop_sost = self.dop_sost - non_reachable
        self.perehod = defaultdict(set, [((s, a), self.perehod[s, a])
                                         for s, a in self.perehod if s not in non_reachable])

        self.add_error_sost()

        table = {(min(s1, s2), max(s1, s2)): (s1 in self.dop_sost) != (s2 in self.dop_sost)
                 for i, s1 in enumerate(self.sosts)
                 for j, s2 in enumerate(self.sosts)
                 if i < j}
        distinguishable = lambda x, y: table[min(x, y), max(x, y)]
        changed = True
        while changed:
            changed = False
            for p, q in table:
                if table[p, q]: continue
                for a in self.alphabet:
                    r, s = self.perehod[p, a], self.perehod[q, a]
                    r, s = list(r)[0], list(s)[0]
                    if r == s: continue
                    if distinguishable(r, s):
                        table[p, q] = changed = True
                        break
        equivalences = {s: {s} for s in self.sosts}
        for sosts in filter(lambda x: table[x] == False, table):
            for s1 in sosts:
                for s2 in sosts:
                    equivalences[s1].add(s2)
        sosts_map = {frozenset(s): min(s) for s in equivalences.values()}
        dka = DKA(self.alphabet)
        for old_sosts_set, new_sost in sosts_map.items():
            if self.contains_start(old_sosts_set):
                dka.set_start(new_sost)
            if self.contains_final(old_sosts_set):
                dka.add_dop(new_sost)
            for old_sost in old_sosts_set:
                for a in (a for s, a in self.perehod if s == old_sost):
                    to = equivalences[self.get_perehod(old_sost, a).pop()]
                    dka.add_trans(new_sost, sosts_map[frozenset(to)], a)
        self.sosts = dka.sosts
        self.perehod = dka.perehod
        self.start_sost = dka.start_sost
        self.dop_sost = dka.dop_sost
        self.remove_sost()

    def non_reachable(self):
        non_visited = self.sosts.copy()
        perehod = copy.deepcopy(self.perehod)

        def f(s):
            non_visited.remove(s)
            perehods = filter(lambda k_a: k_a[0] == s, perehod)
            for k, a in perehods:
                t = perehod[k, a].pop()
                if t in non_visited:
                    f(t)

        f(self.start_sost)
        return non_visited

    def add_error_sost(self, error_sost=-1):
        self.sosts.add(error_sost)
        for sost in self.sosts:
            for sym in self.alphabet:
                if not self.has_perehod_with(sost, sym):
                    self.add_trans(sost, error_sost, sym)

    def remove_sost(self, sost=-1):
        self.sosts.remove(sost)
        perehod = defaultdict(set)
        for t in self.perehod:
            if -1 in self.perehod[t]:
                self.perehod[t].remove(-1)
            if t[0] != -1 and self.perehod[t]:
                perehod[t] = self.perehod[t]
        self.perehod = perehod


def balanced_skobki(txt):
    count = 0
    for c in txt:
        if c == '(':
            count += 1
        if c == ')':
            count -= 1
        if count < 0:
            return False
    return count == 0


with open("string4") as f:
    file = f.readlines()

regex = file[0].strip()
print("Регулярное выражение: ", regex)
res = RegEx(regex)
result = dict(res.dka.perehod)
for r in result.keys():
    print("%s - %s -> %s" % (r[0], r[1], result.get(r)))

print('Начальное состоение: ', res.dka.start_sost)
print('Допускающее состояние: ', res.dka.dop_sost)

str = file[1]
print("Строка: ", str)
result_str = []
strings = []
for i in range(0, len(str)):
    strings.append([str[i:len(str)], i])
for s in strings:
    res_ = res.proverka(s[0], s[1])
    result_str.append(res_)

for list in result_str:
    if list[0]:
        print('Допускающая: ', list[1], list[2])
