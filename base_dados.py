import streamlit as st
import pandas as pd


st.set_page_config(
    page_title="Análise Turnover",
    page_icon="📊",
    layout="wide",
)


@st.cache_data
def load_data():
    df = pd.read_excel("Base_RH.xlsx", sheet_name="Base")
    return df


def app():
    st.title("Base de Dados Original (Turnover)")

    st.dataframe(load_data(), width=2000, height=800)
