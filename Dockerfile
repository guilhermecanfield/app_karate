FROM python:3.12-slim

WORKDIR /app

# Instalar dependências do sistema - agora precisamos de menos dependências
RUN apt-get update && apt-get install -y \
    build-essential \
    curl

# Instalar o Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Garantir que o Poetry esteja no PATH
ENV PATH="/root/.local/bin:$PATH"

# Configurar o Poetry para criar o ambiente virtual no diretório do projeto
RUN poetry config virtualenvs.in-project true

# Copiar dependências do projeto
COPY pyproject.toml poetry.lock /app/

# Instalar dependências do Poetry
RUN poetry install --no-interaction --no-ansi --no-root

# Copiar o código da aplicação
COPY . /app/

# Expor a porta do Streamlit
EXPOSE 8501

# Comando para iniciar o Streamlit usando poetry run
ENTRYPOINT ["poetry", "run"]
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=localhost"]