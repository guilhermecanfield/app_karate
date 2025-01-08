# 🥋 Torneio de Karatê

Bem-vindo ao sistema de gestão do **Torneio de Karatê**! Este projeto foi desenvolvido para gerenciar os dados de participantes, academias, categorias e confrontos, além de fornecer estatísticas detalhadas do torneio. A interface é interativa, simples e eficiente, construída com **Streamlit**.

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
- **Banco de Dados**: PostgreSQL
- **Manipulação de Dados**: Pandas, Faker, itertools
- **Deploy**: Docker e Render
- **Ambiente de Configuração**: dotenv

## 📂 Estrutura do Projeto

```plaintext
├── app.py                     # Interface Streamlit
├── backend/
│   ├── __init__.py
│   ├── etl.py                 # Processamento e anonimização de dados
│   ├── src.py                 # Funções auxiliares
├── data/
│   ├── kata/                  # Dados brutos de Kata
│   ├── luta/                  # Dados brutos de Luta
├── requirements.txt           # Dependências do projeto
└── Dockerfile                 # Configuração para containerização
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
   pip install -r requirements.txt
   ```

4. **Execute a Aplicação**:
   ```bash
   streamlit run app.py
   ```

5. **Acesse no Navegador**:
   - URL: [http://localhost:8501](http://localhost:8501)

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests. 💡

---

**Desenvolvido com 💻 e 🥋 por [Seu Nome]**