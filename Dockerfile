# 1. Imagem base
FROM python:3.9-slim

# 2. Diretório de trabalho
WORKDIR /app

# 3. Copia e instala as dependências Python
# (Removemos o apt-get update pois as bibliotecas modernas não precisam mais dele)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copia o código e o banco
COPY PokeGraph.py .
COPY pokemon_dw.db .

# 5. Expõe a porta
EXPOSE 8501

# 6. Comando de execução
ENTRYPOINT ["streamlit", "run", "PokeGraph.py", "--server.port=8501", "--server.address=0.0.0.0"]
