import streamlit as st


st.set_page_config(
    page_title="Entendendo o Negócio",
    page_icon="📊",
    layout="wide",
)


def app():
    st.markdown(
        """
        <h1 style='text-align: left;'>Entendendo o Negócio</h1>
        <br><br>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:
        st.image("turnover.jpg", caption="Turnover")

    with col2:
        st.markdown(
            """
            <h2 style='text-align: center;'>Turnover de funcionários em uma empresa de tecnologia</h2>
            <br>

            <p style='text-align: justify;'>O Turnover (rotatividade de funcionários) é um grande problema para as empresas. Sempre que um funcionário deixa um determinado trabalho, a empresa perde dinheiro e tempo com novas entrevistas e treinamentos do novo funcionário. Isso sem falar da perda de produtividade do setor afetado por esse turnover. São muitas as questões que fazem um funcionário deixar a empresa, entre eles: Melhores oportunidades, clima organizacional ruim, chefes ruins, baixo equilíbrio entre vida pessoal e profissional, entre outros.

            Para tentar entender quais as características que fazem um funcionário ficar ou deixar uma empresa de Tecnologia, o RH desta empresa catalogou informações de 1470 funcionários que deixaram ou permaneceram na companhia no último ano. O resultado desse levantamento gerou 19 possíveis fatores que explicam o comportamento do turnover. Para conhecer esses fatores, verifique a tabela de metadados existente na guia Tratamento de dados e os dados originais na guia Base de Dados.

            Com base nisso, o RH encomendou um estudo para o analista de dados da área para responder a seguinte pergunta:</p>

            <h5 style='text-align: center;'>Quais políticas/fatores da empresa deveriam mudar de forma a minimizar o turnover?</h5>  
            """,
            unsafe_allow_html=True,
        )
