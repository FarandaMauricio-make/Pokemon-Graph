import streamlit as st
import networkx as nx
from pyvis.network import Network
import streamlit.components.v1 as components
from collections import Counter
import tempfile
import pandas as pd
import sqlite3
import os

# ==============================================================================
# 1. CONFIGURAÇÃO E ESTÉTICA DA PÁGINA
# ==============================================================================
st.set_page_config(
    page_title="PokeGraph: A Rede da Evolução",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CORREÇÃO DO CSS ---
# Adicionei 'color: #0e1117' (preto/cinza escuro) forçado nos elementos de texto
# para garantir contraste mesmo se o usuário estiver usando Dark Mode.
st.markdown("""
    <style>
    /* Estilo para cartões de métricas */
    div[data-testid="stMetric"] {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #d6d6d6;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
    }
    
    /* Força a cor do texto para preto/escuro dentro dos cartões */
    div[data-testid="stMetric"] label, 
    div[data-testid="stMetric"] div[data-testid="stMetricValue"],
    div[data-testid="stMetric"] div[data-testid="stMetricDelta"] {
        color: #0e1117 !important;
    }

    .big-font { font-size:20px !important; }
    </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# 2. CARREGAMENTO DE DADOS
# ==============================================================================
@st.cache_data
def get_data():
    # Caminho absoluto para local
    db_path_local = r'G:\Meu Drive\Projetos\Poke_projeto\Pokemao\pokemon_dw.db'
    
    # Estratégia de Deploy
    if os.path.exists(db_path_local):
        db_file = db_path_local
    elif os.path.exists('pokemon_dw.db'):
        db_file = 'pokemon_dw.db'
    else:
        return pd.DataFrame()

    try:
        conn = sqlite3.connect(db_file)
        query = """
        SELECT 
            from_species, 
            to_species, 
            trigger, 
            min_level, 
            item, 
            time_of_day
        FROM evolution
        """
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Ocorreu um erro na conexão com o banco: {e}")
        return pd.DataFrame()

# ==============================================================================
# 3. INTERFACE: SIDEBAR
# ==============================================================================
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/9/98/International_Pokémon_logo.svg", width=200)
    st.title("Sobre o Projeto")
    st.markdown("""
    Este projeto utiliza **Teoria dos Grafos** para mapear as complexas relações evolutivas do universo Pokémon.
    
    **Técnicas Usadas:**
    - 🐍 Python & Streamlit
    - 🕸️ NetworkX (Cálculos de Grafo)
    - 🎨 PyVis (Visualização Interativa)
    - 🗄️ SQL & Pandas (ETL de Dados)
    """)
    
    st.divider()
    
    df_evolucoes = get_data()
    if not df_evolucoes.empty:
        st.success(f"Banco conectado! {len(df_evolucoes)} evoluções carregadas.")
    else:
        st.error("Banco de dados não encontrado.")

# ==============================================================================
# 4. PROCESSAMENTO DOS DADOS
# ==============================================================================
if df_evolucoes.empty:
    st.warning("⚠️ Usando dados de exemplo para demonstração visual.")
    dados_grafico = [
        ("Bulbasaur", "Ivysaur", "Lvl 16"),
        ("Ivysaur", "Venusaur", "Lvl 32"),
        ("Charmander", "Charmeleon", "Lvl 16"),
        ("Charmeleon", "Charizard", "Lvl 36")
    ]
else:
    dados_grafico = []
    for index, row in df_evolucoes.iterrows():
        origem = str(row['from_species']).title()
        destino = str(row['to_species']).title()
        
        gatilho_texto = row['trigger']
        
        if row['trigger'] == 'level-up' and pd.notna(row['min_level']):
            gatilho_texto = f"Lvl {int(row['min_level'])}"
        elif pd.notna(row['item']) and row['item'] != '':
            gatilho_texto = f"Item: {row['item']}"
        
        if pd.notna(row['time_of_day']) and row['time_of_day'] != '':
             gatilho_texto += f" ({row['time_of_day']})"
             
        dados_grafico.append((origem, destino, gatilho_texto))

# ==============================================================================
# 5. CONSTRUÇÃO DO GRAFO
# ==============================================================================
G = nx.DiGraph()
for origem, destino, gatilho in dados_grafico:
    G.add_edge(origem, destino, title=str(gatilho)) 

# ==============================================================================
# 6. STORYTELLING PRINCIPAL
# ==============================================================================

st.title("🕸️ A Teia da Evolução Pokémon")
st.markdown("""
> *"Pokémon não é apenas batalha, é metamorfose."* > Abaixo, visualizamos essas transformações como uma **Rede Complexa**. 
> Cada nó é uma espécie, cada aresta é o caminho para se tornar algo mais forte.
""")

tab1, tab2 = st.tabs(["🔍 Explorador Interativo", "📊 Análise de Dados"])

# --- ABA 1: O GRAFO VISUAL ---
with tab1:
    st.subheader("Mapa de Interações")
    st.caption("Dica: Arraste os nós, faça zoom com o scroll e passe o mouse nas setas para ver como evoluir.")
    
    def visualizar_rede(graph):
        # bgcolor ajustado para um cinza escuro elegante
        net = Network(height="600px", width="100%", bgcolor="#1A1A1A", font_color="white", directed=True)
        net.from_nx(graph)
        
        net.set_options("""
        var options = {
          "physics": {
            "forceAtlas2Based": {
              "gravitationalConstant": -50,
              "centralGravity": 0.005,
              "springLength": 100,
              "springConstant": 0.08
            },
            "minVelocity": 0.75,
            "solver": "forceAtlas2Based"
          }
        }
        """)
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp:
            net.save_graph(tmp.name)
            return tmp.name

    if G.number_of_nodes() > 0:
        path_html = visualizar_rede(G)
        with open(path_html, 'r', encoding='utf-8') as f:
            source_code = f.read() 
        components.html(source_code, height=620)
    else:
        st.info("Grafo vazio.")

# --- ABA 2: INSIGHTS E MÉTRICAS ---
with tab2:
    st.header("Por trás dos Números")
    st.markdown("Aqui aplicamos métricas de centralidade e contagem para entender padrões de game design.")
    
    num_nodes = G.number_of_nodes()
    num_edges = G.number_of_edges()
    
    try:
        caminho_longo = nx.dag_longest_path(G)
        tam_caminho = len(caminho_longo)
        texto_caminho = " ➡ ".join(caminho_longo)
    except:
        tam_caminho = 0
        texto_caminho = "N/A (Ciclo detectado)"

    if num_nodes > 0:
        centralidade = nx.degree_centrality(G)
        top_node = max(centralidade, key=centralidade.get)
        conexoes_top = len(list(G.neighbors(top_node)))
    else:
        top_node = "N/A"
        conexoes_top = 0

    col_metric1, col_metric2, col_metric3 = st.columns(3)
    col_metric1.metric(label="Total de Espécies", value=num_nodes)
    col_metric2.metric(label="Total de Evoluções", value=num_edges)
    col_metric3.metric(label="Maior Ramificação (Hub)", value=top_node, delta=f"{conexoes_top} conexões")

    st.divider()

    col_chart1, col_chart2 = st.columns([2, 1])

    with col_chart1:
        st.subheader("🧬 A Maior Cadeia Evolutiva")
        st.info(f"A sequência mais longa possui **{tam_caminho} estágios**: \n\n {texto_caminho}")
        
        st.markdown("### 🏆 Gatilhos Mais Comuns")
        if num_edges > 0:
            gatilhos = [G[u][v].get('title', 'Desconhecido') for u, v in G.edges()]
            contagem = Counter(gatilhos)
            
            df_chart = pd.DataFrame.from_dict(contagem, orient='index', columns=['contagem'])
            df_chart = df_chart.sort_values(by='contagem', ascending=False).head(10)
            st.bar_chart(df_chart)

    with col_chart2:
        st.markdown("""
        ### 💡 Insights
        
        **Sobre Centralidade:**
        O Pokémon com maior centralidade (Hub) representa a família com mais opções evolutivas. 
        Historicamente, **Eevee** domina essa métrica devido às suas múltiplas "eeveelutions".
        
        **Sobre Gatilhos:**
        Analisando o gráfico de barras, nota-se que o *Level Up* é o mecanismo padrão, 
        mas *Itens* (pedras) são fundamentais para diversificar a árvore.
        """)