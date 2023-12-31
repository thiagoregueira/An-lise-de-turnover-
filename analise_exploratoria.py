import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


@st.cache_data
def load_data():
    df = pd.read_excel("Base_RH.xlsx", sheet_name="Base")
    return df


def app():
    st.markdown(
        """
        <h1 style='text-align: left;'>Análise Exploratória</h1>
        <br>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <h2 style='text-align: center;'>Funcionário_deixou_a_empresa X Faz_hora_extras?</h2><br><br>
        """,
        unsafe_allow_html=True,
    )

    df = load_data()

    # Análise bidimensional entre as variáveis mais importantes do IV

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
            <h3 style='text-align: center;'>Frequência absoluta</h3><br>
            """,
            unsafe_allow_html=True,
        )

        # Calcular a frequência absoluta
        freq_abs = (
            df.groupby("Funcionário_deixou_a_empresa")["Faz_hora_extras?"]
            .value_counts()
            .unstack(fill_value=0)
        )

        st.dataframe(freq_abs.T, use_container_width=True)

        # Criando o grafico de pizza com plotly usando a frequencia relativa
        freq_rel = round(freq_abs.div(freq_abs.sum(axis=1), axis=0) * 100)

        fig_horas_extras = px.pie(
            freq_rel.T,
            values="Sim",
            names=["Não", "Sim"],
            title="Funcionários que deixaram a empresa X Fizeram hora extra?",
            height=400,
            width=800,
            color_discrete_sequence=["#0068c9", "#83c9ff"],
        )

        # aumentar o tamanho da fonte do titulo
        fig_horas_extras.update_layout(title_font_size=20)

        # Exibindo o grafico

        st.plotly_chart(fig_horas_extras, use_container_width=True)

    with col2:
        st.markdown(
            """
            <h3 style='text-align: center;'>Frequência relativa (%)</h3><br>
            """,
            unsafe_allow_html=True,
        )

        # Calcular a frequência relativa
        freq_rel = round(freq_abs.div(freq_abs.sum(axis=1), axis=0) * 100)

        st.dataframe(freq_rel.T, use_container_width=True)

        st.markdown(
            """
            <br>
            <p style='text-align: justify;'>O gráfico mostra que a saída de funcionários da empresa está quase igualmente dividida entre aqueles que fazem horas extras (54%) e os que não fazem (46%).<br> Para reduzir essa rotatividade, uma estratégia eficaz pode ser conduzir uma pesquisa detalhada para entender as razões específicas por trás das decisões dos funcionários em fazer horas extras e com base nas respostas, a empresa pode implementar políticas mais direcionadas para reter ambos os grupos de funcionários.<br>Por exemplo, se a pesquisa revelar que os funcionários que estão dispostos a fazer horas extras estão deixando a empresa devido à falta de compensação adequada, a empresa pode considerar revisar sua política de horas extras. Da mesma forma, se os funcionários que não estão dispostos a fazer horas extras estão deixando a empresa devido à pressão para trabalhar além do horário normal, a empresa pode precisar reavaliar suas expectativas de carga de trabalho.</p>
    """,
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <br><h2 style='text-align: center;'>Funcionário_deixou_a_empresa X faixas de Salários</h2><br><br>
        """,
        unsafe_allow_html=True,
    )

    # faixas de salários

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

    col3, col4, col5 = st.columns(3)

    with col3:
        st.markdown(
            """
            <h3 style='text-align: center;'>Frequência absoluta</h3><br>
            """,
            unsafe_allow_html=True,
        )

        # Calcular a frequencia absoluta

        freq_abs = (
            df.groupby("Funcionário_deixou_a_empresa")["Salário_5"]
            .value_counts()
            .unstack(fill_value=0)
        )

        st.dataframe(freq_abs.T, use_container_width=True)

    with col4:
        st.markdown(
            """
            <h3 style='text-align: center;'>Frequência relativa (%)</h3><br>
            """,
            unsafe_allow_html=True,
        )

        # Calcular a frequencia relativa

        freq_rel = round(freq_abs.div(freq_abs.sum(axis=1), axis=0) * 100)

        st.dataframe(freq_rel.T, use_container_width=True)

    with col5:
        st.markdown(
            """
            <h3 style='text-align: center;'>Frequência acumulada (%)</h3><br>
            """,
            unsafe_allow_html=True,
        )

        # Calcular a frequencia acumulada em percentual

        freq_acum_pct = freq_rel.cumsum(axis=1)

        st.dataframe(freq_acum_pct.T, use_container_width=True)

    col6, col7 = st.columns(2)

    with col6:
        # Criando grafico de barras dos intervalos de Salário_5 com os valores de frequencia absoluta da coluna "Sim"
        fig = px.bar(
            freq_abs.T,
            x=[
                "0-2500",
                "2501-5000",
                "5001-7500",
                "7501-10000",
                "10001-15000",
                "15001-20000",
            ],
            y="Sim",
            title="Funcionários que deixaram a empresa por faixa Salário",
            labels={"Sim": "Frequência Absoluta", "x": "faixas de Salários"},
            height=600,
            text="Sim",
        )

        # aumentar o tamanho da fonte do titulo
        fig.update_layout(title_font_size=20)

        # Adicionar o gráfico de linha da frequencia acumulada ao gráfico de barras existentes
        fig.add_trace(
            go.Scatter(
                x=[
                    "0-2500",
                    "2501-5000",
                    "5001-7500",
                    "7501-10000",
                    "10001-15000",
                    "15001-20000",
                ],
                y=freq_acum_pct.T["Sim"],
                text=freq_acum_pct.T["Sim"],
                mode="lines+markers+text",
                name="Frequência Acumulada %",
                textposition="top center",
            )
        )

        # exibir o grafico
        st.plotly_chart(fig, use_container_width=True)

    with col7:
        st.markdown(
            """
            <br>
            <p style='text-align: justify;'>A maior parte dos funcionários que deixam a empresa estão na faixa salarial mais baixa (menos de 5000). A rotatividade é particularmente alta na faixa de 0 a 2500, onde mais da metade dos funcionários deixa a empresa.
            <br>
            <h4 style='text-align: left;'>Sugestões:</h4>
            <strong>Revisão Salarial: </strong>Considere revisar as estruturas salariais, especialmente para aqueles na faixa de 0 a 5000, para garantir que os salários sejam competitivos e justos.
            <br><br>
            <strong>Benefícios Adicionais: </strong>Ofereça benefícios adicionais, como seguro saúde, dias de folga flexíveis, ou oportunidades de aprendizado e desenvolvimento.
            <br><br>
            <strong>Oportunidades de Crescimento: </strong>Proporcione oportunidades claras de crescimento profissional para aumentar a satisfação dos funcionários e reduzir a rotatividade.
            </p>
    """,
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <br><h2 style='text-align: center;'>Funcionário_deixou_a_empresa X faixas de Idades</h2><br><br>
        """,
        unsafe_allow_html=True,
    )

    col8, col9, col10 = st.columns(3)

    with col8:
        st.markdown(
            """
            <h3 style='text-align: center;'>Frequência Absoluta</h3><br>
            """,
            unsafe_allow_html=True,
        )

        # Calcular a frequencia absoluta

        freq_abs = (
            df.groupby("Funcionário_deixou_a_empresa")["Idade_5"]
            .value_counts()
            .unstack(fill_value=0)
        )

        st.dataframe(freq_abs.T, use_container_width=True)

    with col9:
        st.markdown(
            """
            <h3 style='text-align: center;'>Frequência Relativa</h3><br>
            """,
            unsafe_allow_html=True,
        )

        # Calcular a frequencia relativa

        freq_rel = round(freq_abs.div(freq_abs.sum(axis=1), axis=0) * 100)

        st.dataframe(freq_rel.T, use_container_width=True)

    with col10:
        st.markdown(
            """
            <h3 style='text-align: center;'>Frequência Acumulada</h3><br>
            """,
            unsafe_allow_html=True,
        )

        # Calcular a frequencia acumulada

        freq_acum_pct = freq_rel.cumsum(axis=1)

        st.dataframe(freq_acum_pct.T, use_container_width=True)

    col11, col12 = st.columns(2)

    with col11:
        # Criar o primeiro gráfico de barras
        fig = px.bar(
            freq_abs.T,
            x=freq_abs.T.index,
            y=freq_abs.T["Sim"],
            text=freq_abs.T["Sim"],
            title="Funcionários que deixaram a empresa por faixas de Idades",
            labels={"y": "Frequência Absoluta", "Idade_5": "faixas de Idades"},
            height=600,
        )

        # aumentar o tamanho da fonte do titulo
        fig.update_layout(title_font=dict(size=20))

        # Adicionar o gráfico de linha da frequencia acumulada ao gráfico de barras existentes
        fig.add_trace(
            go.Scatter(
                x=freq_acum_pct.T.index,
                y=freq_acum_pct.T["Sim"],
                text=freq_acum_pct.T["Sim"],
                mode="lines+markers+text",
                name="Frequência Acumulada %",
                textposition="top center",
            )
        )

        # exibir o grafico
        st.plotly_chart(fig, use_container_width=True)

    with col12:
        st.markdown(
            """
            <br>
            <br>
            <br>
            <br>
            <p style='text-align: justify;'>Os dados e o gráfico indicam que a maior parte dos funcionários que deixam a empresa estão na faixa etária de 18-35 anos, correspondendo a 64%.
            <br>
            <h4 style='text-align: left;'>Sugestões:</h4>
            <strong>Desenvolvimento Profissional: </strong>Implementar programas de desenvolvimento profissional para avanço na carreira de acordo com cada faixa etária.
            <br><br>
            <strong>Equilíbrio Trabalho-Vida: </strong>Melhorar o equilíbrio entre trabalho e vida pessoal, conforme cada faixa etária exige.
            <br><br>
            </p>
    """,
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <br><h2 style='text-align: center;'>Funcionário deixou a empresa X Tempo de Carreira</h2><br><br>
        """,
        unsafe_allow_html=True,
    )

    col13, col14, col15 = st.columns(3)

    with col13:
        st.markdown(
            """
            <h3 style='text-align: center;'>Frequência Absoluta</h3><br>
            """,
            unsafe_allow_html=True,
        )

        # Calcular a frequencia absoluta

        freq_abs = (
            df.groupby("Funcionário_deixou_a_empresa")["Tempo_de_carreira_5"]
            .value_counts()
            .unstack(fill_value=0)
        )

        st.dataframe(freq_abs.T, use_container_width=True)

    with col14:
        st.markdown(
            """
            <h3 style='text-align: center;'>Frequência Relativa</h3><br>
            """,
            unsafe_allow_html=True,
        )

        # Calcular a frequencia relativa

        freq_rel = round(freq_abs.div(freq_abs.sum(axis=1), axis=0) * 100)

        st.dataframe(freq_rel.T, use_container_width=True)

    with col15:
        st.markdown(
            """
            <h3 style='text-align: center;'>Frequência Acumulada</h3><br>
            """,
            unsafe_allow_html=True,
        )

        # Calcular a frequencia acumulada

        freq_acum_pct = freq_rel.cumsum(axis=1)

        st.dataframe(freq_acum_pct.T, use_container_width=True)

    col16, col17 = st.columns(2)

    with col16:
        # Criar o primeiro gráfico de barras
        fig = px.bar(
            freq_abs.T,
            x=freq_abs.T.index,
            y=freq_abs.T["Sim"],
            text=freq_abs.T["Sim"],
            title="Funcionários que deixaram a empresa por faixas de Tempo de Carreira",
            labels={
                "y": "Frequência Absoluta",
                "Tempo_de_carreira_5": "faixas de Tempo de Carreira",
            },
            height=600,
        )

        # aumentar o tamanho da fonte do titulo
        fig.update_layout(title_font=dict(size=16))

        # Adicionar o gráfico de linha da frequencia acumulada ao gráfico de barras existentes
        fig.add_trace(
            go.Scatter(
                x=freq_acum_pct.T.index,
                y=freq_acum_pct.T["Sim"],
                text=freq_acum_pct.T["Sim"],
                mode="lines+markers+text",
                name="Frequência Acumulada %",
                textposition="top center",
            )
        )

        # exibir o grafico
        st.plotly_chart(fig, use_container_width=True)

    with col17:
        st.markdown(
            """
            <br>
            <br>
            <br>
            <br>
            <p style='text-align: justify;'>Com base nos detalhes do gráfico os dados indicam que a maior parte dos funcionários que deixam a empresa estão na faixa de 0-10 anos de carreira, correspondendo a 76% dos funcionários.
            <br>
            <h4 style='text-align: left;'>Sugestões:</h4>
            <strong>Engajamento: </strong>Aumentar o engajamento dos funcionários através de programas de reconhecimento e recompensa, principalmente dando mais "voz" aos os que estão presentes na faixa de foco(0-10 anos).
            <br><br>
            <strong>Desenvolvimento Profissional: </strong>Oferecer oportunidades de desenvolvimento profissional e avanço na carreira, desde os recém contratados até os que possuem mais tempo de carreira.
            <br><br>
            </p>""",
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <br><h2 style='text-align: center;'>Funcionário deixou a empresa X Estado Civil</h2><br><br>
        """,
        unsafe_allow_html=True,
    )

    # Definir a ordem desejada das categorias
    ordem_estado_civil = ["Solteiro", "Casado", "Divorciado"]

    # Reordenar as categorias da coluna 'Estado_civil'
    df["Estado_Civil"] = pd.Categorical(
        df["Estado_Civil"], categories=ordem_estado_civil, ordered=True
    )

    col18, col19 = st.columns(2)

    with col18:
        st.markdown(
            """
            <h3 style='text-align: center;'>Frequência Absoluta</h3><br>
            """,
            unsafe_allow_html=True,
        )

        # Calcular a frequência absoluta
        freq_abs = (
            df.groupby("Funcionário_deixou_a_empresa")["Estado_Civil"]
            .value_counts()
            .unstack(fill_value=0)
        )

        st.dataframe(freq_abs.T, use_container_width=True)

        # Calcular a frequencia relativa
        freq_rel = round(freq_abs.div(freq_abs.sum(axis=1), axis=0) * 100)

        # Plot com plotly um grafico de barras para cada categoria de "Estado_Civil"
        fig = px.bar(
            freq_abs.T,
            x=["Solteiro", "Casado", "Divorciado"],
            y="Sim",
            title="Funcionários que deixaram a empresa X Estado Civil",
            labels={"Sim": "Frequência Absoluta", "x": "Estado Civil"},
            height=600,
            text="Sim",
        )

        # aumentar o tamanho da fonte do titulo
        fig.update_layout(title_font=dict(size=20))

        # Adicionar o gráfico de linha ao gráfico de barras existentes
        fig.add_trace(
            go.Scatter(
                x=["Solteiro", "Casado", "Divorciado"],
                y=freq_rel.T["Sim"],
                text=freq_rel.T["Sim"],
                mode="lines+markers+text",
                name="Frequência Relativa %",
                textposition="top center",
            )
        )

        # exibir o grafico
        st.plotly_chart(fig, use_container_width=True)

    with col19:
        st.markdown(
            """
            <h3 style='text-align: center;'>Frequência Relativa (%)</h3><br>
            """,
            unsafe_allow_html=True,
        )

        # Calcular a frequencia relativa
        freq_rel = round(freq_abs.div(freq_abs.sum(axis=1), axis=0) * 100)

        st.dataframe(freq_rel.T, use_container_width=True)

        st.markdown(
            """
            <br>
            <br>
            <br>
            <br>
            <p style='text-align: justify;'>Os dados e o gráfico indicam que os funcionários solteiros (51%) têm uma tendência mais alta de deixar a empresa, seguidos por casados (35%) e divorciados (14%).
            <br>
            <h4 style='text-align: left;'>Sugestões:</h4>
            <strong>Benefícios Específicos: </strong>Oferecer benefícios adicionais ou programas de bem-estar específicos para atender às necessidades variadas dos funcionários de acordo com seu estado civil.
            <br><br>
            <strong>Oportunidades para Solteiros: </strong>Para os funcionários solteiros, oportunidades de desenvolvimento de carreira e networking podem ser mais atrativas.
            <br><br>
            <strong>Apoio aos Casados e Divorciados: </strong> Para os funcionários casados e divorciados, a empresa pode considerar oferecer um melhor equilíbrio entre trabalho e vida pessoal, como horários flexíveis ou apoio à família.
                    Essas medidas podem ajudar a melhorar a retenção de funcionários na empresa.
            </p>""",
            unsafe_allow_html=True,
        )
