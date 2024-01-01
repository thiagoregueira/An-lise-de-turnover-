import streamlit as st
from streamlit_option_menu import option_menu

import entendendo_o_negocio, tratamento_dados, calculando_ivs, analise_exploratoria, base_dados  # noqa: E401

st.set_page_config(
    page_title="Análise Turnover",
    page_icon="📊",
    layout="wide",
)


class MultiApp:
    def __init__(self):
        self.apps = []

    def add_app(self, title, func):
        self.apps.append({"title": title, "function": func})

    def run(self):
        with st.sidebar:
            app_container = st.container()
            author_container = st.container()

            # Configurações do container das análises
            with app_container:
                st.write(
                    """
                    # Análises:
                    """
                )
                app = option_menu(
                    menu_title="⬇️Etapas: ",
                    options=[
                        "💼Entendendo o Negócio",
                        "✅Tratamento de Dados",
                        "🧮Calculando os IV's",
                        "📊Análise Exploratória",
                        "📊Base de Dados",
                    ],
                    default_index=0,
                    styles={
                        "container": {
                            "padding": "5!important",
                            "background-color": "black",
                        },
                        "nav-link": {
                            "color": "white",
                            "font-size": "16px",
                            "text-align": "left",
                            "margin": "0px",
                            "--hover-color": "blue",
                        },
                        "nav-link-selected": {"background-color": "#02ab21"},
                    },
                )

                st.write("---")

            # Configurações do container do autor e copyright
            with author_container:
                col1, col2 = st.columns([1, 2])

                with col1:
                    st.image("profile-pic(4).png", width=100)
                with col2:
                    st.markdown(
                        """
                        - Thiago Regueira
                        - [Linkedin](https://www.linkedin.com/in/thiagoregueira/)
                        - [Github](https://github.com/thiagoregueira)
                        """
                    )
                st.markdown(
                    """
                    - Os dados utilizados pertencem a [preditiva.ai](https://www.preditiva.ai) e são usados apenas para fins educacionais.
                    \n
                    - Este projeto foi desenvolvido como parte do estudo do autor e não tem nenhuma finalidade comercial.
                    """
                )

        if app == "💼Entendendo o Negócio":
            entendendo_o_negocio.app()
        if app == "✅Tratamento de Dados":
            tratamento_dados.app()
        if app == "🧮Calculando os IV's":
            calculando_ivs.app()
        if app == "📊Análise Exploratória":
            analise_exploratoria.app()
        if app == "📊Base de Dados":
            base_dados.app()


multiapp = MultiApp()
multiapp.run()
