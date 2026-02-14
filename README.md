# 🕸️ PokeGraph: Network Evolution Analytics

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32-red)
![NetworkX](https://img.shields.io/badge/Graph_Theory-NetworkX-blueviolet)
![PyVis](https://img.shields.io/badge/Visualization-PyVis-orange)

> **Aplicação de Teoria dos Grafos** para mapear, visualizar e analisar as complexas cadeias evolutivas do universo Pokémon. Descubra "Hubs" de evolução, caminhos críticos e a topologia biológica desse ecossistema.

## 📋 Sobre o Projeto

Enquanto a maioria das análises foca em batalhas ou estatísticas individuais, o **PokeGraph** olha para as *conexões*.

Utilizando o banco de dados `pokemon_dw.db`, o projeto constrói um **Grafo Direcionado (DiGraph)** onde cada Pokémon é um Nó e cada evolução é uma Aresta. Isso permite visualizar a "Árvore da Vida" Pokémon de forma interativa e calcular métricas de centralidade para identificar quais espécies são cruciais para a diversidade genética do jogo.

---

## 🚀 Funcionalidades de Network Science

### 1. 🕸️ Visualização Interativa (PyVis)
- **Rede Dinâmica:** Renderização física onde os nós se repelem e atraem (Force Atlas 2), permitindo arrastar, dar zoom e explorar a teia de evoluções.
- **Tooltips:** Ao passar o mouse sobre uma conexão, o sistema revela o **Gatilho** da evolução (Nível, Pedra, Item, Felicidade).

### 2. 📐 Métricas de Grafo (NetworkX)
- **Degree Centrality (Hubs):** Identifica automaticamente o Pokémon com maior número de ramificações (Historicamente: *Eevee* e *Tyrogue*).
- **Longest Path (Caminho Crítico):** Algoritmo que encontra a maior cadeia evolutiva sequencial sem ciclos.

### 3. 📊 Análise de Gatilhos
- **Ranking de Métodos:** Gráfico de barras que quantifica quais são os métodos de evolução mais comuns (Level Up vs Pedras vs Trocas).

### 4. 🎨 UX Refinada
- **Dark Mode Support:** Injeção de CSS personalizado para garantir que métricas e textos sejam legíveis independentemente do tema do usuário.

---

## 🛠️ Tecnologias Utilizadas

* **[Streamlit](https://streamlit.io/):** Framework web.
* **[NetworkX](https://networkx.org/):** Motor de cálculo matemático para grafos e redes complexas.
* **[PyVis](https://pyvis.readthedocs.io/):** Biblioteca para gerar visualizações de redes em HTML/Canvas interativo.
* **[Pandas & SQLite](https://pandas.pydata.org/):** Manipulação de dados relacionais.

---

## 📦 Como Rodar o Projeto

### Pré-requisitos
⚠️ **Importante:** Você precisa ter o arquivo `pokemon_dw.db` na raiz do projeto (gerado pelo seu script de ETL).

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/SEU-USUARIO/pokegraph-analytics.git](https://github.com/SEU-USUARIO/pokegraph-analytics.git)
    cd pokegraph-analytics
    ```

2.  **Instale as dependências:**
    ```bash
    pip install streamlit pandas networkx pyvis
    ```

3.  **Execute o Dashboard:**
    ```bash
    streamlit run pokegraph.py
    ```

---

## 📂 Estrutura de Arquivos

---

## 🧠 Insights de Topologia

Ao explorar o grafo, notamos padrões interessantes de Game Design:
1.  **Linearidade Predominante:** A vasta maioria dos grafos são componentes desconexos lineares de tamanho 2 ou 3 (Ex: *Charmander -> Charmeleon -> Charizard*).
2.  **O Fenômeno Eevee:** O nó "Eevee" atua como um *Star Graph* (Grafo Estrela), sendo um outlier estatístico com altíssima centralidade de saída.
3.  **Complexidade Crescente:** Nas gerações mais recentes, o grafo se torna mais denso com evoluções cruzadas e regionais (Ex: *Slowpoke* evoluindo para *Slowbro* ou *Slowking*).

---

## 🤝 Contribuição

Quer adicionar sprites dos Pokémon nos nós do grafo?

1.  Faça um Fork.
2.  Crie sua Feature Branch.
3.  Commit e Push.
4.  Abra um Pull Request.

---
**Connecting the dots... literally.** 🕸️
