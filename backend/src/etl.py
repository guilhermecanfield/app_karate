from faker import Faker
import os
import pandas as pd
from unidecode import unidecode

# Inicializando o Faker
fake = Faker('pt_BR')

# Dicionários para armazenar os mapeamentos
name_mapping = {}
academy_mapping = {}

# Função para gerar ou recuperar o nome fictício
def get_fake_name(real_name):
    real_name = real_name.strip().lower()  # Normaliza o valor antes do mapeamento
    if real_name not in name_mapping:
        if real_name:  # Se não for vazio, gera o nome fictício
            name_mapping[real_name] = fake.name()
        else:  # Se for vazio, usa um padrão
            name_mapping[real_name] = "Nome Desconhecido"
    return name_mapping[real_name]

# Função para gerar ou recuperar a academia fictícia
def get_fake_academy(real_academy):
    real_academy = real_academy.strip().lower()  # Normaliza o valor antes do mapeamento
    if real_academy not in academy_mapping:
        if real_academy:
            academy_mapping[real_academy] = f"Academia {fake.last_name()}"
        else:
            academy_mapping[real_academy] = "Academia Desconhecida"
    return academy_mapping[real_academy]

def gera_dados():
    # Lista de arquivos a serem anonimizados
    lista = [
        'CATEGORIAS KATÁ COM LOCAL DE APRESENTAÇÃO FEMININO.xlsx',
        'CATEGORIAS KATÁ COM LOCAL DE APRESENTAÇÃO MASCULINO.xlsx',
        'CATEGORIAS KATÁ EM EQUIPE COM LOCAL DE APRESENTAÇÃO MISTO.xlsx'
    ]

    dfs = []

    # Processando cada arquivo
    for file in lista:
        df = pd.read_excel(f'kata/{file}')

        # Normalizando os nomes das colunas
        new_cols = []
        for col in df.columns:
            new_cols.append(
                unidecode(
                    col.strip()
                    .replace('.', '')
                    .replace(' - ', '_')
                    .replace(' ', '_')
                    .replace('__', '_')
                    .replace('%', '')
                    .lower()
                )
            )
        df.columns = new_cols

        df['estilo'] = 'Kata'
        df['sexo'] = file.split(' ')[-1].split('.')[0].title()
        df['local_de_apresentacao'] = df['local_de_apresentacao'].str.replace('\n', ' ', regex=False).str.title()
        df['atleta_1'] = df['nome_da_categoria'].str.split('\n').str.get(1).str.split('(').str.get(0).str.strip()
        df['academia_1'] = df['nome_da_categoria'].str.split('\n').str.get(1).str.split('(').str.get(1).str.strip().str.replace(')', '', regex=False)
        df['atleta_2'] = df['nome_da_categoria'].str.split('\n').str.get(2).str.split('(').str.get(0).str.strip()
        df['academia_2'] = df['nome_da_categoria'].str.split('\n').str.get(2).str.split('(').str.get(1).str.strip().str.replace(')', '', regex=False)
        df['atleta_3'] = df['nome_da_categoria'].str.split('\n').str.get(3).str.split('(').str.get(0).str.strip()
        df['academia_3'] = df['nome_da_categoria'].str.split('\n').str.get(3).str.split('(').str.get(1).str.strip().str.replace(')', '', regex=False)
        if not 'MISTO' in file:
            df['idade'] = df['nome_da_categoria'].str.split('\n').str.get(0).str.split('–').str.get(1).str.strip().str.title()
            df['faixa'] = df['nome_da_categoria'].str.split('\n').str.get(0).str.split('–').str.get(2).str.strip().str.title()
            df['faixa'] = df['faixa'].str.split(' ').apply(lambda x: ' '.join(x[:2]))
        else:
            df['faixa'] = df['nome_da_categoria'].str.split('\n').str.get(0).str.split('–').str.get(1).str.strip().str.title()
            df['faixa'] = df['faixa'].str.split(' ').apply(lambda x: ' '.join(x[:2]))
            df['idade'] = 'Mista'

        # Preenchendo valores vazios e normalizando
        for col in ['atleta_1', 'atleta_2', 'atleta_3', 'academia_1', 'academia_2', 'academia_3']:
            df[col] = df[col].fillna('').str.strip().str.lower()

        # Anonimizando os dados usando os mapeamentos
        for col in ['atleta_1', 'atleta_2', 'atleta_3']:
            df[col] = df[col].apply(get_fake_name)

        for col in ['academia_1', 'academia_2', 'academia_3']:
            df[col] = df[col].apply(get_fake_academy)

        df.drop(columns='nome_da_categoria', inplace=True)
    
        df.rename(columns={
            'local_de_apresentacao':'local',
            'no_da_categoria':'categoria'
        }, inplace=True)

        df = df[[
            'categoria', 'faixa', 'idade', 'sexo', 'atleta_1', 'academia_1', 
            'atleta_2', 'academia_2', 'atleta_3', 'academia_3', 'estilo', 'local'
            ]].copy()

        dfs.append(df)

    kata = pd.concat(dfs)

    # Lista para armazenar as linhas "derretidas" com uma coluna para atletas e uma para academias
    long_format_data = []

    # Iterar sobre cada linha e "desempilhar" as colunas de atleta e academia
    for _, row in kata.iterrows():
        for i in range(1, 4):  # Supondo que há 3 atletas e 3 academias por linha
            long_format_data.append({
                'categoria': row['categoria'],
                'faixa': row['faixa'],
                'idade': row['idade'],
                'sexo': row['sexo'],
                'estilo': row['estilo'],
                'local': row['local'],
                'atleta': row[f'atleta_{i}'],
                'academia': row[f'academia_{i}']
            })

    # Criando um DataFrame a partir dos dados organizados
    kata = pd.DataFrame(long_format_data)

    kata = kata[[
        'categoria', 'faixa', 'idade', 'atleta',
        'sexo', 'estilo', 'academia', 'local'
        ]].copy()

    # Lista de arquivos
    lista = os.listdir('luta')

    dfs = []

    # Processando cada arquivo
    for file in lista:
        # Lendo o arquivo Excel e renomeando colunas
        df = pd.read_excel(f'luta/{file}').rename(columns={
            'Nº DA CATEGORIA': 'categoria',
            'LOCAL DA LUTA': 'local'
        })


        # Extraindo informações dos atletas e academias
        df['nome_categoria'] = df['NOME DA CATEGORIA'].str.split('\n').str.get(0).str.split('–').str.get(1).str.strip()
        df['idade'] = df['NOME DA CATEGORIA'].str.split('\n').str.get(0).str.split('–').str.get(2).str.strip().str.title()
        df['atleta_1'] = df['NOME DA CATEGORIA'].str.split('\n').str.get(1).str.split('(').str.get(0).str.strip()
        df['academia_1'] = df['NOME DA CATEGORIA'].str.split('\n').str.get(1).str.split('(').str.get(1).str.strip().str.replace(')', '', regex=False)
        df['atleta_2'] = df['NOME DA CATEGORIA'].str.split('\n').str.get(2).str.split('(').str.get(0).str.strip()
        df['academia_2'] = df['NOME DA CATEGORIA'].str.split('\n').str.get(2).str.split('(').str.get(1).str.strip().str.replace(')', '', regex=False)
        df['atleta_3'] = df['NOME DA CATEGORIA'].str.split('\n').str.get(3).str.split('(').str.get(0).str.strip()
        df['academia_3'] = df['NOME DA CATEGORIA'].str.split('\n').str.get(3).str.split('(').str.get(1).str.strip().str.replace(')', '', regex=False)

        # Removendo a coluna original de categorias
        df.drop(columns=['NOME DA CATEGORIA'], inplace=True)

        # Adicionando informações de sexo e estilo
        df['sexo'] = file.split(' ')[3].title()
        df['estilo'] = 'Luta'
        # Padronizando Dados
        df.loc[:, 'local'] = df['local'].str.title()

        # Normalizando os dados e aplicando a anonimização
        for col in ['atleta_1', 'atleta_2', 'atleta_3', 'academia_1', 'academia_2', 'academia_3']:
            df[col] = df[col].fillna('').str.strip().str.lower()

        for col in ['atleta_1', 'atleta_2', 'atleta_3']:
            df[col] = df[col].apply(get_fake_name)

        for col in ['academia_1', 'academia_2', 'academia_3']:
            df[col] = df[col].apply(get_fake_academy)

        dfs.append(df)

    # Concatenando todos os DataFrames em um único DataFrame final
    luta = pd.concat(dfs, ignore_index=True)

    # Removendo a coluna desnecessária
    luta.drop(columns=['nome_categoria'], inplace=True)

    # Lista para armazenar as linhas "derretidas" com uma coluna para atletas e uma para academias
    long_format_data = []

    # Iterar sobre cada linha e "desempilhar" as colunas de atleta e academia
    for _, row in luta.iterrows():
        for i in range(1, 4):  # Levando em consideração que pode haver 3 atletas e 3 academias por linha
            long_format_data.append({
                'categoria': row['categoria'],
                'local': row['local'],
                'idade': row['idade'],
                'sexo': row['sexo'],
                'atleta': row[f'atleta_{i}'],
                'academia': row[f'academia_{i}'],
                'estilo': row['estilo']
            })

    # Criando um DataFrame a partir dos dados organizados
    df_long = pd.DataFrame(long_format_data)

    luta = df_long.dropna().reset_index(drop=True)
    luta['faixa'] = luta.atleta.map(kata[['atleta','faixa']].dropna().set_index('atleta').to_dict()['faixa'])
    luta.loc[:, 'faixa'] = luta['faixa'].fillna('Não Informada')

    df_final = pd.concat([kata, luta])

    df_final = df_final.query('atleta != "Nome Desconhecido"')

    return df_final