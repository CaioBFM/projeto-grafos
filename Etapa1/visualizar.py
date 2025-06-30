import importlib
import métricas as métricas
importlib.reload(métricas)
from métricas import *
from IPython.display import display, clear_output, HTML
import numpy as np
import pandas as pd
import os
import ipywidgets as widgets

# Função de visualização: criar tabela do grafo
def criar_tabela_grafo(grafo):
    if grafo is None or not hasattr(grafo, 'shape') or len(grafo.shape) != 2:
        print("Grafo não carregado corretamente ou está vazio.")
        return None
    grafo_ajustado = np.array(grafo)[1:, 1:]
    n_vertices = grafo_ajustado.shape[0]
    if n_vertices <= 30:
        cell_width = '25px'
        font_size = '9pt'
    elif n_vertices <= 100:
        cell_width = '15px'
        font_size = '8pt'
    else:
        cell_width = '10px'
        font_size = '7pt'
    df = pd.DataFrame(
        grafo_ajustado,
        index=range(1, n_vertices + 1),
        columns=range(1, n_vertices + 1)
    )
    def format_value(x):
        if pd.isna(x):
            return "-"
        elif np.isinf(x):
            return "∞"
        elif isinstance(x, (int, np.integer)):
            return str(x)
        elif isinstance(x, (float, np.floating)):
            return f"{x:.2f}" if not x.is_integer() else str(int(x))
        return str(x)
    def background_style(x):
        return 'background-color: #e6f3ff' if x != 0 and not np.isinf(x) else 'background-color: white'
    styled_table = (
        df.style
        .map(background_style)
        .format(format_value)
        .set_properties(**{
            'text-align': 'center',
            'font-size': font_size,
            'padding': '2px',
            'border': '1px solid #ddd',
            'width': cell_width,
            'height': cell_width
        })
        .set_table_styles([{
            'selector': 'table',
            'props': [
                ('width', 'auto'),
                ('margin', '0 auto'),
                ('display', 'block' if n_vertices > 100 else 'inline-block'),
                ('max-width', '100%'),
                ('overflow-x', 'auto' if n_vertices > 100 else 'visible')
            ]
        }, {
            'selector': 'th, td',
            'props': [('max-width', cell_width)]
        }])
    )
    return styled_table

def criar_tabela_grafo_scroll(grafo):
    tabela = criar_tabela_grafo(grafo)
    return tabela.set_table_attributes('style="display:block;overflow-x:auto;max-width:100%;"')

def componentes_conectados(grafo):
    n = grafo.shape[0] - 1
    visitados = set()
    componentes = 0
    for v in range(1, n+1):
        if v not in visitados:
            fila = [v]
            while fila:
                u = fila.pop()
                if u not in visitados:
                    visitados.add(u)
                    vizinhos = [i for i in range(1, n+1) if grafo[u][i] < np.inf and u != i]
                    fila.extend([w for w in vizinhos if w not in visitados])
            componentes += 1
    return componentes

def formatar_valor(v):
    if isinstance(v, float):
        if v.is_integer():
            return f"{int(v)}"
        else:
            return f"{v:.1f}"
    return v

def mostrar_metricas_grafo(dados, grafo):
    # 1. Quantidade de vértices
    qtd_vertices = dados['qtd_vertices']
    # 2. Quantidade de arestas
    qtd_arestas = len(dados['arestas']) + len(dados['arestas_req'])
    # 3. Quantidade de arcos
    qtd_arcos = len(dados['arcos']) + len(dados['arcos_req'])
    # 4. Quantidade de vértices requeridos
    qtd_vertices_req = len(set(
        [i for (i, _, *_) in dados['arestas_req']] +
        [j for (_, j, *_) in dados['arestas_req']] +
        [i for (i, _, *_) in dados['arcos_req']] +
        [j for (_, j, *_) in dados['arcos_req']]
    ))
    # 5. Quantidade de arestas requeridas
    qtd_arestas_req = len(dados['arestas_req'])
    # 6. Quantidade de arcos requeridos
    qtd_arcos_req = len(dados['arcos_req'])
    # 7. Densidade do grafo
    dens = densidade(qtd_vertices, len(dados['arestas']) + len(dados['arestas_req']),
                     len(dados['arcos']) + len(dados['arcos_req']))
    # 8. Componentes conectados
    try:
        n_componentes = componentes_conectados(grafo)
    except Exception:
        n_componentes = "Função não implementada"
    # 9. Grau mínimo dos vértices
    graus = calcula_graus(dados)
    grau_min = min([g[4] for g in graus])
    # 10. Grau máximo dos vértices
    grau_max = max([g[4] for g in graus])
    # 11. Intermediação
    try:
        vertices = list(range(1, qtd_vertices+1))
        intermediacao = calcula_intermediacao(vertices, grafo)
    except Exception:
        intermediacao = {}
    # 12. Caminho médio
    try:
        distancias, _ = floyd_warshall(grafo)
        caminho_medio_val = caminho_medio(distancias)
    except Exception:
        caminho_medio_val = "Função não implementada"
    # 13. Diâmetro
    try:
        diametro_val = diametro(distancias)
    except Exception:
        diametro_val = "Função não implementada"

    estatisticas = {
        'Qtd. Vértices': qtd_vertices,
        'Qtd. Arestas': qtd_arestas,
        'Qtd. Arcos': qtd_arcos,
        'Qtd. Vértices Requeridos': qtd_vertices_req,
        'Qtd. Arestas Requeridas': qtd_arestas_req,
        'Qtd. Arcos Requeridos': qtd_arcos_req,
        'Densidade': dens,
        'Componentes Conectados': n_componentes,
        'Grau Mínimo': grau_min,
        'Grau Máximo': grau_max,
        'Caminho Médio': caminho_medio_val,
        'Diâmetro': diametro_val
    }
    df_est = pd.DataFrame(
        [(k, formatar_valor(v)) for k, v in estatisticas.items()],
        columns=['Métrica', 'Valor']
    )
    display(HTML("<h4>Métricas do Grafo</h4>"))
    display(df_est.style.set_properties(**{'width': '300px'}))

    display(HTML("<h4>Intermediação dos Vértices</h4>"))
    if intermediacao:
        df_inter = pd.DataFrame(list(intermediacao.items()), columns=['Vértice', 'Intermediação'])
        display(df_inter.style.set_properties(**{'width': '300px'}))

    display(HTML("<h4>Matriz de Adjacência</h4>"))
    display(criar_tabela_grafo_scroll(grafo))

def painel_visualizacao():
    dat_files = sorted([f for f in os.listdir('../Etapas2e3/instancias') if f.endswith('.dat')])
    def default_file():
        return 'BHW4.dat' if 'BHW4.dat' in dat_files else dat_files[0]
    file_selector = widgets.Dropdown(
        options=dat_files,
        value=default_file(),
        description='Arquivo:',
        disabled=False,
    )
    output = widgets.Output()
    def atualizar_visualizacao(change):
        with output:
            clear_output(wait=True)
            arquivo = file_selector.value
            with open(f'../Etapas2e3/instancias/{arquivo}', 'r', encoding='utf-8') as f:
                linhas = f.readlines()
            dados = extrair_dados_instancia(linhas)
            grafo = dados['grafo']
            mostrar_metricas_grafo(dados, grafo)
    file_selector.observe(atualizar_visualizacao, names='value')
    display(file_selector, output)
    atualizar_visualizacao(None)
