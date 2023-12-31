import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np


@st.cache_data
def load_data():
    df = pd.read_excel("Base_RH.xlsx", sheet_name="Base")
    return df


def app():
    st.markdown(
        """
        <h1 style='text-align: left;'>Calculando os IV's</h1>
        <br>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <p style='text-align: justify;'>O Information Value é uma medida usada para avaliar o grau de associação/separação entre duas variáveis.<br> A análise de associação/separação é uma ferramenta fundamental para avaliar o grau de relacionamento entre duas ou mais variáveis. Ela permite descobrir com precisão o quanto uma variável interfere no resultado de outra.<br><br> Portanto, o Information Value pode ser útil para entender melhor a dependência existente entre as variáveis, de modo que se possa prever melhor o resultado de uma delas quando se conhece o resultado da outra.<br><br>
        Então utilizaremos dos IV's para definir quais as variáveis mais importantes e que "explicam" o comportamento de nossa variável de resposta("Funcionário_deixou_a_empresa").</p>
        """,
        unsafe_allow_html=True,
    )

    df = load_data()

    col1, col2 = st.columns(2)

    with col1:
        # Usando o plotly
        # variáveis categóricas
        columns_cat = df.drop(
            columns=[
                "Funcionário_deixou_a_empresa",
                "ID",
                "Idade",
                "Distância_do_trabalho",
                "Salário",
                "Qte_Empresas_Trabalhadas",
                "Perc_de_aumento",
                "Qte_ações_da_empresa",
                "Tempo_de_carreira",
                "Horas_de_treinamento",
                "Tempo_de_empresa",
                "Anos_no_mesmo_cargo",
                "Anos_desde_a_ultima_promocao",
                "Anos_com_o_mesmo_chefe",
            ]
        ).columns

        # Lista para armazenar o IV
        iv = []

        # Loop para calcular o IV de cada variável
        for i in columns_cat:
            df_woe_iv = (
                pd.crosstab(
                    df[i], df["Funcionário_deixou_a_empresa"], normalize="columns"
                )
                .assign(woe=lambda dfx: np.log(dfx["Sim"] / dfx["Não"]))
                .assign(iv=lambda dfx: np.sum(dfx["woe"] * (dfx["Sim"] - dfx["Não"])))
            )
            iv.append(df_woe_iv["iv"].iloc[0])

        # Criando um dataframe com as variáveis e seus respectivos IVs
        df_iv_qualitativas = (
            pd.DataFrame({"Features": columns_cat, "iv": iv})
            .set_index("Features")
            .sort_values(by="iv")
        )

        # Plot
        fig_qualitativas = px.bar(
            df_iv_qualitativas,
            y=df_iv_qualitativas.index,
            x="iv",
            orientation="h",
            title="IV das variáveis Qualitativas categóricas",
        )

        # adicionando os valores das barras
        fig_qualitativas.update_layout(
            title_x=0.1,
            title_font=dict(family="Monospace", size=26, color="white"),
            annotations=[
                dict(
                    x=df_iv_qualitativas.iloc[i]["iv"],
                    y=df_iv_qualitativas.index[i],
                    text=str(round(df_iv_qualitativas.iloc[i]["iv"], 3)),
                    xanchor="left",
                    yanchor="middle",
                    showarrow=False,
                )
                for i in range(len(df_iv_qualitativas))
            ],
        )

        st.plotly_chart(fig_qualitativas)

    with col2:
        # Criando as faixas de valores para as variáveis quantitativas e calcular o IV
        # Idade

        df["Idade_5"] = pd.cut(
            df["Idade"],
            bins=5,
            labels=[
                "18-25",
                "26-35",
                "36-45",
                "46-55",
                "56-65",
            ],
        )

        # Distância do trabalho

        df["Distância_do_trabalho_5"] = pd.cut(
            df["Distância_do_trabalho"],
            bins=5,
            labels=[
                "0-5",
                "6-10",
                "11-15",
                "16-20",
                "21-30",
            ],
        )

        # Salário

        df["Salário_5"] = pd.cut(
            df["Salário"],
            bins=6,
            labels=[
                "0-2500",
                "2501-5000",
                "5001-7500",
                "7501-10000",
                "10001-15000",
                "15001-20000",
            ],
        )

        # Qte_Empresas_Trabalhadas

        df["Qte_Empresas_Trabalhadas_5"] = pd.cut(
            df["Qte_Empresas_Trabalhadas"],
            bins=5,
            labels=[
                "0-1",
                "2-3",
                "4-5",
                "6-7",
                "8-10",
            ],
        )

        # Perc_de_aumento

        df["Perc_de_aumento_5"] = pd.cut(
            df["Perc_de_aumento"], bins=3, labels=["10-15", "16-20", "21-25"]
        )

        # Qte_ações_da_empresa

        df["Qte_ações_da_empresa_5"] = pd.cut(
            df["Qte_ações_da_empresa"],
            bins=2,
            labels=[
                "0-1",
                "2-3",
            ],
        )

        # Tempo_de_carreira

        df["Tempo_de_carreira_5"] = pd.cut(
            df["Tempo_de_carreira"],
            bins=8,
            labels=[
                "0-5",
                "6-10",
                "11-15",
                "16-20",
                "21-25",
                "26-30",
                "31-35",
                "36-40",
            ],
        )

        # Horas_de_treinamento

        df["Horas_de_treinamento_5"] = pd.cut(
            df["Horas_de_treinamento"],
            bins=3,
            labels=[
                "0-2",
                "3-4",
                "5-6",
            ],
        )

        # Tempo_de_empresa

        df["Tempo_de_empresa_5"] = pd.cut(
            df["Tempo_de_empresa"],
            bins=5,
            labels=[
                "0-2",
                "3-5",
                "6-8",
                "9-10",
                "11-40",
            ],
        )

        # Anos_no_mesmo_cargo

        df["Anos_no_mesmo_cargo_5"] = pd.cut(
            df["Anos_no_mesmo_cargo"],
            bins=5,
            labels=[
                "0-2",
                "3-5",
                "6-8",
                "9-10",
                "11-20",
            ],
        )

        # Anos_desde_a_ultima_promocao

        df["Anos_desde_a_ultima_promocao_5"] = pd.cut(
            df["Anos_desde_a_ultima_promocao"],
            bins=5,
            labels=[
                "0-2",
                "3-5",
                "6-8",
                "9-10",
                "11-15",
            ],
        )

        # Anos_com_o_mesmo_chefe

        df["Anos_com_o_mesmo_chefe_5"] = pd.cut(
            df["Anos_com_o_mesmo_chefe"],
            bins=5,
            labels=[
                "0-2",
                "3-5",
                "6-8",
                "9-10",
                "11-20",
            ],
        )

        # Usando o plotly

        columns_faixas = [
            "Idade_5",
            "Distância_do_trabalho_5",
            "Salário_5",
            "Qte_Empresas_Trabalhadas_5",
            "Perc_de_aumento_5",
            "Qte_ações_da_empresa_5",
            "Tempo_de_carreira_5",
            "Horas_de_treinamento_5",
            "Tempo_de_empresa_5",
            "Anos_no_mesmo_cargo_5",
            "Anos_desde_a_ultima_promocao_5",
            "Anos_com_o_mesmo_chefe_5",
        ]

        # Lista para armazenar o IV
        iv_quantitativas = []

        # Loop para calcular o IV de cada variável
        for i in columns_faixas:
            df_woe_iv = (
                pd.crosstab(
                    df[i], df["Funcionário_deixou_a_empresa"], normalize="columns"
                )
                .assign(woe=lambda dfx: np.log(dfx["Sim"] / dfx["Não"]))
                .assign(iv=lambda dfx: np.sum(dfx["woe"] * (dfx["Sim"] - dfx["Não"])))
            )
            iv_quantitativas.append(df_woe_iv["iv"].iloc[0])  # Armazena o valor de IV

        # Criando um dataframe com as variáveis e seus respectivos IVs
        df_iv_quantitativas = (
            pd.DataFrame({"Features": columns_faixas, "iv": iv_quantitativas})
            .set_index("Features")
            .sort_values(by="iv")
        )

        # Plot
        fig_quantitativas = px.bar(
            df_iv_quantitativas,
            y=df_iv_quantitativas.index,
            x="iv",
            orientation="h",
            title="IV das variáveis quantitativas",
        )

        # adicionando os valores das barras
        fig_quantitativas.update_layout(
            title_x=0.2,
            title_font=dict(family="Monospace", size=26, color="white"),
            annotations=[
                dict(
                    x=df_iv_quantitativas.iloc[i]["iv"],
                    y=df_iv_quantitativas.index[i],
                    text=str(round(df_iv_quantitativas.iloc[i]["iv"], 3)),
                    xanchor="left",
                    yanchor="middle",
                    showarrow=False,
                )
                for i in range(len(df_iv_quantitativas))
            ],
        )

        st.plotly_chart(fig_quantitativas)

    st.markdown(
        "<h4 style='text-align: center;'>Comparando os IV's que obtivemos de cada variável com o benchmark, temos a seguinte situação:</h4><br><br>",
        unsafe_allow_html=True,
    )

    col3, col4 = st.columns(2)

    with col3:
        st.markdown(
            "<h5 style='text-align: left;'>Benchmark:</h5>", unsafe_allow_html=True
        )
        st.image("benchmark_iv.png")

    with col4:
        st.markdown(
            "<h5 style='text-align: left;'>Iv's Calculados:</h5>",
            unsafe_allow_html=True,
        )

        df_final = pd.concat([df_iv_qualitativas, df_iv_quantitativas])
        df_final = df_final.sort_values(by="iv", ascending=False)

        def color_cells(val):
            if val > 0.5:
                color = "darkgreen"
            elif val > 0.3:
                color = "green"
            elif val > 0.1:
                color = "yellow"
            elif val > 0.02:
                color = "darkred"
            else:
                color = "red"
            return "background-color: %s" % color

        st.dataframe(df_final.style.applymap(color_cells), height=475)

    st.markdown(
        """<br><br><h5 style='text-align: justify;'>Agora que já temos os IV's, podemos definir quais as variáveis mais importantes para o estudo.<br>Para isso, selecionaremos as 5 variáveis que tiveram o maior IV.<br>São elas:<br><br>
        <ul><li>Faz_hora_extras?</li><li>Salário</li><li>Idade</li><li>Tempo_de_carreira</li><li>Estado_Civil</li></ul></h5><br><br>""",
        unsafe_allow_html=True,
    )
