from collections import deque


def ford_fulkerson(n, s, t, c):
    '''
    n: number of nodes
    s: start node
    t: target node
    c: capacity matrix
    '''
    INF = 1 << 50
    max_flow = 0

    # flow matrix f(u,v) for computing the residual capacity
    # cf = c(u,v) - f(u,v) for the edge (u,v)
    f = [[0 for k in range(n)] for i in range(n)]

    # while there is a path from s to t in the residual graph
    while True:
        # Use BFS to find s-t path in residual graph
        prev = [-1 for _ in range(n)]
        prev[s] = -2
        q = deque()
        q.append(s)

        while q and prev[t] == -1:
            u = q.popleft()
            for v in range(n):
                cf = c[u][v] - f[u][v]
                if cf > 0 and prev[v] == -1:
                    q.append(v)
                    prev[v] = u

        if prev[t] == -1:  # if t has not been reached
            break

        # augment s-t path in residual graph that has been found by BFS
        v = t
        delta = INF
        while True:
            u = prev[v]
            cf = c[u][v] - f[u][v]
            delta = min(delta, cf)
            v = u
            if v == s:
                break

        v = t
        while True:
            u = prev[v]
            f[u][v] += delta
            f[v][u] -= delta
            v = u
            if v == s:
                break

        max_flow += delta

    return max_flow

def task():
    from sys import stdin, stdout
    num_nodes, num_edges, s, t = [int(c) for c in stdin.readline().split()]
    capacity_matrix = [[0 for k in range(num_nodes)] for i in range(num_nodes)]

    for i in range(num_edges):
        u, v, c = [int(c) for c in stdin.readline().split()]
        capacity_matrix[u - 1][v - 1] = c

    res = ford_fulkerson(num_nodes, s - 1, t - 1, capacity_matrix)
    stdout.write("Maximum flow: " + str(res) + '\n')


if __name__ == '__main__':
    task()
