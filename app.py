import streamlit as st
import pandas as pd

# Configurações iniciais da página
st.set_page_config(page_title="Campeonato de Karatê", layout="wide")

image_url = "https://karateshubudo.com.br/wp-content/uploads/2021/12/2-Academia-Master-Karate-Shubu-do.jpg"
st.image(image_url, width=200)

# Título
st.markdown("<h1 style='text-align: center;'>Campeonato de Karatê Shubu-dô</h1>", unsafe_allow_html=True)

# Descrição
st.write("""
#### Informações:
    Campeonato de Luta e Katá  
    Dia: 20/10/2024  
    Horário: a partir das 09:00h  
    Local: Ginásio de Esportes Gurizão  
    Endereço: R. São João, 1042 – Santa Terezinha, Fazenda Rio Grande – PR, 83829-248
""")

# Carregar os dados
@st.cache_data
def load_data(file_path):
    return pd.read_csv(file_path)

file_path = "kata.csv"
data = load_data(file_path)

# Listas únicas para filtros, ordenadas
atletas_unicos = sorted(data['atleta'].dropna().unique())
academias_unicas = sorted(data['academia'].dropna().unique())

# Filtros principais, exibidos antes da tabela
st.write("")
academia = st.multiselect("Academia", options=academias_unicas, placeholder='Selecionar Academia')
atleta = st.multiselect("Atleta", options=atletas_unicos, placeholder='Selecionar Atleta')

# Aplicar filtros nos dados
filtered_data = data

if academia:
    filtered_data = filtered_data[filtered_data['academia'].isin(academia)]

if atleta:
    grupos_atleta = data[data['atleta'].isin(atleta)]['categoria'].unique()
    filtered_data = filtered_data[filtered_data['categoria'].isin(grupos_atleta)]

# Exibir tabela de dados filtrados
st.markdown("<h2 style='text-align: center; font-size: 28px;'>Tabela Completa de Katas</h2>", unsafe_allow_html=True)
st.write("**Apresentações:**", len(filtered_data))
st.dataframe(filtered_data[['categoria', 'atleta', 'mesa', 'academia']], hide_index=True)

# Estatísticas adicionais
st.markdown("<h2 style='text-align: center; font-size: 28px;'>Estatísticas do Campeonato</h2>", unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:
    st.write("**Quantidade de atletas por academia:**")
    st.write(
        filtered_data.groupby('academia').agg({
            'atleta': 'nunique',
            'categoria': 'nunique'
        }).rename(columns={
            'atleta': 'Quantidade de Atletas',
            'categoria': 'Ouros Possíveis'
        }).sort_values('Quantidade de Atletas', ascending=False)
    )

with col2:
    st.write("**Contagem de Confrontos entre Academias**")
    confrontos_data = (
        filtered_data.groupby(['categoria', 'academia'])
        .size()
        .reset_index(name='contagem_lutas')
    )
    confrontos_entre_academias = (
        confrontos_data.merge(confrontos_data, on='categoria', suffixes=('_1', '_2'))
        .query("academia_1 != academia_2")
    )
    confrontos_entre_academias['total_confrontos'] = (
        confrontos_entre_academias.groupby(['academia_1', 'academia_2'])['contagem_lutas_1']
        .transform('sum')
    )
    confrontos_entre_academias = confrontos_entre_academias[['academia_1', 'academia_2', 'total_confrontos']].drop_duplicates().sort_values('total_confrontos', ascending=False)
    st.dataframe(confrontos_entre_academias, hide_index=True)

col1, col2 = st.columns(2)
with col1:
    st.write("**Distribuição de atletas por faixa etária:**")
    st.write(data['idade'].value_counts())
with col2:
    st.write("**Distribuição por Graduação:**")
    st.write(data['faixa'].value_counts())
