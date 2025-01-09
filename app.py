import streamlit as st
import pandas as pd
from itertools import combinations
from backend.conexao import ler_dados, get_engine
import os
from dotenv import load_dotenv

# Configurar estilo personalizado
st.set_page_config(
    page_title="Torneio de Karatê",
    page_icon="🥋",
    layout="wide",
    initial_sidebar_state="auto"
)


# CSS personalizado com cores de texto ajustadas
st.markdown("""
    <style>
        /* Estilo para títulos */
        h1 {
            color: #D0312D;
            padding: 20px 0;
            text-shadow: 1px 1px 1px rgb(249, 249, 249);
        }
        h2 {
            color: #bab4af;
            padding: 15px 0;
        }
        h3 {
            color: #333333;
        }
        
        /* Estilo para cards */
        .stcard {
            background-color: white;
            padding: 3px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin: 10px 0;
            color: #333333;
        }
        
        /* Estilo para estatísticas */
        .metric-card {
            background-color: #f8f9fa;
            padding: 5px;
            border-radius: 8px;
            border-left: 4px solid #D0312D;
            margin: 10px 0;
            color: #333333;
            font-weight: bold !important;
        }
        
        /* Estilo para o botão do Google Maps */
        .maps-button {
            background-color: #D0312D;
            color: white;
            padding: 10px 20px;
            border-radius: 5px;
            border: none;
            cursor: pointer;
            transition: background-color 0.3s;
        }
        .maps-button:hover {
            background-color: #B02825;
        }
        
        /* Estilo para tabelas */
        .dataframe {
            font-size: 14px !important;
            color: #333333 !important;
        }
        
        /* Estilo para filtros */
        .stSelectbox, .stMultiSelect {
            margin-bottom: 15px;
            color: #333333;
        }

        /* Garantir que todo texto em containers tenha cor escura */
        .stcard p, .stcard span, .stcard td, .stcard th {
            color: #333333 !important;
        }
        
        /* Estilo específico para elementos dentro de containers */
        div[data-testid="stVerticalBlock"] {
            color: #f9f9f9 !important;
            font-weight: bold !important;
        }
    </style>
""", unsafe_allow_html=True)

@st.cache_resource
def init_connection():
    load_dotenv()
    return get_engine()

@st.cache_data
def get_data():
    try:
        return ler_dados()
    except Exception as e:
        st.error(f"Erro ao ler dados do banco: {e}")
        return pd.DataFrame()

@st.cache_data
def load_data(estilo):
    df = get_data()
    if df.empty:
        return df
    return df[df.estilo == estilo.title()]

# Inicializar conexão
engine = init_connection()

# Header da aplicação
st.markdown("<h1 style='text-align: center;'>🥋 Torneio de Karatê</h1>", unsafe_allow_html=True)

# Banner
image_url = "https://cdn.leonardo.ai/users/2a909725-4edc-44d7-b332-54400832d020/generations/e8f640d2-754d-4843-841d-556f67a949d5/Leonardo_Phoenix_09_A_vibrant_and_dynamic_banner_announcing_a_2.jpg"
st.markdown(
    f"""
    <div style='display: flex; justify-content: center; margin: 20px 0 30px 0;'>
        <img src="{image_url}" width="300" style="border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
    </div>
    """,
    unsafe_allow_html=True
)

# Container de informações
with st.container():
    st.markdown("""
        <div class="stcard">
            <h2 style='margin-top: 0;'>ℹ️ Informações do Evento</h2>
            <table style="width: 100%">
                <tr>
                    <td style="padding: 8px; width: 150px;"><strong>Data:</strong></td>
                    <td>08/02/2025</td>
                </tr>
                <tr>
                    <td style="padding: 8px;"><strong>Horário:</strong></td>
                    <td>A partir das 09:00h</td>
                </tr>
                <tr>
                    <td style="padding: 8px;"><strong>Local:</strong></td>
                    <td>Ginásio de Esportes Gurizão</td>
                </tr>
                <tr>
                    <td style="padding: 8px;"><strong>Endereço:</strong></td>
                    <td>R. São João, 1042 – Santa Terezinha, Fazenda Rio Grande – PR, 83829-248</td>
                </tr>
            </table>
        </div>
    """, unsafe_allow_html=True)

# Botão do Google Maps
endereco = "R. São João, 1042 – Santa Terezinha, Fazenda Rio Grande – PR, 83829-248 - Ginásio de Esportes Gurizão"
google_maps_url = f"https://www.google.com/maps/search/?api=1&query={endereco.replace(' ', '+')}"
st.markdown(f"""
    <div style='text-align: center; margin: 20px 0;'>
        <a href="{google_maps_url}" target="_blank" style="text-decoration: none;">
            <button class="maps-button">
                📍 Abrir no Google Maps
            </button>
        </a>
    </div>
""", unsafe_allow_html=True)

# Seleção de modalidade com ícones
st.markdown("<h2>Modalidade</h2>", unsafe_allow_html=True)
estilo = st.radio(
    "",
    ["Kata", "Luta"],
    format_func=lambda x: f"🥋 {x}" if x == "Kata" else f"🥊 {x}",
    horizontal=True,
)

