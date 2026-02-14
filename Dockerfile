# 1. Imagem base: Usa uma versão leve do Python 3.9
FROM python:3.9-slim

# 2. Define o diretório de trabalho dentro do container
WORKDIR /app

# 3. Instala dependências do sistema operacional (opcional, mas recomendado para evitar erros com bibliotecas gráficas)
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

# 4. Copia o arquivo de requisitos primeiro (para aproveitar o cache do Docker)
COPY requirements.txt .

# 5. Instala as bibliotecas Python
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copia o restante dos arquivos do projeto (Seu código e o Banco de Dados)
COPY PokeGraph.py .
COPY pokemon_dw.db .

# 7. Expõe a porta padrão do Streamlit
EXPOSE 8501

# 8. Configuração de saúde (Healthcheck) para o Render saber que o app está vivo
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# 9. Comando para rodar a aplicação
ENTRYPOINT ["streamlit", "run", "PokeGraph.py", "--server.port=8501", "--server.address=0.0.0.0"]
