import os
import time
import psutil
from heuristica import algoritmo_clarke_wright, salvar_solucao, iterated_local_search_optimized
from ler_escrever_arquivos import ler_instancia
import numpy as np


# Funções utilitárias para grafo e matriz de distâncias

def construir_grafo(nos, arestas_req, arcos_req, arestas_nr, arcos_nr):
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
    for (u, v), c, *_ in arestas_req + arestas_nr:
        grafo[u][v] = c
        grafo[v][u] = c
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


def main():
    pasta_testes = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instancias')
    pasta_resultados = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resultados')
    os.makedirs(pasta_resultados, exist_ok=True)
    arquivos_dat = [f for f in os.listdir(pasta_testes) if f.endswith('.dat')]
    for arquivo in arquivos_dat:
        instancia = os.path.join(pasta_testes, arquivo)
        saida_base = os.path.join(pasta_resultados, f"sol-{os.path.splitext(os.path.basename(instancia))[0]}")
        v0, Q, arestas_req, arcos_req, nos, arestas_nr, arcos_nr = ler_instancia(instancia)
        freq_mhz = psutil.cpu_freq().current
        freq_hz = freq_mhz * 1_000_000
        clock_inicio_total = time.perf_counter_ns()
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
        grafo = construir_grafo(nos, arestas_req, arcos_req, arestas_nr, arcos_nr)
        matriz_distancias = matriz_menores_distancias(nos, arestas_req, arcos_req, arestas_nr, arcos_nr)
        clock_ini_sol = time.perf_counter_ns()
        if len(servicos) > 100:
            # Grafo grande: apenas Clarke & Wright
            rotas = algoritmo_clarke_wright(servicos, v0, matriz_distancias, Q)
            nome_saida = saida_base + ".dat"
        else:
            # Grafo pequeno: metaheurística otimizada
            rotas = iterated_local_search_optimized(servicos, matriz_distancias, Q, v0, iterations=30)
            nome_saida = saida_base + ".dat"
        clock_fim_sol = time.perf_counter_ns()
        clock_sol = clock_fim_sol - clock_ini_sol
        clock_fim_total = time.perf_counter_ns()
        clock_total = clock_fim_total - clock_inicio_total
        ciclos_estimados_total = int(clock_total * (freq_hz / 1_000_000_000))
        ciclos_estimados_melhor_sol = int(clock_sol * (freq_hz / 1_000_000_000))
        # Exportar solução usando a função da heurística
        salvar_solucao(
            nome_saida,
            rotas,
            matriz_distancias,
            deposito=v0,
            tempo_referencia_execucao=ciclos_estimados_total,
            tempo_referencia_solucao=ciclos_estimados_melhor_sol
        )


if __name__ == '__main__':
    main()
