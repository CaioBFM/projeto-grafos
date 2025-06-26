
# Metaheurística otimizada usando Iterated Local Search com 2-opt-simple (ideal para problemas maiores)
def iterated_local_search_optimized(servicos, distance_matrix, capacity, depot, iterations):
    # Solução inicial usando Clarke & Wright Savings
    routes = algoritmo_clarke_wright(servicos, depot, distance_matrix, capacity)
    # 2-opt-simple em cada rota
    routes = [two_opt_simple(r, distance_matrix, depot) for r in routes]
    best_routes = copy.deepcopy(routes)
    best_cost = total_solution_cost(best_routes, distance_matrix, depot)
    for _ in range(min(iterations, 200)):
        # Perturbação
        perturbed = perturbation(routes, capacity)
        # 2-opt-simple na solução perturbada
        perturbed = [two_opt_simple(r, distance_matrix, depot) for r in perturbed]
        cost = total_solution_cost(perturbed, distance_matrix, depot)
        if cost < best_cost:
            best_routes = copy.deepcopy(perturbed)
            best_cost = cost
        routes = copy.deepcopy(perturbed)
    return best_routes   

def algoritmo_clarke_wright(servicos, deposito, matriz_distancias, capacidade):
    rotas, demandas = construir_rotas_iniciais(servicos, deposito, capacidade)
    savings = calcular_savings(rotas, matriz_distancias, deposito)

    for s, i, j in savings:
        if rotas[i] and rotas[j]:
            tentar_fundir_rotas(rotas, demandas, i, j, capacidade)

    # Remove rotas vazias
    rotas = [r for r in rotas if r]
    return rotas

# fuções auxiliares de clarke_wright para construir rotas iniciais, calcular savings e tentar fundir rotas
def construir_rotas_iniciais(servicos, deposito, capacidade):
    rotas = []
    demandas = []
    for serv in servicos:
        demanda = serv['demanda']
        if demanda > capacidade:
            raise ValueError(f"Serviço {serv['id_servico']} demanda maior que capacidade do veículo!")
        rotas.append([serv])
        demandas.append(demanda)
    return rotas, demandas

def calcular_savings(rotas, matriz_distancias, deposito):
    savings = []
    n = len(rotas)
    for i in range(n):
        serv_i = rotas[i][0]
        origem_i = serv_i['origem']
        destino_i = serv_i['destino']

        for j in range(i+1, n):
            serv_j = rotas[j][0]
            origem_j = serv_j['origem']
            destino_j = serv_j['destino']

            s = (matriz_distancias[deposito][origem_i] +
                 matriz_distancias[destino_j][deposito] -
                 matriz_distancias[destino_i][origem_j])
            savings.append((s, i, j))
    savings.sort(key=lambda x: x[0], reverse=True)
    return savings

def tentar_fundir_rotas(rotas, demandas, idx_i, idx_j, capacidade):
    rota_i = rotas[idx_i]
    rota_j = rotas[idx_j]

    demanda_total = demandas[idx_i] + demandas[idx_j]
    if demanda_total > capacidade:
        return False

    ids_i = set(s['id_servico'] for s in rota_i)
    ids_j = set(s['id_servico'] for s in rota_j)

    if ids_i.intersection(ids_j):
        return False

    rotas[idx_i] = rota_i + rota_j
    demandas[idx_i] = demanda_total

    rotas[idx_j] = []
    demandas[idx_j] = 0
    return True

# Busca local 2-opt-simple para otimizar uma rota
def two_opt_simple(route, distance_matrix, depot):
    if len(route) < 3:
        return route
    best = route[:]
    best_cost = route_cost(best, distance_matrix, depot)
    improved = True
    while improved:
        improved = False
        for i in range(1, len(best) - 1):
            for j in range(i + 1, len(best)):
                new_route = best[:i] + best[i:j][::-1] + best[j:]
                new_cost = route_cost(new_route, distance_matrix, depot)
                if new_cost < best_cost:
                    best = new_route
                    best_cost = new_cost
                    improved = True
        if improved:
            break
    return best

import random
import copy

# Funções auxiliares a iterated_local_search_optimized
# Função para calcular o custo total de uma solução (lista de rotas)
def total_solution_cost(routes, distance_matrix, depot):
    return sum(route_cost(r, distance_matrix, depot) for r in routes)

# Função de perturbação: remove 2 ou 3 serviços aleatórios e reinserir em rotas válidas
def perturbation(routes, capacity):
    routes = copy.deepcopy(routes)
    all_services = [(i, idx) for i, r in enumerate(routes) for idx in range(len(r))]
    if len(all_services) < 3:
        return routes
    num_remove = min(3, len(all_services))
    remove_indices = random.sample(all_services, num_remove)
    removed = []
    for i, idx in sorted(remove_indices, reverse=True):
        removed.append(routes[i][idx])
        del routes[i][idx]
    # reinserir serviços removidos
    for serv in removed:
        possible = [i for i, r in enumerate(routes) if sum(s['demanda'] for s in r) + serv['demanda'] <= capacity]
        if not possible:
            # se nenhum rota possível, criar nova rota
            routes.append([serv])
        else:
            i = random.choice(possible)
            insert_pos = random.randint(0, len(routes[i]))
            routes[i].insert(insert_pos, serv)
    # remove rotas vazias
    routes = [r for r in routes if r]
    return routes

