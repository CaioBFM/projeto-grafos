# Função para ler a instância do problema a partir de um arquivo .dat e retorna os dados estruturados
def ler_instancia(caminho):
    try:
        with open(caminho, 'r', encoding='utf-8') as f:
            linhas = [l.rstrip() for l in f if l.strip()]
        capacidade   = int(linhas[3].split()[-1])
        deposito     = int(linhas[4].split()[-1])
        qtd_v_req    = int(linhas[8].split()[-1])
        qtd_e_req    = int(linhas[9].split()[-1])
        qtd_a_req    = int(linhas[10].split()[-1])
        i = 12
        nos = []
        for _ in range(qtd_v_req):
            partes = linhas[i].split()
            v = int(partes[0][1:]); q = int(partes[1])
            nos.append((v, q)); i += 1
        while not linhas[i].startswith('ReE.'):
            i += 1
        i += 1
        arestas_req = []
        for _ in range(qtd_e_req):
            p = linhas[i].split()
            o, d, c, qv = map(int, p[1:5])
            arestas_req.append(((o, d), c, qv)); i += 1
        while not linhas[i].startswith('EDGE'):
            i += 1
        i += 1
        arestas_nr = []
        while i < len(linhas) and linhas[i] and not linhas[i].startswith('ReA.'):
            p = linhas[i].split()
            if len(p) >= 4:
                o, d, c = map(int, p[1:4])
                arestas_nr.append(((o, d), c))
            i += 1
        while not linhas[i].startswith('ReA.'):
            i += 1
        i += 1
        arcos_req = []
        for _ in range(qtd_a_req):
            p = linhas[i].split()
            o, d, c, qv = map(int, p[1:5])
            arcos_req.append(((o, d), c, qv)); i += 1
        while not linhas[i].startswith('ARC'):
            i += 1
        i += 1
        arcos_nr = []
        while i < len(linhas):
            p = linhas[i].split()
            if len(p) >= 4 and p[0].startswith('NrA'):
                o, d, c = map(int, p[1:4])
                arcos_nr.append(((o, d), c))
            i += 1
        return deposito, capacidade, arestas_req, arcos_req, nos, arestas_nr, arcos_nr
    except Exception as e:
        raise RuntimeError(f"Erro ao ler instância: {e}")
    
import numpy as np

# Função para construir o grafo (matriz) e os dados a partir das listas de nós, arestas e arcos
def construir_grafo_e_dados(nos, arestas_req, arcos_req, arestas_nr, arcos_nr):
    vertices = set()
    for v, _ in nos:
        vertices.add(v)
    for (u, v), *_ in arestas_req + arestas_nr:
        vertices.add(u)
        vertices.add(v)
    for (u, v), *_ in arcos_req + arcos_nr:
        vertices.add(u)
        vertices.add(v)
    n = max(vertices)
    grafo = np.full((n+1, n+1), np.inf)
    np.fill_diagonal(grafo, 0)
    # Arestas bidirecionais
    for (u, v), c, *_ in arestas_req + arestas_nr:
        grafo[u][v] = c
        grafo[v][u] = c
    # Arcos direcionais
    for (u, v), c, *_ in arcos_req + arcos_nr:
        grafo[u][v] = c
    dados = {
        'nos': nos,
        'arestas_req': arestas_req,
        'arcos_req': arcos_req,
        'arestas_nr': arestas_nr,
        'arcos_nr': arcos_nr,
        'grafo': grafo
    }
    return grafo, dados
