import os
import csv
from concurrent.futures import ProcessPoolExecutor
from testes_unitarios import processar_teste_unitario_automatico

# Lista de instâncias para cada cidade (4 a fim de testar soluções)
instancias = [
    ("BHW1.dat", "BHW1"),
    ("BHW2.dat", "BHW2"),
    ("BHW3.dat", "BHW3"),
    ("BHW4.dat", "BHW4"),
    ("CBMix1.dat", "CBMix1"),
    ("CBMix2.dat", "CBMix2"),
    ("CBMix3.dat", "CBMix3"),
    ("CBMix4.dat", "CBMix4"),
    ("DI-NEARP-n240-Q16k.dat", "DI-NEARP-n240-Q16k"),
    ("DI-NEARP-n240-Q2k.dat", "DI-NEARP-n240-Q2k"),
    ("DI-NEARP-n240-Q4k.dat", "DI-NEARP-n240-Q4k"),
    ("DI-NEARP-n240-Q8k.dat", "DI-NEARP-n240-Q8k"),
    ("mggdb_0.25_1.dat", "mggdb_0.25_1"),
    ("mggdb_0.25_2.dat", "mggdb_0.25_2"),
    ("mggdb_0.25_3.dat", "mggdb_0.25_3"),
    ("mggdb_0.25_4.dat", "mggdb_0.25_4"),
    ("mgval_0.25_1A.dat", "mgval_0.25_1A"),
    ("mgval_0.25_1B.dat", "mgval_0.25_1B"),
    ("mgval_0.25_1C.dat", "mgval_0.25_1C"),
    ("mgval_0.25_2A.dat", "mgval_0.25_2A"),
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
    with ProcessPoolExecutor() as executor:
        list(executor.map(processar_teste_unitario_automatico, nomes_arquivos))
    for arq, nome in instancias:
        sol_ref = ref_values.get(nome, None)
        sol_obt = get_primeira_linha_resultado(nome + ".dat")
        if sol_ref is not None and sol_obt is not None:
            diff = sol_obt - sol_ref
        else:
            diff = ""
        resultados.append([nome, sol_ref, sol_obt, diff])
    with open("comparacao_solucoes.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Nome", "Solucao_Referencia", "Solucao_Obtida", "Diferenca"])
        writer.writerows(resultados)

if __name__ == "__main__":
    main()