# Função para calcular o custo de uma rota
def route_cost(route, distance_matrix, deposit):
    if not route:
        return 0
    cost = distance_matrix[deposit][route[0]['origem']]
    for i in range(len(route) - 1):
        cost += distance_matrix[route[i]['destino']][route[i+1]['origem']]
    cost += distance_matrix[route[-1]['destino']][deposit]
    cost += sum(s['custo_servico'] for s in route)
    return cost

# função para salvar a solução em um arquivo no formato especificado
def salvar_solucao(
    nome_arquivo,
    rotas,
    matriz_distancias,
    deposito=0,
    tempo_referencia_execucao=0,
    tempo_referencia_solucao=0
):
    custo_total_solucao = 0
    total_rotas = len(rotas)
    linhas_rotas = []

    for idx_rota, rota in enumerate(rotas, start=1):
        servicos_unicos = {}
        demanda_rota = 0
        custo_servico_rota = 0
        custo_transporte_rota = 0

        destinos = []
        for serv in rota:
            id_s = serv["id_servico"]
            if id_s not in servicos_unicos:
                servicos_unicos[id_s] = serv
                demanda_rota += serv["demanda"]
                custo_servico_rota += serv["custo_servico"]
            destinos.append(serv["destino"])

        if destinos:
            custo_transporte_rota += matriz_distancias[deposito][destinos[0]]
            for i in range(len(destinos) - 1):
                custo_transporte_rota += matriz_distancias[destinos[i]][destinos[i + 1]]
            custo_transporte_rota += matriz_distancias[destinos[-1]][deposito]

        custo_rota = custo_servico_rota + custo_transporte_rota
        custo_total_solucao += custo_rota

        total_visitas = 2 + len(servicos_unicos)

        linha = f"0 1 {idx_rota} {demanda_rota} {custo_rota} {total_visitas} (D {deposito},1,1)"

        servicos_impressos = set()
        for serv in rota:
            id_s = serv["id_servico"]
            if id_s in servicos_impressos:
                continue
            servicos_impressos.add(id_s)
            linha += f" (S {id_s},{serv['origem']},{serv['destino']})"

        linha += f" (D {deposito},1,1)"
        linhas_rotas.append(linha)

    with open(nome_arquivo, "w", encoding="utf-8") as f:
        f.write(f"{custo_total_solucao}\n")
        f.write(f"{total_rotas}\n")
        f.write(f"{tempo_referencia_execucao}\n")
        f.write(f"{tempo_referencia_solucao}\n")
        for linha in linhas_rotas:
            f.write(linha + "\n")

    print(f"Solução salva em '{nome_arquivo}' com {total_rotas} rotas e custo total {custo_total_solucao}.")


# Heurística GRASP para VRP: construção gulosa randomizada + busca local 2-opt-simple (ideal para problemas menores)
def grasp_heuristic(servicos, distance_matrix, capacity, depot, iterations, alpha):
    best_routes = None
    best_cost = float('inf')
    for _ in range(iterations):
        rotas = grasp_constructive(servicos, distance_matrix, capacity, depot, alpha)
        # Busca local 2-opt-simple em cada rota
        rotas = [two_opt_simple(r, distance_matrix, depot) for r in rotas]
        cost = total_solution_cost(rotas, distance_matrix, depot)
        if cost < best_cost:
            best_routes = copy.deepcopy(rotas)
            best_cost = cost
    return best_routes

# Função construção gulosa randomizada de solução para VRP usando LRC(Lista Restrita de Candidatos).
def grasp_constructive(servicos, distance_matrix, capacity, depot, alpha):
    # Inicializa todos os serviços como não atendidos
    nao_atendidos = set(range(len(servicos)))
    rotas = []
    while nao_atendidos:
        rota = []
        carga = 0
        atual = depot
        while True:
            # Calcula candidatos viáveis
            candidatos = []
            for idx in nao_atendidos:
                s = servicos[idx]
                if carga + s['demanda'] <= capacity:
                    custo = distance_matrix[atual][s['origem']]
                    candidatos.append((custo, idx))
            if not candidatos:
                break
            candidatos.sort()
            # LRC: seleciona aleatoriamente entre os melhores (alpha controla tamanho)
            lrc_size = max(1, int(alpha * len(candidatos)))
            lrc = candidatos[:lrc_size]
            _, escolhido_idx = random.choice(lrc)
            s = servicos[escolhido_idx]
            rota.append(s)
            carga += s['demanda']
            atual = s['destino']
            nao_atendidos.remove(escolhido_idx)
        if rota:
            rotas.append(rota)
    return rotas



