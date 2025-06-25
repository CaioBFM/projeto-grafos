"""

============================================================
Projeto Prático de Grafos - Etapa 1
Grupo:
Caio Bueno Finocchio Martins (202410377)
Diego Alves de Oliveira (202410370)     
============================================================

"""

import numpy as np                      # Importando numpy para manipulação de matrizes
import heapq                            # Importando heapq para implementação de fila de prioridade

# Declarando variável global grafo (para visualização)
global_grafo = None

# Função para extrair dados relevantes de uma lista de linhas de um arquivo .dat já lido
# (Agora recebe as linhas já lidas, não faz leitura de arquivo)
def extrair_dados_instancia(linhas):
    """
    Realiza o parsing das linhas de uma instância .dat do CARP e retorna um dicionário com os dados estruturados.
    Parâmetros:
        linhas (list[str]): Linhas do arquivo .dat já lidas em memória.
    Retorna:
        dict: Dicionário com informações do grafo, demandas, arestas, arcos, etc.
    """
    qtd_veiculos = int(linhas[2].split()[-1])
    capacidade = int(linhas[3].split()[-1])
    deposito = int(linhas[4].split()[-1])
    qtd_vertices = int(linhas[5].split()[-1])
    qtd_arestas = int(linhas[6].split()[-1])
    qtd_arcos = int(linhas[7].split()[-1])
    qtd_vertices_req = int(linhas[8].split()[-1])
    qtd_arestas_req = int(linhas[9].split()[-1])
    qtd_arcos_req = int(linhas[10].split()[-1])
    grafo = np.full((qtd_vertices + 1, qtd_vertices + 1), np.inf)
    np.fill_diagonal(grafo, 0)
    i = 12
    vertices_req = {}
    while i < len(linhas) and linhas[i].strip() and not linhas[i].startswith("ReE."):
        partes = linhas[i].split()
        if partes[0].startswith("N"):
            v = int(partes[0][1:])
            demanda = int(partes[1])
            custo_servico = int(partes[2])
            vertices_req[v] = (demanda, custo_servico)
        i += 1
    while i < len(linhas) and not linhas[i].startswith("ReE."):
        i += 1
    i += 1
    arestas_req = []
    arestas = []
    while i < len(linhas) and linhas[i].strip() and not linhas[i].startswith("EDGE"):
        partes = linhas[i].split()
        if partes[0].startswith("E"):
            origem, destino = map(int, [partes[1], partes[2]])
            custo_transporte = int(partes[3])
            demanda = int(partes[4])
            custo_servico = int(partes[5])
            grafo[origem][destino] = custo_transporte
            grafo[destino][origem] = custo_transporte
            arestas_req.append((origem, destino, custo_transporte, demanda, custo_servico))
            arestas.append((origem, destino, custo_transporte))
        i += 1
    while i < len(linhas) and not linhas[i].startswith("EDGE"):
        i += 1
    i += 1
    while i < len(linhas) and linhas[i].strip() and not linhas[i].startswith("ReA."):
        partes = linhas[i].split()
        if partes[0].startswith("NrE"):
            origem, destino = map(int, [partes[1], partes[2]])
            custo_transporte = int(partes[3])
            grafo[origem][destino] = custo_transporte
            grafo[destino][origem] = custo_transporte
            arestas.append((origem, destino, custo_transporte))
        i += 1
    while i < len(linhas) and not linhas[i].startswith("ReA."):
        i += 1
    i += 1
    arcos_req = []
    arcos = []
    while i < len(linhas) and linhas[i].strip() and not linhas[i].startswith("ARC"):
        partes = linhas[i].split()
        if partes[0].startswith("A"):
            origem, destino = map(int, [partes[1], partes[2]])
            custo_transporte = int(partes[3])
            demanda = int(partes[4])
            custo_servico = int(partes[5])
            grafo[origem][destino] = custo_transporte
            arcos_req.append((origem, destino, custo_transporte, demanda, custo_servico))
            arcos.append((origem, destino, custo_transporte))
        i += 1
    while i < len(linhas) and not linhas[i].startswith("ARC"):
        i += 1
    i += 1
    while i < len(linhas) and linhas[i].strip():
        partes = linhas[i].split()
        if partes[0].startswith("NrA"):
            origem, destino = map(int, [partes[1], partes[2]])
            custo_transporte = int(partes[3])
            grafo[origem][destino] = custo_transporte
            arcos.append((origem, destino, custo_transporte))
        i += 1
    return {
        "qtd_veiculos": qtd_veiculos,
        "capacidade": capacidade,
        "deposito": deposito,
        "qtd_vertices": qtd_vertices,
        "qtd_arestas": qtd_arestas,
        "qtd_arcos": qtd_arcos,
        "qtd_vertices_req": qtd_vertices_req,
        "qtd_arestas_req": qtd_arestas_req,
        "qtd_arcos_req": qtd_arcos_req,
        "vertices_req": vertices_req,
        "arestas_req": arestas_req,
        "arestas": arestas,
        "arcos_req": arcos_req,
        "arcos": arcos,
        "grafo": grafo
    }

