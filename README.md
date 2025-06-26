# Projeto: Capacitated Arc Routing Problem (CARP) — Soluções Heurísticas e Metaheurísticas

Este projeto resolve o problema de roteamento de serviços em grafos (CARP - Capacitated Arc Routing Problem) utilizando heurísticas e metaheurísticas modernas. O objetivo é encontrar rotas otimizadas para veículos que devem atender demandas em vértices, arestas e arcos de um grafo, respeitando restrições de capacidade.

## Sumário

- [Descrição Geral](#descrição-geral)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Funcionalidades](#funcionalidades)
- [Como Executar](#como-executar)
- [Formato dos Arquivos](#formato-dos-arquivos)
- [Visualização e Análise](#visualização-e-análise)
- [Feedback e Contato](#Feedback-e-Contato)
- [Licença](#licença)

---

## Descrição Geral

O projeto lê instâncias do CARP a partir de arquivos `.dat`, processa cada instância com algoritmos eficientes (Clarke & Wright, GRASP, ILS), exporta as soluções em formato padronizado e permite análise comparativa e visualização gráfica dos resultados.

- **Problema resolvido:** CARP (roteamento de veículos em grafos com restrições de capacidade)
- **Abordagens:** Algoritmo de Clarke & Wright, GRASP (Greedy Randomized Adaptive Search Procedure), Iterated Local Search (ILS)
- **Resultados:** Soluções salvas em arquivos, métricas de desempenho, comparação com valores de referência, visualização gráfica

---

## Estrutura do Projeto

```
projeto-grafos/
│
├── instancias/              # Instâncias do problema (.dat)
├── resultados/              # Soluções geradas para cada instância
├── comparacao_solucoes.csv  # Comparação entre soluções obtidas e referência
├── gerar_comparacao.py      # Gera comparacao_solucoes.csv
├── grafo_utils.py           # Funções utilitárias para criação de grafos e leitura de instâncias
├── heuristica.py            # Implementação das heurísticas e metaheurísticas
├── main.py                  # Executa todas as instâncias e gera soluções
├── métricas.py              # Cálculo de métricas e propriedades dos grafos
├── README.md                # Este arquivo
├── reference_values.csv     # Valores de referência para cada instância
├── testes_unitarios.py      # Testes unitários e execução de instâncias individuais
└── visualizar.ipynb         # Notebook para visualização gráfica das soluções
```

---

## Funcionalidades

- **Leitura e processamento de instâncias** no formato `.dat`
- **Execução de heurísticas**:
  - Clarke & Wright Savings (para instâncias grandes)
  - Iterated Local Search (ILS) (refino das soluções de instâncias grandes)
  - GRASP + 2-opt (para instâncias pequenas)
- **Exportação padronizada das soluções** (incluindo rotas, custos, tempos)
- **Comparação automática** com valores de referência
- **Visualização gráfica** das soluções e métricas no notebook
- **Execução paralela** para acelerar o processamento de múltiplas instâncias
- **Testes unitários** para validação de instâncias individuais

---

## Como Executar

### 1. Navegue até o diretório do projeto

```
cd /caminho/para/seu/graph_routing_solver
```

### 2. Depêndencias

- Python 3.7+
- numpy
- psutil

```powershell
pip install numpy psutil
```

### 3. Gerar soluções para todas as instâncias

```powershell
python main.py
```

As soluções serão salvas em `resultados/`.

### 4. Executar um teste unitário em uma instância específica

```powershell
python testes_unitarios.py
# Digite o nome do arquivo .dat (ex: BHW1.dat): mggdb_0.30_19.dat
```

Digite o nome do arquivo `.dat` quando solicitado.

### 5. Gerar o arquivo de comparação

```powershell
python gerar_comparacao.py
```

Isso executa 4 testes selecionados de cada grupo de instâncias, compara com os valores de referência e gera `comparacao_solucoes.csv`.

### 6. Visualize as soluções

Abra o notebook `visualizar.ipynb` no Jupyter ou VSCode para visualizar graficamente as métricas (soluções da Etapa 1).

---

## Formato dos Arquivos

### Instâncias (`instancias/*.dat`)

Arquivos de texto estruturados contendo vértices, arestas, arcos, demandas e capacidades.

### Soluções (`resultados/sol-*.dat`)

Arquivos de texto com as rotas encontradas, custos e clocks.

### Comparação (`comparacao_solucoes.csv`)

CSV com as colunas:

- Nome da instância
- Solução de referência
- Solução obtida
- Diferença (solução de referência - solução obtida)

### Valores de referência (`reference_values.csv`)

CSV com os valores de referência para cada instância, número de rotas e métricas de tempo (valores próximo do ótimo disponibilizados pelo Docente).

---

## Visualização e Análise

- O notebook `visualizar.ipynb` vizualização em graficos e tabelas das soluções obtidas em métricas.py
- O arquivo `métricas.py` contém funções para análise estrutural dos grafos (graus, densidade, diâmetro, etc).

---

## Feedback e Contato

Para fornecer feedback ou entrar em contato, sinta-se à vontade para enviar um e-mail para

- caiofinocchio@outlook.com
- diegoalves.div@gmail.com

---

## Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.
