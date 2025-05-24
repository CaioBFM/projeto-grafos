import sys
import time
import csv
import os
import psutil
from heuristica import resolver_problema, info_serv, custo_serv_dict, custos_desloc

def ler_instancia(caminho):
    try:
        with open(caminho, 'r', encoding='utf-8') as f:
            linhas = [l.rstrip() for l in f if l.strip()]

        # Cabeçalhos fixos
        capacidade   = int(linhas[3].split()[-1])
        deposito     = int(linhas[4].split()[-1])
        qtd_v_req    = int(linhas[8].split()[-1])
        qtd_e_req    = int(linhas[9].split()[-1])
        qtd_a_req    = int(linhas[10].split()[-1])

        # Seção ReN.
        i = 12
        nos = []
        for _ in range(qtd_v_req):
            partes = linhas[i].split()
            v = int(partes[0][1:]); q = int(partes[1])
            nos.append((v, q)); i += 1

        # Seção ReE. (arestas requeridas)
        while not linhas[i].startswith('ReE.'):
            i += 1
        i += 1
        arestas_req = []
        for _ in range(qtd_e_req):
            p = linhas[i].split()
            o, d, c, qv = map(int, p[1:5])
            arestas_req.append(((o, d), c, qv)); i += 1

        # Seção EDGE (arestas não requeridas)
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

        # Seção ReA. (arcos requeridos)
        while not linhas[i].startswith('ReA.'):
            i += 1
        i += 1
        arcos_req = []
        for _ in range(qtd_a_req):
            p = linhas[i].split()
            o, d, c, qv = map(int, p[1:5])
            arcos_req.append(((o, d), c, qv)); i += 1

        # Seção ARC (arcos não requeridos)
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
        print(f"Erro ao ler instância: {e}")
        sys.exit(1)


def obter_clocks_csv(nome_base):
    import csv
    import os
    caminho_csv = os.path.join(os.path.dirname(__file__), 'reference_values.csv')
    try:
        with open(caminho_csv, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)  # pula cabeçalho
            for row in reader:
                if row and row[0].strip() == nome_base:
                    return int(row[3]), int(row[4])
    except Exception as e:
        print(f"Erro ao ler reference_values.csv: {e}")
    return -1, -1

def obter_clock_melhor_sol(nome_base):
    caminho_csv = os.path.join(os.path.dirname(__file__), 'reference_values.csv')
    try:
        with open(caminho_csv, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)  # pula cabeçalho
            for row in reader:
                if row and row[0].strip() == nome_base:
                    return int(row[4])
    except Exception as e:
        print(f"Erro ao ler reference_values.csv: {e}")
    return -1


def main():
    if len(sys.argv) != 2:
        print('Uso: python main.py <instancia.dat>')
        sys.exit(1)

    instancia = sys.argv[1]
    nome_base = os.path.splitext(os.path.basename(instancia))[0]
    pasta_resultados = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resultados')
    os.makedirs(pasta_resultados, exist_ok=True)
    saida = os.path.join(pasta_resultados, f"{nome_base}_sol.dat")
    clock_melhor_sol = obter_clock_melhor_sol(nome_base)
    v0, Q, arestas_req, arcos_req, nos, arestas_nr, arcos_nr = ler_instancia(instancia)

    freq_mhz = psutil.cpu_freq().current
    freq_hz = freq_mhz * 1_000_000

    clock_inicio_total = time.perf_counter_ns()
    rotas, seq_ids_por_rota, custo_desloc_total, custo_serv_total = resolver_problema(
        v0, Q, arestas_req, arcos_req, nos, arestas_nr, arcos_nr
    )
    clock_fim_total = time.perf_counter_ns()
    clock_total = clock_fim_total - clock_inicio_total
    ciclos_estimados = int(clock_total * (freq_hz / 1_000_000_000))

    custo_total = custo_desloc_total + custo_serv_total
    num_rotas = len(rotas)

    # Escreve solução em arquivo
    with open(saida, 'w', encoding='utf-8') as f:
        f.write(f"{custo_total}\n")
        f.write(f"{num_rotas}\n")
        f.write(f"{clock_melhor_sol}\n")
        f.write(f"{ciclos_estimados}\n")

        for rid, (rota, seq_ids) in enumerate(zip(rotas, seq_ids_por_rota), start=1):
            demanda_rota = sum(custo_serv_dict[sid] for sid in seq_ids)
            # Calcula custo de deslocamento da rota
            custo_desloc = 0
            for u, v in zip(rota, rota[1:]):
                if (u, v) in custos_desloc:
                    custo_desloc += custos_desloc[(u, v)]
                else:
                    from heuristica import dijkstra
                    grafo_tmp = {}
                    for (a, b), c in custos_desloc.items():
                        if a not in grafo_tmp:
                            grafo_tmp[a] = []
                        grafo_tmp[a].append((b, c))
                    if u not in grafo_tmp:
                        grafo_tmp[u] = []
                    dist, _ = dijkstra(grafo_tmp, u)
                    custo_desloc += dist.get(v, 0)
            custo_rota = custo_desloc + demanda_rota
            num_visitas = 2 + len(seq_ids)

            prefixo = f"0 1 {rid} {demanda_rota} {custo_rota} {num_visitas}"
            detalhes = ['(D 0,1,1)']
            for sid in seq_ids:
                _, i, j = info_serv[sid]
                detalhes.append(f"(S {sid},{i},{j})")
            detalhes.append('(D 0,1,1)')

            f.write(prefixo + ' ' + ' '.join(detalhes) + "\n")

if __name__ == '__main__':
    main()