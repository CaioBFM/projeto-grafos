"""
Arquivo principal do projeto CARP.
Realiza a leitura da instância, execução da heurística Clarke & Wright e gravação da solução.
"""
import os
import psutil
import time
from heuristica import algoritmo_clarke_wright, salvar_solucao, iterated_local_search, iterated_local_search_optimized
from ler_escrever_arquivos import ler_instancia
import numpy as np

def construir_grafo(nos, arestas_req, arcos_req, arestas_nr, arcos_nr):
    # Cria matriz de adjacência com infinito
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
    # Arestas requeridas e não requeridas (bidirecional)
    for (u, v), c, *_ in arestas_req + arestas_nr:
        grafo[u][v] = c
        grafo[v][u] = c
    # Arcos requeridos e não requeridos (direcional)
    for (u, v), c, *_ in arcos_req + arcos_nr:
        grafo[u][v] = c
    return grafo

def matriz_menores_distancias(nos, arestas_req, arcos_req, arestas_nr, arcos_nr):
    grafo = construir_grafo(nos, arestas_req, arcos_req, arestas_nr, arcos_nr)
    n = grafo.shape[0]
    dist = grafo.copy()
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][j] > dist[i][k] + dist[k][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    return dist

def teste_unitario_rodar_uma_instancia():
    nome = input('Digite o nome do arquivo .dat (ex: BHW1.dat): ').strip()
    pasta_testes = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'testes')
    pasta_resultados = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resultados')
    os.makedirs(pasta_resultados, exist_ok=True)
    arquivo = os.path.join(pasta_testes, nome)
    if not os.path.exists(arquivo):
        print(f"Arquivo {arquivo} não encontrado!")
        return
    saida = os.path.join(pasta_resultados, f"sol-{os.path.splitext(os.path.basename(arquivo))[0]}.dat")
    v0, Q, arestas_req, arcos_req, nos, arestas_nr, arcos_nr = ler_instancia(arquivo)
    # Montar lista de serviços obrigatórios
    servicos = []
    id_servico = 1
    for v, q in nos:
        servicos.append({
            'id_servico': id_servico,
            'origem': v,
            'destino': v,
            'demanda': q,
            'custo_servico': 0
        })
        id_servico += 1
    for (u, v), c, q in arestas_req:
        servicos.append({
            'id_servico': id_servico,
            'origem': u,
            'destino': v,
            'demanda': q,
            'custo_servico': c
        })
        id_servico += 1
    for (u, v), c, q in arcos_req:
        servicos.append({
            'id_servico': id_servico,
            'origem': u,
            'destino': v,
            'demanda': q,
            'custo_servico': c
        })
        id_servico += 1
    freq_mhz = psutil.cpu_freq().current
    freq_hz = freq_mhz * 1_000_000
    clock_inicio_total = time.perf_counter_ns()
    grafo = construir_grafo(nos, arestas_req, arcos_req, arestas_nr, arcos_nr)
    matriz_distancias = matriz_menores_distancias(nos, arestas_req, arcos_req, arestas_nr, arcos_nr)
    # Executar metaheurística otimizada
    clock_ini_sol = time.perf_counter_ns()
    rotas = iterated_local_search_optimized(servicos, matriz_distancias, Q, v0, iterations=30)
    clock_fim_sol = time.perf_counter_ns()
    clock_sol = clock_fim_sol - clock_ini_sol
    clock_fim_total = time.perf_counter_ns()
    clock_total = clock_fim_total - clock_inicio_total
    ciclos_estimados_total = int(clock_total * (freq_hz / 1_000_000_000))
    ciclos_estimados_melhor_sol = int(clock_sol * (freq_hz / 1_000_000_000))
    # Exportar solução usando a função da heurística
    salvar_solucao(
        saida,
        rotas,
        matriz_distancias,
        deposito=v0,
        tempo_referencia_execucao=ciclos_estimados_total,
        tempo_referencia_solucao=ciclos_estimados_melhor_sol
    )
    print(f"Solução salva em {saida}")

if __name__ == '__main__':
    teste_unitario_rodar_uma_instancia()