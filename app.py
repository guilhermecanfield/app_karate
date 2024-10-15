import streamlit as st
import pandas as pd

# Configurações iniciais da página
st.set_page_config(page_title="Campeonato de Karatê", layout="wide")

col1, col2 = st.columns(2)

with col1:
    # Adicionar a imagem
    image_url = "https://karateshubudo.com.br/wp-content/uploads/2021/12/2-Academia-Master-Karate-Shubu-do.jpg"
    st.image(image_url, width=250)
with col2:
    # Adicionar a imagem
    image_url = "https://karateshubudo.com.br/wp-content/uploads/2024/02/LOGO_KARATE-JPG-2010-1536x1536.jpg"
    st.image(image_url, width=250)

# Título
# st.title("Campeonato de Karatê Shubu-dô")

st.markdown(
    "<h1 style='text-align: center;'>Campeonato de Karatê Shubu-dô</h1>", 
    unsafe_allow_html=True
)


st.write("""
        
        #### - Informações:
            
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

# Função para exibir os dados
def display_data(data):
    st.dataframe(data)

# Carregar o arquivo CSV de dados
file_path = "kata.csv"
data = load_data(file_path)

# Unindo as colunas de atletas e academias para obter listas únicas, removendo NaNs
atletas_unicos = sorted(data['atleta'].dropna().unique())
academias_unicas = sorted(data['academia'].dropna().unique())

# Filtros
st.sidebar.header("Filtros")
academia = st.sidebar.multiselect("Academia", options=academias_unicas, placeholder='Selecionar Academia')
atleta = st.sidebar.multiselect("Atleta", options=atletas_unicos, placeholder='Selecionar Atleta')

# Aplicar filtros nos dados
filtered_data = data

# Filtra por academia, se selecionado
if academia:
    filtered_data = filtered_data[filtered_data['academia'].isin(academia)]

# Identifica grupos das lutas em que os atletas selecionados irão participar
if atleta:
    grupos_atleta = data[data['atleta'].isin(atleta)]['no_da_categoria'].unique()
    filtered_data = filtered_data[filtered_data['no_da_categoria'].isin(grupos_atleta)]

# Exibir dados filtrados
st.markdown("<h2 style='text-align: center; font-size: 28px;'>Tabela Completa de Katas</h2>", unsafe_allow_html=True)
st.write("**Apresentações:**", len(filtered_data))
display_data(filtered_data)

# Estatísticas adicionais
st.markdown("<h2 style='text-align: center; font-size: 28px;'>Estatísticas do Campeonato</h2>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.write("**Quantidade de atletas por academia:**")
    st.write(
        filtered_data.groupby('academia').agg({
            'atleta':'nunique',
            'no_da_categoria':'nunique'
        }).rename(columns={
            'atleta': 'Quantidade de Atletas',
            'no_da_categoria': 'Ouros Possíveis'
        }).sort_values('Quantidade de Atletas', ascending=False)
    )

with col2:
    # Contagem de lutas entre academias na mesma categoria
    st.write("**Contagem de Confrontos entre Academias**")

    # Agrupar e contar lutas entre academias que estão na mesma categoria
    confrontos_data = (
        filtered_data.groupby(['no_da_categoria', 'academia'])
        .size()
        .reset_index(name='contagem_lutas')
    )

    # Criar um DataFrame de confrontos
    confrontos_entre_academias = (
        confrontos_data.merge(confrontos_data, on='no_da_categoria', suffixes=('_1', '_2'))
        .query("academia_1 != academia_2")
    )

    # Contar lutas entre cada par de academias
    confrontos_entre_academias['total_confrontos'] = (
        confrontos_entre_academias.groupby(['academia_1', 'academia_2'])['contagem_lutas_1']
        .transform('sum')
    )

    confrontos_entre_academias = confrontos_entre_academias[['academia_1', 'academia_2', 'total_confrontos']].drop_duplicates().sort_values('total_confrontos', ascending=False)

    display_data(confrontos_entre_academias)

col1, col2 = st.columns(2)

with col1:
    st.write("**Distribuição de atletas por faixa etária:**")
    st.write(filtered_data['idade'].value_counts())

with col2:
    st.write("**Distribuição por Graduação:**")
    st.write(filtered_data['faixa'].value_counts())
