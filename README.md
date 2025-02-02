# 🥋 Torneio de Karatê

Bem-vindo ao sistema de gestão do **Torneio de Karatê**! Este projeto foi desenvolvido para:
- Atletas:
   - Com o objetivo de facilitar aos competidores ver de maneira fácil o número e o local das suas lutas.
- Academias:
   - Para  possam avaliar suas chances no campeonato.
- Federação e Equipe de Organização do Evento:
   - Gerenciar os dados de participantes, academias, categorias, confrontos e estatísticas detalhadas do torneio. 

A interface é interativa, simples e eficiente, construída com **Streamlit**.

## 🚀 Funcionalidades

- **Visualização de Dados**: Explore informações completas sobre os participantes, como atletas, academias e categorias.
- **Filtros Personalizados**: Selecione dados por modalidade (Kata ou Luta), academia ou atleta.
- **Estatísticas do Torneio**:
  - Total de atletas e academias.
  - Distribuição por faixa etária e graduação.
  - Gênero e categorias.
  - Confrontos entre academias.
- **Botão de Navegação**: Localize o endereço do evento diretamente no Google Maps.

## 🛠️ Tecnologias Utilizadas

- **Linguagem**: Python 🐍
- **Framework de Interface**: Streamlit
- **Framework de Backend**: SQLAlchemy
- **Banco de Dados**: PostgreSQL
- **Manipulação de Dados**: Pandas, Faker, itertools
- **Deploy**: Streamlit Cloud, Docker e Render
- **Ambiente de Configuração**: dotenv

## 📂 Estrutura do Projeto

O projeto segue a seguinte estrutura:

```plaintext
├── app.py                     # Arquivo principal: Interface Streamlit para interação com o sistema
├── backend/                   # Contém arquivos relacionados à conexão e lógica de backend
│   ├── __init__.py            # Arquivo de inicialização do pacote backend
│   ├── conexao_db.py          # Script para conexão ao banco de dados
|   ├── src/                   # Diretório para processamento e anonimização de dados
│     ├── etl.py               # Script de ETL (Extração, Transformação e Carga) dos dados
|   ├── models/                # Diretório para modelos e funções auxiliares
|     ├── atletas_luta_kata.py # Definições de modelos e funções relacionadas a Luta e Kata
├── .gitignore                 # Arquivo para ignorar arquivos e diretórios desnecessários no Git
├── poetry.lock                # Arquivo de bloqueio de dependências do projeto gerado pelo Poetry
├── pyproject.toml             # Arquivo de configuração do Poetry com as dependências do projeto
├── requirements.txt           # Lista de dependências para instalação com `pip`
├── README.md                  # Contendo todas as informações sobre o Projeto
└── Dockerfile                 # Arquivo de configuração para containerização com Docker
```

## ⚙️ Como Funciona

1. **Anonimização dos Dados**: O sistema processa os dados de atletas e academias, substituindo informações reais por dados fictícios utilizando a biblioteca `Faker`.
2. **ETL (Extract, Transform, Load)**:
   - Extrai os dados de planilhas do Excel.
   - Transforma os dados com estruturação e limpeza.
   - Carrega os dados no banco PostgreSQL.
3. **Interface**:
   - Permite filtragem e visualização interativa.
   - Gera tabelas e estatísticas do torneio.
4. **Deploy**:
   - Projeto configurado com Docker para fácil distribuição e implantação em ambientes remotos.

## 🏟️ Informações do Evento

- **Data**: 08/02/2025  
- **Horário**: A partir das 09:00h  
- **Local**: Ginásio de Esportes Gurizão  
- **Endereço**: R. São João, 1042 – Santa Terezinha, Fazenda Rio Grande – PR, 83829-248  
- **Mapa**: [Abrir no Google Maps](https://www.google.com/maps/search/?api=1&query=R.+São+João,+1042+–+Santa+Terezinha,+Fazenda+Rio+Grande+–+PR,+83829-248)

## 📦 Como Executar o Projeto

### 1. Usando Python/Pip diretamente

1. **Clone o Repositório**:
   ```bash
   git clone https://github.com/seu-usuario/torneio-karate.git
   cd torneio-karate
   ```

2. **Configure as Variáveis de Ambiente**:
   Crie um arquivo `.env` na raiz com as seguintes variáveis:
   ```env
   DB_HOST=seu_host
   DB_DATABASE=seu_banco
   DB_USER=seu_usuario
   DB_PASSWORD=sua_senha
   ```

3. **Instale as Dependências**:
   ```bash
   poetry install
   ```

4. **Execute a Aplicação**:
   ```bash
   streamlit run app.py
   ```

5. **Acesse no Navegador**:
   - URL: [http://localhost:8501](http://localhost:8501)

### 2. Usando Docker 🐳

1. **Clone o Repositório**:
   ```bash
   git clone https://github.com/seu-usuario/torneio-karate.git
   cd torneio-karate
   ```

2. **Configure as Variáveis de Ambiente**:
   Crie um arquivo `.env` na raiz com as seguintes variáveis:
   ```env
   DB_HOST=seu_host
   DB_DATABASE=seu_banco
   DB_USER=seu_usuario
   DB_PASSWORD=sua_senha
   ```

3. **Construa a Imagem Docker**:
   ```bash
   docker build -t app-karate .
   ```

4. **Execute o Container**:
   ```bash
   docker run -p 8501:8501 --env-file .env app-karate
   ```

5. **Acesse no Navegador**:
   - URL: [http://localhost:8501](http://localhost:8501)

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests. 💡


## 📞 Contato

**Desenvolvido por Guilherme Canfield de Almeida**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Guilherme%20Canfield-blue?style=flat&logo=linkedin)](https://www.linkedin.com/in/guilhermecanfield/)
[![Portfólio](https://img.shields.io/badge/Portf%C3%B3lio-Guilherme%20Canfield-orange?style=flat&logo=google)](https://sites.google.com/view/guilhermecanfield/)
[![Gmail](https://img.shields.io/badge/Email-guilherme.canfield87%40gmail.com-red?style=flat&logo=gmail)](mailto:guilherme.canfield87@gmail.com)
[![WhatsApp](https://img.shields.io/badge/WhatsApp-55%2041%20984805004-brightgreen?style=flat&logo=whatsapp)](https://wa.me/5541984805004)