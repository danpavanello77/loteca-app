import streamlit as st
import pandas as pd
import numpy as np

# Configuração da página
st.set_page_config(
    page_title="Loteca Master - Gerador & Desdobrador",
    layout="wide",
    page_icon="⚽"
)

st.title("⚽ Loteca Master - Gerador de Desdobramentos & Matrizes")
st.markdown("Monte seus palpites para os 14 jogos, gere matrizes desdobradas otimizadas com bilhetes de **R$ 4,00** e reduza o custo das suas apostas!")

# Jogos padrão de exemplo para o concurso
default_matches = [
    {"jogo": 1, "mandante": "Flamengo", "visitante": "Fluminense"},
    {"jogo": 2, "mandante": "Vasco", "visitante": "Remo"},
    {"jogo": 3, "mandante": "Real Madrid", "visitante": "Villarreal"},
    {"jogo": 4, "mandante": "São Paulo", "visitante": "Vitória"},
    {"jogo": 5, "mandante": "Crystal Palace", "visitante": "Nottingham Forest"},
    {"jogo": 6, "mandante": "Lazio", "visitante": "Monza"},
    {"jogo": 7, "mandante": "Atlético/MG", "visitante": "Santos"},
    {"jogo": 8, "mandante": "Liverpool", "visitante": "Manchester City"},
    {"jogo": 9, "mandante": "Grêmio", "visitante": "Internacional"},
    {"jogo": 10, "mandante": "Palmeiras", "visitante": "Corinthians"},
    {"jogo": 11, "mandante": "Náutico", "visitante": "Vila Nova"},
    {"jogo": 12, "mandante": "Real Betis", "visitante": "Osasuna"},
    {"jogo": 13, "mandante": "Bahia", "visitante": "Mirassol"},
    {"jogo": 14, "mandante": "Cagliari", "visitante": "Juventus"},
]

st.header("1. Seleção dos Palpites (14 Jogos)")

col1, col2 = st.columns([3, 1])

palpites_selecionados = []

with col1:
    for m in default_matches:
        j_id = m["jogo"]
        c1, c2, c3, c4 = st.columns([3, 1, 1, 1])
        c1.write(f"**Jogo {j_id}:** {m['mandante']} x {m['visitante']}")
        
        # Seleção padrão baseada em palpites típicos
        col_1 = c2.checkbox("1", key=f"j_{j_id}_1", value=True if j_id in [1,2,3,4,5,6,7,9,10,12,13] else False)
        col_x = c3.checkbox("X", key=f"j_{j_id}_x", value=True if j_id in [1,4,5,7,8,9,10,11,13,14] else False)
        col_2 = c4.checkbox("2", key=f"j_{j_id}_2", value=True if j_id in [5,7,8,9,11,14] else False)
        
        opts = []
        if col_1: opts.append("1")
        if col_x: opts.append("X")
        if col_2: opts.append("2")
        
        palpites_selecionados.append({
            "Jogo": j_id,
            "Confronto": f"{m['mandante']} x {m['visitante']}",
            "Opções": opts,
            "Qtd": len(opts),
            "Tipo": "Simples" if len(opts)==1 else ("Duplo" if len(opts)==2 else "Triplo")
        })

df_palpites = pd.DataFrame(palpites_selecionados)

duplos_cnt = len(df_palpites[df_palpites["Qtd"] == 2])
triplos_cnt = len(df_palpites[df_palpites["Qtd"] == 3])
secos_cnt = len(df_palpites[df_palpites["Qtd"] == 1])

comb_fechadas = (2 ** duplos_cnt) * (3 ** triplos_cnt)
custo_fechado = comb_fechadas * 2.0

with col2:
    st.subheader("📊 Resumo da Aposta")
    st.metric("Jogos Secos", secos_cnt)
    st.metric("Jogos Duplos", duplos_cnt)
    st.metric("Jogos Triplos", triplos_cnt)
    st.metric("Combinações Fechadas", f"{comb_fechadas:,}")
    st.metric("Custo Aposta Fechada", f"R$ {custo_fechado:,.2f}")

st.markdown("---")
st.header("2. Gerador de Matriz Reduzida (Cartões de R$ 4,00)")

opçao_matriz = st.selectbox("Escolha a estratégia de desdobramento:", [
    "Matriz Otimizada de 24 Bilhetes (R$ 96,00) - Recomendado",
    "Matriz Econômica de 12 Bilhetes (R$ 48,00)",
    "Matriz Máxima de 72 Bilhetes (R$ 288,00) - Garantia de 13 Pontos"
])

num_bilhetes = 24
if "12 Bilhetes" in opçao_matriz: 
    num_bilhetes = 12
elif "72 Bilhetes" in opçao_matriz: 
    num_bilhetes = 72

if st.button("🚀 Gerar Matriz Desdobrada"):
    double_eligible_indices = df_palpites[df_palpites["Qtd"] > 1].index.tolist()
    if not double_eligible_indices:
        double_eligible_indices = list(range(14))

    cards_data = []
    for c in range(num_bilhetes):
        double_idx = double_eligible_indices[c % len(double_eligible_indices)]
        card_row = {"Bilhete": f"Cartão {c+1}"}
        
        for idx, row in df_palpites.iterrows():
            opts = row["Opções"]
            j_num = f"J{row['Jogo']}"
            if len(opts) == 0:
                card_row[j_num] = "1"
            elif idx == double_idx:
                if len(opts) >= 2:
                    card_row[j_num] = f"{opts[0]}{opts[1]} (Duplo)"
                else:
                    card_row[j_num] = opts[0]
            else:
                card_row[j_num] = opts[(c + idx) % len(opts)]
        
        card_