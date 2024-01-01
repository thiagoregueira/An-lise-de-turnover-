import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(
    page_title="Tratamento de Dados",
    page_icon="📊",
    layout="wide",
)


@st.cache_data
def load_data():
    df = pd.read_excel("Base_RH.xlsx", sheet_name="Base")
    return df


def app():
    df = load_data()
    st.markdown(
        """
                <h1 style='text-align: left;'> Tratamento de Dados </h1>
                <br><br>""",
        unsafe_allow_html=True,
    )
    st.markdown(
        """
            <h2 style='text-align: center;'>Mostrando as primeiras linhas:</h2>
            <br>""",
        unsafe_allow_html=True,
    )
    st.dataframe(df.head())
    st.markdown(
        """
        <h2 style='text-align: center;'>Dicionário de dados:</h2>
        <br>

        | Variável | Descrição |
        | --- | --- |
        | ID | Matrícula do funcionário |
        | Funcionário_deixou_a_empresa | Marcação sem funcionário deixou a empresa recentemente |
        | Idade | Idade do funcionário |
        | Frequência de Viagens | Frequência de viagens a trabalho do funcionário |
        | Distância_do_trabalho | Distância em Km até o trabalho |
        | Formação | Nível de formação |
        | E-Sat | Satisfação com o clima organizacional |
        | Gênero | Gênero do funcionário |
        | Estado_Civil | Estado civil do funcionário |
        | Salário | Salário mensal |
        | Qte_Empresas_Trabalhadas | Quantidade de empresas que o funcionário já trabalhou |
        | Faz_hora_extras? | Se funcionário costuma fazer hora extra |
        | Perc_de_aumento | Percentual de aumento de salário de 2018 a 2019 |
        | Qte_ações_da_empresa | Qte de lotes de ações da empresa que o funcionário possui |
        | Tempo_de_carreira | Tempo em anos que o funcionário tem de carreira |
        | Horas_de_treinamento | Qte de horas de treinamento que o funcionário teve no ano passado |
        | Equilibrio_de_Vida | Nota que o funcionário deu para seu equilibrio entre vida pessoal e profissional |
        | Tempo_de_empresa | Tempo em anos que o funcionário trabalha na empresa |
        | Anos_no_mesmo_cargo | Qte de tempo em anos que o funcionário atua no mesmo cargo |
        | Anos_desde_a_ultima_promocao | Qte de tempo em anos que o funcionário teve a última promoção |
        | Anos_com_o_mesmo_chefe | Qte de tempo em anos que o funcionário responde para o mesmo chefe |
""",
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        """
            <h2 style='text-align: center;'>Verificando se existem valores ausentes:</h2>
            <br>""",
        unsafe_allow_html=True,
    )

    # Criando colunas
    col1, col2 = st.columns(2)

    # Definindo a largura das colunas e colocando o conteúdo da col2 no centro da coluna
    col1_width = 600

    with col1:
        st.dataframe(df.isnull().sum(), width=col1_width)

    with col2:
        st.markdown(
            """
            <br><br><br>
            <p style='text-align: justify;'>- Todas as colunas possuem valores preenchidos para todas as linhas. Não há nenhuma célula vazia ou com valor faltante em nenhuma das variáveis do dataframe. Isso significa que todas as informações necessárias estão presentes e completas para cada funcionário representado no conjunto de dados.</p>""",
            unsafe_allow_html=True,
        )

    # verificando se existem valores duplicados
    st.markdown(
        """
            <br>
            <h2 style='text-align: center;'>Verificando se existem valores duplicados:</h2>
            <br><br>""",
        unsafe_allow_html=True,
    )

    col7, col8 = st.columns(2)

    with col7:
        # Criar DataFrame com a soma dos valores duplicados
        duplicated_df = pd.DataFrame({"Valores Duplicados": [df.duplicated().sum()]})
        st.dataframe(duplicated_df, width=col1_width)

    with col8:
        st.markdown(
            """
            <p style='text-align: justify;'>- Nenhuma linha do dataframe possui valores duplicados.</p>""",
            unsafe_allow_html=True,
        )

    st.markdown(
        """<h2 style='text-align: center;'>Verificando os tipos de dados:</h2> <br><br>""",
        unsafe_allow_html=True,
    )

    col3, col4 = st.columns(2)

    col3_width = 600

    with col3:
        st.dataframe(df.dtypes, width=col3_width)
    with col4:
        st.markdown(
            """
            <p style='text-align: justify;'>- As variáveis quantitativas são aquelas que podem ser medidas em uma escala numérica, como idade, salário, distância do trabalho, etc. As variáveis qualitativas são aquelas que representam características ou categorias, como gênero, estado civil, formação, etc.</p>
            <br>
            <br>
            <h5>- Variáveis Quantitativas:</h5> 
            <p style='text-align: justify;'>Idade, Distância_do_trabalho, Salário, Qte_Empresas_Trabalhadas, Perc_de_aumento, Qte_ações_da_empresa, Tempo_de_carreira, Horas_de_treinamento, Tempo_de_empresa, Anos_no_mesmo_cargo, Anos_desde_a_ultima_promocao, Anos_com_o_mesmo_chefe.</p>
            <br>
            <br>
            <h5>- Variáveis Qualitativas:</h5> Funcionário_deixou_a_empresa, Frequência de Viagens, Formação, E-Sat, Gênero, Estado_Civil, Faz_hora_extras?, Equilibrio_de_Vida.
""",
            unsafe_allow_html=True,
        )

    st.markdown(
        """<br><br><h2 style='text-align: center;'>Verificando se existem outliers:</h2> <br>""",
        unsafe_allow_html=True,
    )

    col5, col6 = st.columns(2)

    df = df.drop("ID", axis=1)
    # Plotando o boxplot para cada coluna numérica
    with col5:
        for col in df.columns:
            if pd.api.types.is_numeric_dtype(df[col]):
                fig = px.box(df, y=col)
                st.plotly_chart(fig)

    with col6:
        st.markdown(
            """
            <br>
            <br>
            <br>
            <p style='text-align: justify;'>- Os outliers podem ter várias causas, como erros de medição, variações naturais, ou características especiais da população. Dependendo do contexto e do objetivo da análise, os outliers podem ser ignorados, removidos, ou mantidos nos dados. No nosso caso iremos mantê-los devido aos seguintes pontos:</p>
            <br>
            <br>
            <p style='text-align: justify;'>- Os outliers são consistentes com as regras de negócio</p>
            <br>
            <br>
            <p style='text-align: justify;'>- Os outliers são poucos e não afetam significativamente as medidas de tendência central e de dispersão dos dados.</p>
            <br>
            <br>
            <p style='text-align: justify;'>- Os outliers são importantes para a análise, pois revelam informações relevantes ou interessantes sobre os dados.</p>
            <br>
            <br>
""",
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <h3 style='text-align: center;'>Conclusão:</h3>
            <p style='text-align: justify;'>- Realizamos uma análise exploratória dos dados fornecidos, verificando sua qualidade, consistência e distribuição. Não encontramos dados faltantes, duplicados ou inválidos, o que indica que a base de dados já foi previamente tratada e padronizada.</p>
            <br>
            <p style='text-align: justify;'>- Identificamos alguns valores extremos nos dados, mas optamos por não removê-los, pois eles representam casos reais e relevantes para as regras de negócio. Além disso, a remoção dos outliers poderia afetar a confiabilidade e a representatividade dos dados, comprometendo as análises posteriores.</p>
            <br>
            <p style='text-align: justify;'>- Concluímos que os dados fornecidos estão em boas condições para serem utilizados em etapas posteriores do projeto, como a análise exploratória, visualização e interpretação.</p>
""",
            unsafe_allow_html=True,
        )
