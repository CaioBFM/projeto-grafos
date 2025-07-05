import os
import csv
from concurrent.futures import ProcessPoolExecutor
from testes_unitarios import processar_teste_unitario_automatico

# Lista de instâncias para cada cidade (4 a fim de testar soluções)
instancias = [
    # BHW
    ("BHW1.dat", "BHW1"),
    ("BHW2.dat", "BHW2"),
    ("BHW3.dat", "BHW3"),
    ("BHW4.dat", "BHW4"),
    ("BHW5.dat", "BHW5"),
    ("BHW6.dat", "BHW6"),
    ("BHW7.dat", "BHW7"),
    ("BHW8.dat", "BHW8"),
    ("BHW9.dat", "BHW9"),
    ("BHW10.dat", "BHW10"),
    ("BHW11.dat", "BHW11"),
    ("BHW12.dat", "BHW12"),
    ("BHW13.dat", "BHW13"),
    ("BHW14.dat", "BHW14"),
    ("BHW15.dat", "BHW15"),
    ("BHW16.dat", "BHW16"),
    ("BHW17.dat", "BHW17"),
    ("BHW18.dat", "BHW18"),
    ("BHW19.dat", "BHW19"),
    ("BHW20.dat", "BHW20"),
    # CBMix
    ("CBMix1.dat", "CBMix1"),
    ("CBMix2.dat", "CBMix2"),
    ("CBMix3.dat", "CBMix3"),
    ("CBMix4.dat", "CBMix4"),
    ("CBMix5.dat", "CBMix5"),
    ("CBMix6.dat", "CBMix6"),
    ("CBMix7.dat", "CBMix7"),
    ("CBMix8.dat", "CBMix8"),
    ("CBMix9.dat", "CBMix9"),
    ("CBMix10.dat", "CBMix10"),
    ("CBMix11.dat", "CBMix11"),
    ("CBMix12.dat", "CBMix12"),
    ("CBMix13.dat", "CBMix13"),
    ("CBMix14.dat", "CBMix14"),
    ("CBMix15.dat", "CBMix15"),
    ("CBMix16.dat", "CBMix16"),
    ("CBMix17.dat", "CBMix17"),
    ("CBMix18.dat", "CBMix18"),
    ("CBMix19.dat", "CBMix19"),
    ("CBMix20.dat", "CBMix20"),
    # DI-NEARP-n240
    # ("DI-NEARP-n240-Q16k.dat", "DI-NEARP-n240-Q16k"),
    # ("DI-NEARP-n240-Q2k.dat", "DI-NEARP-n240-Q2k"),
    # ("DI-NEARP-n240-Q4k.dat", "DI-NEARP-n240-Q4k"),
    # ("DI-NEARP-n240-Q8k.dat", "DI-NEARP-n240-Q8k"),
    # ("DI-NEARP-n422-Q16k.dat", "DI-NEARP-n422-Q16k"),
    # ("DI-NEARP-n422-Q2k.dat", "DI-NEARP-n422-Q2k"),
    # ("DI-NEARP-n422-Q4k.dat", "DI-NEARP-n422-Q4k"),
    # ("DI-NEARP-n422-Q8k.dat", "DI-NEARP-n422-Q8k"),
    # ("DI-NEARP-n442-Q16k.dat", "DI-NEARP-n442-Q16k"),
    # ("DI-NEARP-n442-Q2k.dat", "DI-NEARP-n442-Q2k"),
    # ("DI-NEARP-n442-Q4k.dat", "DI-NEARP-n442-Q4k"),
    # ("DI-NEARP-n442-Q8k.dat", "DI-NEARP-n442-Q8k"),
    # ("DI-NEARP-n477-Q16k.dat", "DI-NEARP-n477-Q16k"),
    # ("DI-NEARP-n477-Q2k.dat", "DI-NEARP-n477-Q2k"),
    # ("DI-NEARP-n477-Q4k.dat", "DI-NEARP-n477-Q4k"),
    # ("DI-NEARP-n477-Q8k.dat", "DI-NEARP-n477-Q8k"),
    # ("DI-NEARP-n699-Q16k.dat", "DI-NEARP-n699-Q16k"),
    # ("DI-NEARP-n699-Q2k.dat", "DI-NEARP-n699-Q2k"),
    # ("DI-NEARP-n699-Q4k.dat", "DI-NEARP-n699-Q4k"),
    # ("DI-NEARP-n699-Q8k.dat", "DI-NEARP-n699-Q8k"),
    # ("DI-NEARP-n833-Q16k.dat", "DI-NEARP-n833-Q16k"),
    # ("DI-NEARP-n833-Q2k.dat", "DI-NEARP-n833-Q2k"),
    # ("DI-NEARP-n833-Q4k.dat", "DI-NEARP-n833-Q4k"),
    # ("DI-NEARP-n833-Q8k.dat", "DI-NEARP-n833-Q8k"),
    # mggdb_0.25
    ("mggdb_0.25_1.dat", "mggdb_0.25_1"),
    ("mggdb_0.25_2.dat", "mggdb_0.25_2"),
    ("mggdb_0.25_3.dat", "mggdb_0.25_3"),
    ("mggdb_0.25_4.dat", "mggdb_0.25_4"),
    ("mggdb_0.25_5.dat", "mggdb_0.25_5"),
    ("mggdb_0.25_6.dat", "mggdb_0.25_6"),
    ("mggdb_0.25_7.dat", "mggdb_0.25_7"),
    ("mggdb_0.25_8.dat", "mggdb_0.25_8"),
    ("mggdb_0.25_9.dat", "mggdb_0.25_9"),
    ("mggdb_0.25_10.dat", "mggdb_0.25_10"),
    ("mggdb_0.25_11.dat", "mggdb_0.25_11"),
    ("mggdb_0.25_12.dat", "mggdb_0.25_12"),
    ("mggdb_0.25_13.dat", "mggdb_0.25_13"),
    ("mggdb_0.25_14.dat", "mggdb_0.25_14"),
    ("mggdb_0.25_15.dat", "mggdb_0.25_15"),
    ("mggdb_0.25_16.dat", "mggdb_0.25_16"),
    ("mggdb_0.25_17.dat", "mggdb_0.25_17"),
    ("mggdb_0.25_18.dat", "mggdb_0.25_18"),
    ("mggdb_0.25_19.dat", "mggdb_0.25_19"),
    ("mggdb_0.25_20.dat", "mggdb_0.25_20"),
    # mgval_0.25
    ("mgval_0.25_1A.dat", "mgval_0.25_1A"),
    ("mgval_0.25_1B.dat", "mgval_0.25_1B"),
    ("mgval_0.25_1C.dat", "mgval_0.25_1C"),
    ("mgval_0.25_2A.dat", "mgval_0.25_2A"),
    ("mgval_0.25_2B.dat", "mgval_0.25_2B"),
    ("mgval_0.25_2C.dat", "mgval_0.25_2C"),
    ("mgval_0.25_3A.dat", "mgval_0.25_3A"),
    ("mgval_0.25_3B.dat", "mgval_0.25_3B"),
    ("mgval_0.25_3C.dat", "mgval_0.25_3C"),
    ("mgval_0.25_4A.dat", "mgval_0.25_4A"),
    ("mgval_0.25_4B.dat", "mgval_0.25_4B"),
    ("mgval_0.25_4C.dat", "mgval_0.25_4C"),
    ("mgval_0.25_5A.dat", "mgval_0.25_5A"),
    ("mgval_0.25_5B.dat", "mgval_0.25_5B"),
    ("mgval_0.25_5C.dat", "mgval_0.25_5C"),
    ("mgval_0.25_6A.dat", "mgval_0.25_6A"),
    ("mgval_0.25_6B.dat", "mgval_0.25_6B"),
    ("mgval_0.25_6C.dat", "mgval_0.25_6C"),
]

