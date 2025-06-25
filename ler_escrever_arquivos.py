# Funções para leitura e escrita de arquivos do projeto CARP
import csv

def ler_instancia(caminho):
    """
    Lê um arquivo de instância .dat do CARP e retorna os dados estruturados.
    Parâmetros:
        caminho (str): Caminho do arquivo .dat
    Retorna:
        tuple: (deposito, capacidade, arestas_req, arcos_req, nos, arestas_nr, arcos_nr)
    """
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

def ler_reference_values(caminho_csv, nome_base):
    """
    Lê o arquivo de valores de referência e retorna clocks e clocks_melhor_sol para a instância.
    Parâmetros:
        caminho_csv (str): Caminho do arquivo reference_values.csv
        nome_base (str): Nome base da instância
    Retorna:
        tuple: (clocks, clocks_melhor_sol)
    """
    try:
        with open(caminho_csv, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                if row and row[0].strip() == nome_base:
                    return int(row[3]), int(row[4])
    except Exception as e:
        raise RuntimeError(f"Erro ao ler reference_values.csv: {e}")
    return -1, -1

def salvar_solucao(saida, custo_total, num_rotas, clock_melhor_sol, ciclos_estimados, rotas, seq_ids_por_rota, demanda_rota, custo_rota, detalhes_rotas):
    """
    Salva a solução gerada no formato esperado.
    Parâmetros:
        saida (str): Caminho do arquivo de saída
        custo_total (float): Custo total da solução
        num_rotas (int): Número de rotas
        clock_melhor_sol (int): Clock da melhor solução de referência
        ciclos_estimados (int): Ciclos estimados
        rotas, seq_ids_por_rota, demanda_rota, custo_rota, detalhes_rotas: detalhes das rotas
    """
    with open(saida, 'w', encoding='utf-8') as f:
        f.write(f"{custo_total}\n")
        f.write(f"{num_rotas}\n")
        f.write(f"{clock_melhor_sol}\n")
        f.write(f"{ciclos_estimados}\n")
        for rid, (detalhes) in enumerate(detalhes_rotas, start=1):
            f.write(detalhes + "\n")

def ler_estatisticas_csv(caminho):
    import pandas as pd
    return pd.read_csv(caminho)

def ler_intermediacao_csv(caminho):
    import pandas as pd
    return pd.read_csv(caminho)