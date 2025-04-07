# Análise e Processamento de Grafos a partir de Arquivos `.dat`

Este projeto em Python foi desenvolvido com o objetivo de **ler, modelar e analisar estruturas de grafos complexos**, extraídos a partir de arquivos `.dat`. A partir do grafo construído, o código realiza o **cálculo de métricas importantes** da Teoria dos Grafos.

## Funcionalidades

- **Leitura estruturada de arquivos `.dat`** leitura de vértices, arestas, arcos e demandas;
- Construção de um **grafo representado como matriz de adjacência (usando `numpy`)**;
- **Cálculo da densidade do grafo** considerando ligações direcionadas e bidirecionais;
- **Cálculo de graus dos vértices**, cálculo do grau mínimo e máximo dos vértices;
- **Escolha adaptativa entre os algoritmos de Dijkstra e Floyd-Warshall** com base na densidade do grafo;
- **Cálculo do diâmetro do grafo** e do **caminho médio** entre os pares de vértices;
- **Reconstrução de caminhos mínimos** entre pares de vértices;
- **Cálculo da intermediação dos vértices** quantas vezes um vértice aparece em caminhos mínimos entre todos os pares.

## 📁 Estrutura do Código

- `ler_arquivo()`: Realiza o parsing detalhado do arquivo `.dat` e extrai todas as estruturas relevantes do grafo.
- `densidade()`: Calcula a densidade do grafo considerando arcos e arestas.
- `calcula_graus()`: Analisa os graus dos vértices em diferentes perspectivas.
- `dijkstra()` / `floyd_warshall()`: Implementações clássicas para o cálculo de caminhos mínimos.
- `caminho_medio()` e `diametro()`: Métricas globais de conectividade.
- `reconstruir_caminho()`: Recompõe um caminho mínimo usando predecessores.
- `calcula_intermediacao()`: Mede a importância dos vértices como intermediários em caminhos mínimos.
- `main()`: Interface principal com o usuário, leitura do arquivo e chamada dos cálculos.

## 🛠️ Requisitos

- Python 3.7+
- Bibliotecas:
  - `numpy`
  - `heapq` (padrão do Python)

Instale as dependências com:

```bash
pip install numpy
```
## Como usar

1. Coloque o arquivo `.dat` contendo a definição do grafo no mesmo diretório do script.
2. Execute o script principal com:

```bash
python projeto1.py
```

3. Siga as instruções no terminal:
   - Insira o nome do arquivo `.dat` quando solicitado.
   - O programa realizará a leitura e o processamento dos dados.
   - As métricas e estatísticas do grafo serão exibidas em sequência.

## 📊 Exemplo de Saída

```bash
Digite o nome do arquivo (ex: nome_arquivo.dat):

- ESTATÍSTICAS BÁSICAS DO GRAFO:
- Quantidade de vértices: 12
- Quantidade de arestas: 11
- Quantidade de arcos: 22
- Quantidade de vértices requeridos: 7
- Quantidade de arestas requeridas: 11
- Quantidade de arcos requeridos: 11
- Densidade do grafo: 0.1667
- Grau total mínimo: 4
- Grau total máximo: 3
- Caminho médio: 16.7121
- Diâmetro do grafo: 30

- INTERMEDIAÇÃO DOS VÉRTICES:
- Vértice 1: 18
- Vértice 2: 22
- Vértice 3: 6
- Vértice 4: 0
- Vértice 5: 14
- Vértice 6: 38
- Vértice 7: 22
- Vértice 8: 16
- Vértice 9: 14
- Vértice 10: 6
- Vértice 11: 0
- Vértice 12: 22
```

## Estratégia de Escolha do Algoritmo

O algoritmo de caminhos mínimos é escolhido com base na **densidade do grafo**:

- Se a densidade for **maior que 0.5**, utiliza-se **Floyd-Warshall**, eficiente para grafos densos.
- Caso contrário, aplica-se **Dijkstra com fila de prioridade**, ideal para grafos esparsos.

## Observações Adicionais

- A reconstrução dos caminhos mínimos requer a matriz de predecessores calculada durante os algoritmos.
- Apenas pesos positivos são considerados nos arcos e arestas.
- A centralidade de intermediação pode demandar tempo significativo em grafos grandes, pois envolve a análise de todos os pares de vértices.