# Função para calcular a densidade do grafo
def densidade(qtd_vertices, qtd_arestas, qtd_arcos):
    """
    Calcula a densidade do grafo considerando arestas e arcos.
    Parâmetros:
        qtd_vertices (int): Número de vértices.
        qtd_arestas (int): Número de arestas.
        qtd_arcos (int): Número de arcos.
    Retorna:
        float: Densidade do grafo.
    """
    max_ligacoes_arestas = (qtd_vertices * (qtd_vertices - 1)) / 2
    max_ligacoes_arcos = (qtd_vertices * (qtd_vertices - 1))
    total_ligacoes = max_ligacoes_arestas + max_ligacoes_arcos
    return (qtd_arestas + qtd_arcos) / total_ligacoes

# Função para calcular os graus dos vértices
def calcula_graus(dados):
    """
    Calcula o grau de cada vértice (arestas, entrada, saída, total).
    Parâmetros:
        dados (dict): Dicionário retornado por extrair_dados_instancia.
    Retorna:
        list[tuple]: Lista de tuplas (vértice, grau_arestas, grau_entrada, grau_saida, total).
    """
    qtd_vertices = dados["qtd_vertices"]
    grau_arestas = [0] * (qtd_vertices + 1)
    grau_entrada = [0] * (qtd_vertices + 1)
    grau_saida = [0] * (qtd_vertices + 1)

    for origem, destino, _ in dados["arestas"]:
        grau_arestas[origem] += 1
        grau_arestas[destino] += 1

    for origem, destino, _ in dados["arcos"]:
        grau_saida[origem] += 1
        grau_entrada[destino] += 1

    resultado = []
    for v in range(1, qtd_vertices + 1):
        total = grau_arestas[v] + grau_entrada[v] + grau_saida[v]
        resultado.append((v, grau_arestas[v], grau_entrada[v], grau_saida[v], total))

    return resultado

# Implementação do algoritmo de Dijkstra
def dijkstra(grafo, inicio):
    """
    Executa o algoritmo de Dijkstra para encontrar menores caminhos a partir de um vértice.
    Parâmetros:
        grafo (np.ndarray): Matriz de adjacência.
        inicio (int): Vértice de origem.
    Retorna:
        tuple: (distancias, predecessores) para todos os vértices.
    """
    n = grafo.shape[0]
    distancias = {v: float('inf') for v in range(n)}
    predecessores = {v: -1 for v in range(n)}
    distancias[inicio] = 0
    
    heap = []
    heapq.heappush(heap, (0, inicio))
    
    visitados = set()
    
    while heap:
        dist_atual, vertice_atual = heapq.heappop(heap)
        
        if vertice_atual in visitados:
            continue
            
        visitados.add(vertice_atual)
        
        for vizinho in range(n):
            if grafo[vertice_atual][vizinho] < float('inf'):
                distancia = dist_atual + grafo[vertice_atual][vizinho]
                
                if distancia < distancias[vizinho]:
                    distancias[vizinho] = distancia
                    predecessores[vizinho] = vertice_atual
                    heapq.heappush(heap, (distancia, vizinho))
    
    return distancias, predecessores

# Função para calcular todas as distâncias usando Dijkstra
def calcular_todas_distancias_dijkstra(grafo):
    """
    Calcula todas as distâncias e predecessores entre todos os pares de vértices usando Dijkstra.
    Parâmetros:
        grafo (np.ndarray): Matriz de adjacência.
    Retorna:
        tuple: (matriz de distâncias, matriz de predecessores)
    """
    n = grafo.shape[0]
    distancias = np.full((n, n), np.inf)
    predecessores = np.full((n, n), -1)
    
    for i in range(n):
        dist, pred = dijkstra(grafo, i)
        for j in range(n):
            distancias[i][j] = dist[j]
            predecessores[i][j] = pred[j]
    
    np.fill_diagonal(distancias, 0)
    return distancias, predecessores

