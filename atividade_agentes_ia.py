# app.py
import streamlit as st
import pandas as pd
from datetime import datetime

# === CONFIGURAÇÃO DO APP ===
st.set_page_config(
    page_title="EC Bahia - Jogos e Probabilidades",
    page_icon="⚽",
    layout="wide"
)

st.title("EC Bahia - Próximos Jogos e Chances de Vitória")
st.markdown("---")

# === DADOS SIMULADOS (sempre funcionam) ===
def gerar_jogos():
    return [
        {"Data": "16/11", "Jogo": "Bahia vs Fortaleza", "Horário": "16:00", "Competição": "Brasileirão"},
        {"Data": "23/11", "Jogo": "Internacional vs Bahia", "Horário": "19:00", "Competição": "Brasileirão"},
        {"Data": "30/11", "Jogo": "Bahia vs Flamengo", "Horário": "21:30", "Competição": "Brasileirão"},
        {"Data": "07/12", "Jogo": "Bahia vs Vasco", "Horário": "16:00", "Competição": "Brasileirão"},
        {"Data": "14/12", "Jogo": "Fluminense vs Bahia", "Horário": "18:00", "Competição": "Brasileirão"},
    ]

# === PROBABILIDADES POR FORÇA DO ADVERSÁRIO ===
def calcular_probabilidades(jogo):
    jogo_upper = jogo.upper()

    if "FORTALEZA" in jogo_upper:
        return 68, 20, 12   # Mais fraco → Bahia favorito
    elif "FLAMENGO" in jogo_upper:
        return 22, 25, 53   # Mais forte → Bahia azarão
    elif "INTERNACIONAL" in jogo_upper or "INTER" in jogo_upper:
        return 38, 30, 32   # Médio
    elif "VASCO" in jogo_upper:
        return 55, 25, 20
    elif "FLUMINENSE" in jogo_upper:
        return 35, 30, 35
    else:
        return 45, 28, 27   # Padrão

# === BOTÃO DE ATUALIZAÇÃO ===
if st.button("Atualizar Jogos e Probabilidades", type="primary", use_container_width=True):
    st.success("Atualizado com sucesso!")
    st.rerun()

# === CARREGAR E PROCESSAR DADOS ===
with st.spinner("Carregando jogos do Bahia..."):
    jogos = gerar_jogos()
    dados = []

    for jogo in jogos:
        v, e, d = calcular_probabilidades(jogo["Jogo"])
        dados.append({
            "Data": jogo["Data"],
            "Jogo": jogo["Jogo"],
            "Horário": jogo["Horário"],
            "Competição": jogo["Competição"],
            "Vitória (%)": v,
            "Empate (%)": e,
            "Derrota (%)": d
        })

    df = pd.DataFrame(dados)

# === EXIBIR TABELA ESTILIZADA ===
st.subheader("Próximos Jogos do Bahia")

# Destaque da maior chance
def destacar_maior(s):
    is_max = s == s.max()
    return ['background-color: #d4edda; font-weight: bold' if v else '' for v in is_max]

styled_df = df.style \
    .apply(destacar_maior, subset=["Vitória (%)", "Empate (%)", "Derrota (%)"]) \
    .format({
        "Vitória (%)": "{:.0f}",
        "Empate (%)": "{:.0f}",
        "Derrota (%)": "{:.0f}"
    }) \
    .set_properties(**{
        'text-align': 'center',
        'font-size': '14px'
    })

st.dataframe(styled_df, use_container_width=True)

# === GRÁFICO DO PRÓXIMO JOGO ===
if len(df) > 0:
    proximo = df.iloc[0]
    st.subheader(f"Próximo Jogo: {proximo['Jogo']} ({proximo['Data']})")

    chart_data = pd.DataFrame({
        "Resultado": ["Vitória", "Empate", "Derrota"],
        "Chance (%)": [proximo["Vitória (%)"], proximo["Empate (%)"], proximo["Derrota (%)"]]
    })

    st.bar_chart(chart_data.set_index("Resultado"), height=300, use_container_width=True)

    # Destaque do favorito
    max_val = chart_data["Chance (%)"].max()
    favorito = chart_data.loc[chart_data["Chance (%)"] == max_val, "Resultado"].values[0]
    st.success(f"**Maior chance: {favorito} ({max_val}%)**")

# === SIDEBAR ===
st.sidebar.image("https://upload.wikimedia.org/wikipedia/pt/5/5a/EC_Bahia_logo.png", width=100)
st.sidebar.header("Informações")
st.sidebar.info(f"**Última atualização:**\n{datetime.now().strftime('%d/%m/%Y %H:%M')}")
st.sidebar.caption("Fortaleza = adversário mais fraco\nFlamengo = adversário mais forte")

# === RODAPÉ ===
st.markdown("---")
st.caption("Fonte: Dados simulados com base em força dos times | App desenvolvido para demonstração")