# Carregar dados
df = get_data()
if df.empty:
    st.error("🚫 Não foi possível carregar os dados. Por favor, verifique a conexão com o banco de dados.")
    st.stop()

data = load_data(estilo=estilo)
atletas_ambos_estilos = df.groupby('atleta').agg({'estilo':'nunique'}).query("estilo > 1").shape[0]

# Filtros em um container próprio
with st.container():
    st.markdown("<h2>Filtros</h2>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        academia = st.multiselect(
            "🏢 Academia",
            options=sorted(data['academia'].dropna().unique()),
            placeholder='Selecionar Academia'
        )
    
    with col2:
        atleta = st.multiselect(
            "🥋 Atleta",
            options=sorted(data['atleta'].dropna().unique()),
            placeholder='Selecionar Atleta'
        )

# Aplicar filtros
filtered_data = data
if academia:
    filtered_data = filtered_data[filtered_data['academia'].isin(academia)]
if atleta:
    grupos_atleta = data[data['atleta'].isin(atleta)]['categoria'].unique()
    filtered_data = filtered_data[filtered_data['categoria'].isin(grupos_atleta)]

# Tabela de dados
st.markdown(f"<h2>Tabela de {estilo}s</h2>", unsafe_allow_html=True)
st.markdown(f"<div class='metric-card'>Atletas Selecionados: {len(filtered_data)}</div>", unsafe_allow_html=True)
st.dataframe(
    filtered_data[['categoria', 'atleta', 'local', 'academia', 'faixa']],
    hide_index=True,
    use_container_width=True
)

# Estatísticas em cards
st.markdown("<h2>Estatísticas do Campeonato</h2>", unsafe_allow_html=True)

# Primeira linha de estatísticas
col1, col2 = st.columns(2)
with col1:
    st.markdown("""
        <div class="stcard">
            <h3 style="margin-top: 0;">📊 Total de Participantes</h3>
    """, unsafe_allow_html=True)
    st.write(f"- {df[df.estilo == estilo.title()].categoria.nunique()} Chaves")
    st.write(f"- {df[df.estilo == estilo.title()].atleta.nunique()} atletas no {estilo}")
    st.write(f"- {atletas_ambos_estilos} participam de ambas modalidades")
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="stcard">
            <h3 style="margin-top: 0;">👥 Distribuição por Gênero</h3>
    """, unsafe_allow_html=True)
    st.write(f"- {df[(df.estilo == estilo.title()) & (df.sexo == 'Masculino')].atleta.nunique()} Masculino")
    st.write(f"- {df[(df.estilo == estilo.title()) & (df.sexo == 'Feminino')].atleta.nunique()} Feminino")
    st.write(f"- {df[(df.estilo == estilo.title()) & (df.sexo != 'Feminino') & (df.sexo != 'Masculino')].atleta.nunique()} Misto")
    st.markdown("</div>", unsafe_allow_html=True)

# Segunda linha de estatísticas
col1, col2 = st.columns(2)
with col1:
    st.markdown("""
        <div class="stcard">
            <h3 style="margin-top: 0;">🏢 Atletas por Academia</h3>
    """, unsafe_allow_html=True)
    st.dataframe(
        filtered_data.groupby('academia').agg({
            'atleta': 'nunique',
            'categoria': 'nunique'
        }).rename(columns={
            'atleta': 'Atletas',
            'categoria': 'Ouros Possíveis'
        }).sort_values('Atletas', ascending=False),
        use_container_width=True
    )
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="stcard">
            <h3 style="margin-top: 0;">🤼 Confrontos entre Academias</h3>
    """, unsafe_allow_html=True)
    confrontos = []
    for _, grupo in filtered_data.groupby('categoria'):
        academias = grupo['academia'].unique()
        for a1, a2 in combinations(sorted(academias), 2):
            confrontos.append((a1, a2))
    confrontos_df = pd.DataFrame(confrontos, columns=['Academia 1', 'Academia 2'])
    confrontos_df_final = confrontos_df.value_counts().reset_index(name='Confrontos')
    st.dataframe(confrontos_df_final, hide_index=True, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Terceira linha de estatísticas
col1, col2 = st.columns(2)
with col1:
    st.markdown("""
        <div class="stcard">
            <h3 style="margin-top: 0;">📊 Distribuição por Faixa Etária</h3>
    """, unsafe_allow_html=True)
    st.dataframe(
        pd.DataFrame(
            filtered_data['idade'].value_counts()
        ).rename(
            columns={
                'count':'Quantidade de Atletas'
            }
        ),
        use_container_width=True
    )
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="stcard">
            <h3 style="margin-top: 0;">🥋 Distribuição por Graduação</h3>
    """, unsafe_allow_html=True)
    st.dataframe(
        pd.DataFrame(
            filtered_data['faixa'].value_counts()
        ).rename(
            columns={
                'count':'Quantidade de Atletas'
            }
        ),
        use_container_width=True
    )
    st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("""
    <div style='text-align: center; margin-top: 50px; padding: 20px; color: #666;'>
        <p>Desenvolvido para a comunidade do Karatê 🥋</p>
    </div>
""", unsafe_allow_html=True)