# Carrega valores de reference_values.csv
ref_values = {}
with open("reference_values.csv", encoding="utf-8") as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        nome = row[0].strip()
        sol = row[1].replace(".", ".").replace(",", ".")
        try:
            ref_values[nome] = float(sol)
        except:
            ref_values[nome] = None

# Função para obter a primeira linha do resultado de um arquivo
def get_primeira_linha_resultado(nome):
    path = os.path.join("resultados", f"sol-{nome}")
    if not os.path.exists(path):
        return None
    with open(path, "r") as f:
        return float(f.readline().strip())

# Função principal que executa os testes unitários e gera o CSV de comparação
def main():
    resultados = []
    nomes_arquivos = [arq for arq, _ in instancias]

    # Lê soluções anteriores, se existirem
    solucao_anterior = {}
    if os.path.exists("comparacao_solucoes.csv"):
        with open("comparacao_solucoes.csv", encoding="utf-8") as f:
            try:
                reader = csv.DictReader(f)
                if reader.fieldnames and "Nome" in reader.fieldnames and "Solucao_Obtida" in reader.fieldnames:
                    for row in reader:
                        nome = row.get("Nome", None)
                        solucao_ant = row.get("Solucao_Obtida", "")
                        if nome is not None:
                            try:
                                solucao_anterior[nome] = float(solucao_ant)
                            except:
                                solucao_anterior[nome] = ""
            except Exception as e:
                pass

    with ProcessPoolExecutor() as executor:
        list(executor.map(processar_teste_unitario_automatico, nomes_arquivos))
    for arq, nome in instancias:
        sol_ref = ref_values.get(nome, None)
        sol_obt = get_primeira_linha_resultado(nome + ".dat")
        sol_ant = solucao_anterior.get(nome, "")
        if sol_ref is not None and sol_obt is not None:
            diff = sol_obt - sol_ref
        else:
            diff = ""
        resultados.append([nome, sol_ref, sol_ant, sol_obt, diff])
    with open("comparacao_solucoes.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Nome", "Solucao_Referencia", "Solucao_Obtida_Anterior", "Solucao_Obtida", "Diferenca"])
        writer.writerows(resultados)

if __name__ == "__main__":
    main()
