# mesmo padrão da main, mas para testes unitários.
import os
import time
import psutil
from concurrent.futures import ProcessPoolExecutor # ProcessPoolExecutor para paralelizar o processamento melhorando o desempenho
from heuristica import salvar_solucao, iterated_local_search_optimized, grasp_heuristic
from grafo_utils import construir_grafo_e_dados, ler_instancia

# Função para processar uma instancia e gerar a solução (testes unitários)
def processar_teste_unitario_automatico(nome_dat):
    pasta_testes = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instancias')
    pasta_resultados = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resultados')
    os.makedirs(pasta_resultados, exist_ok=True)
    arquivo = os.path.join(pasta_testes, nome_dat)
    if not os.path.exists(arquivo):
        print(f"Arquivo {arquivo} não encontrado!")
        return
    saida_base = os.path.join(pasta_resultados, f"sol-{os.path.splitext(os.path.basename(arquivo))[0]}")
    v0, Q, arestas_req, arcos_req, nos, arestas_nr, arcos_nr = ler_instancia(arquivo)
    freq_mhz = psutil.cpu_freq().current
    freq_hz = freq_mhz * 1_000_000
    clock_inicio_total = time.perf_counter_ns()
    # Montar lista de serviços obrigatórios (igual main.py)
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
    matriz_distancias = matriz_menores_distancias(nos, arestas_req, arcos_req, arestas_nr, arcos_nr)
    clock_ini_sol = time.perf_counter_ns()
    if len(servicos) > 200: 
        rotas = iterated_local_search_optimized(servicos, matriz_distancias, Q, v0, iterations=100) # aumento do numero de perturbações para melhores resultados
    else:
        rotas = grasp_heuristic(servicos, matriz_distancias, Q, v0, iterations=100, alpha=0.2)
    nome_saida = saida_base + ".dat"
    clock_fim_sol = time.perf_counter_ns()
    clock_sol = clock_fim_sol - clock_ini_sol
    clock_fim_total = time.perf_counter_ns()
    clock_total = clock_fim_total - clock_inicio_total
    ciclos_estimados_total = int(clock_total * (freq_hz / 1_000_000_000))
    ciclos_estimados_melhor_sol = int(clock_sol * (freq_hz / 1_000_000_000))
    salvar_solucao(
        nome_saida,
        rotas,
        matriz_distancias,
        deposito=v0,
        tempo_referencia_execucao=ciclos_estimados_total,
        tempo_referencia_solucao=ciclos_estimados_melhor_sol
    )
    print(f"Solução salva em {nome_saida}")

# fw
def matriz_menores_distancias(nos, arestas_req, arcos_req, arestas_nr, arcos_nr):
    grafo, _ = construir_grafo_e_dados(nos, arestas_req, arcos_req, arestas_nr, arcos_nr)
    n = grafo.shape[0]
    dist = grafo.copy()
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][j] > dist[i][k] + dist[k][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    return dist

# Função para rodar testes unitários automáticos em lote, processamento paralelo
# utilizado por gerar_comparacao.py
def rodar_teste_unitario_automatico_em_lote(lista_nomes):
    with ProcessPoolExecutor() as executor:
        list(executor.map(processar_teste_unitario_automatico, lista_nomes))

def teste_unitario_rodar_uma_instancia():
    nome = input('Digite o nome do arquivo .dat (ex: BHW1.dat): ').strip()
    processar_teste_unitario_automatico(nome)

if __name__ == '__main__':
    teste_unitario_rodar_uma_instancia()
