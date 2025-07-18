import os
import time
import psutil
from concurrent.futures import ProcessPoolExecutor # ProcessPoolExecutor para paralelizar o processamento melhorando o desempenho
from heuristica import salvar_solucao, iterated_local_search_optimized
from grafo_utils import construir_grafo_e_dados, ler_instancia

# Função para processar cada instância
def processar_instancia(arquivo, pasta_testes, pasta_resultados):
    # leitura e preparação da instância
    instancia = os.path.join(pasta_testes, arquivo)
    saida_base = os.path.join(pasta_resultados, f"sol-{os.path.splitext(os.path.basename(instancia))[0]}")
    v0, Q, arestas_req, arcos_req, nos, arestas_nr, arcos_nr = ler_instancia(instancia)
    # Pega a frequência atual do processador, isso é usado para estimar o número de ciclos de clock gastos na execução,
    # tornando a medição de tempo mais comparável entre máquinas diferentes.
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
    # Matriz de distâncias mínimas entre os nós
    matriz_distancias = matriz_menores_distancias(nos, arestas_req, arcos_req, arestas_nr, arcos_nr)
    clock_ini_sol = time.perf_counter_ns()
    rotas = iterated_local_search_optimized(servicos, matriz_distancias, Q, v0, iterations=100)
    nome_saida = saida_base + ".dat"
    # Cálculo do tempo de execução e estimativa de ciclos, após a solução ser encontrada
    # Isso fornece uma estimativa de quantos ciclos de CPU foram gastos, útil para comparar desempenho em diferentes máquinas.
    clock_fim_sol = time.perf_counter_ns()
    clock_sol = clock_fim_sol - clock_ini_sol
    clock_fim_total = time.perf_counter_ns()
    clock_total = clock_fim_total - clock_inicio_total
    ciclos_estimados_total = int(clock_total * (freq_hz / 1_000_000_000))
    ciclos_estimados_melhor_sol = int(clock_sol * (freq_hz / 1_000_000_000))
    # Exportar solução usando a função da heurística para gravar rotas, matriz de distâncias, depósito e tempos de execução no arquivo de saída
    salvar_solucao(
        nome_saida,
        rotas,
        matriz_distancias,
        deposito=v0,
        tempo_referencia_execucao=ciclos_estimados_total,
        tempo_referencia_solucao=ciclos_estimados_melhor_sol
    )

# Função utilitária para matriz de distâncias (fw)
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

# Função principal para executar o processamento de instâncias
def main():
    # Definir os caminhos para as pastas de instâncias e resultados
    pasta_testes = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instancias')
    pasta_resultados = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resultados')
    os.makedirs(pasta_resultados, exist_ok=True)
    arquivos_dat = [f for f in os.listdir(pasta_testes) if f.endswith('.dat')]
    # Iniciar o ProcessPoolExecutor para processar as instâncias em paralelo
    with ProcessPoolExecutor() as executor:
        # Submeter as tarefas de processamento para cada arquivo .dat
        futures = [executor.submit(processar_instancia, arquivo, pasta_testes, pasta_resultados) for arquivo in arquivos_dat]
        for future in futures:
            future.result()

if __name__ == '__main__':
    main()
