import streamlit as st

from streamlit_option_menu import option_menu

import entendendo_o_negocio, tratamento_dados, calculando_ivs, analise_exploratoria, conclusao  # noqa: E401


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
        # app = st.sidebar(
        with st.sidebar:
            app = option_menu(
                menu_title="⬇️Etapas: ",
                options=[
                    "💼Entendendo o Negócio",
                    "✅Tratamento de Dados",
                    "🧮Calculando os IV's",
                    "📊Análise Exploratória",
                    "👍Conclusão",
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

        if app == "💼Entendendo o Negócio":
            entendendo_o_negocio.app()
        if app == "✅Tratamento de Dados":
            tratamento_dados.app()
        if app == "🧮Calculando os IV's":
            calculando_ivs.app()
        if app == "📊Análise Exploratória":
            analise_exploratoria.app()
        if app == "👍Conclusão":
            conclusao.app()


multiapp = MultiApp()
multiapp.run()