# Função de Floyd-Warshall para comparação
def floyd_warshall(grafo):
    """
    Executa o algoritmo de Floyd-Warshall para todos os pares de vértices.
    Parâmetros:
        grafo (np.ndarray): Matriz de adjacência.
    Retorna:
        tuple: (matriz de distâncias, matriz de predecessores)
    """
    n = grafo.shape[0]
    distancia = grafo.copy()
    predecessores = np.full((n, n), -1)

    for i in range(n):
        for j in range(n):
            if i != j and grafo[i][j] < np.inf:
                predecessores[i][j] = i

    for k in range(n):
        for i in range(n):
            for j in range(n):
                if distancia[i][j] > distancia[i][k] + distancia[k][j]:
                    distancia[i][j] = distancia[i][k] + distancia[k][j]
                    predecessores[i][j] = predecessores[k][j]

    return distancia, predecessores

# Função para calcular o caminho médio entre todos os pares de vértices
def caminho_medio(distancias):
    """
    Calcula o caminho médio entre todos os pares de vértices do grafo.
    Parâmetros:
        distancias (np.ndarray): Matriz de distâncias.
    Retorna:
        float: Caminho médio.
    """
    n = distancias.shape[0]
    soma = 0
    cont = 0
    for i in range(1, n):
        for j in range(1, n):
            if i != j and distancias[i][j] < np.inf:
                soma += distancias[i][j]
                cont += 1
    return soma / cont if cont > 0 else 0

# Função para calcular o diâmetro do grafo
def diametro(distancias):
    """
    Calcula o diâmetro do grafo (maior menor caminho).
    Parâmetros:
        distancias (np.ndarray): Matriz de distâncias.
    Retorna:
        int: Diâmetro do grafo.
    """
    n = distancias.shape[0]
    max_dist = 0
    for i in range(1, n):
        for j in range(1, n):
            if i != j and distancias[i][j] < np.inf:
                max_dist = max(max_dist, distancias[i][j])
    return int(max_dist)

# Função para reconstruir o caminho mais curto
def reconstruir_caminho(predecessores, inicio, fim):
    """
    Reconstrói o caminho mais curto entre dois vértices usando a matriz de predecessores.
    Parâmetros:
        predecessores (dict ou np.ndarray): Predecessores de cada vértice.
        inicio (int): Vértice de origem.
        fim (int): Vértice de destino.
    Retorna:
        list[int] ou None: Lista de vértices do caminho ou None se não existe.
    """
    caminho = []
    atual = fim
    
    while atual != -1 and atual != inicio and atual in predecessores:
        caminho.insert(0, atual)
        atual = predecessores[atual]
    
    if atual == inicio:
        caminho.insert(0, inicio)
        return caminho
    return None

# Função para calcular a intermediação de cada vértice usando Dijkstra
def calcula_intermediacao(vertices, grafo):
    """
    Calcula a intermediação (betweenness) de cada vértice usando caminhos mínimos.
    Parâmetros:
        vertices (list[int]): Lista de vértices.
        grafo (np.ndarray): Matriz de adjacência.
    Retorna:
        dict: Dicionário {vértice: valor de intermediação}
    """
    intermediacao = {v: 0 for v in vertices}
    
    for u in vertices:
        distancias, predecessores = dijkstra(grafo, u)
        for v in vertices:
            if u != v:
                caminho = reconstruir_caminho(predecessores, u, v)
                if caminho:
                    for vertice in caminho[1:-1]:  # Ignora o primeiro e o último vértice
                        intermediacao[vertice] += 1
    
    return intermediacao

# Função para carregar o grafo e os dados a partir de linhas já lidas (não lê arquivo)
def carregar_grafo_de_linhas(linhas):
    """
    Realiza o parsing das linhas e retorna a matriz de adjacência e o dicionário de dados.
    Parâmetros:
        linhas (list[str]): Linhas do arquivo .dat já lidas em memória.
    Retorna:
        tuple: (grafo, dados)
    """
    dados = extrair_dados_instancia(linhas)
    return dados["grafo"], dados