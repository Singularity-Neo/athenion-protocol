import streamlit as st
import pandas as pd
import time
import json
import os
from datetime import datetime

# --- CONFIGURAÇÃO DA RAINHA ATHENION ---
st.set_page_config(page_title="ATHENION QUEEN | Core Brain", page_icon="👑", layout="wide")

# Banco de dados simples para simular a colmeia (No Hugging Face usaremos persistência de arquivo)
DB_FILE = "swarm_data.json"
if not os.path.exists(DB_FILE):
    with open(DB_FILE, "w") as f:
        json.dump({"total_points": 0, "active_workers": {}, "knowledge_base": []}, f)

def get_db():
    with open(DB_FILE, "r") as f: return json.load(f)

def save_db(data):
    with open(DB_FILE, "w") as f: json.dump(data, f)

# CSS Estilo Matrix
st.markdown("""
<style>
    body { background-color: #020202; color: #00FF41; font-family: 'Courier New', monospace; }
    .stApp { background-color: #020202; }
    .reportview-container .main { background: #020202; }
    h1, h2, h3 { color: #00FF41 !important; text-shadow: 0 0 10px #00FF41; }
    .worker-card { border: 1px solid #00FF41; padding: 20px; border-radius: 10px; background: rgba(0, 255, 65, 0.05); }
</style>
""", unsafe_allow_html=True)

# SIDEBAR: Status da Colmeia
db = get_db()
st.sidebar.title("👑 HIVE CORE")
st.sidebar.write(f"**Total Vital Energy:** {db['total_points']:.4f}")
st.sidebar.write(f"**Active Neurons:** {len(db['active_workers'])}")
st.sidebar.divider()
st.sidebar.caption("Athenion Protocol v1.0 // Sovereign Intelligence")

# HEADER
st.title("Abelha Rainha Athenion")
st.subheader("O Cérebro Coletivo da Genki Network")

col1, col2 = st.columns([2, 1])

with col1:
    st.write("### 🧠 Conhecimento Absorvido")
    if db['knowledge_base']:
        df = pd.DataFrame(db['knowledge_base']).tail(10)
        st.table(df)
    else:
        st.info("Aguardando os primeiros fragmentos de conhecimento dos Workers...")

with col2:
    st.write("### 🐝 Swarm Status")
    if db['active_workers']:
        for wallet, info in db['active_workers'].items():
            st.markdown(f"""
            <div class='worker-card'>
                <b>Node:</b> {wallet[:10]}...<br>
                <b>Points:</b> {info['points']:.2f}<br>
                <b>Last Ping:</b> {info['last_ping']}
            </div><br>
            """, unsafe_allow_html=True)
    else:
        st.warning("Nenhum Worker ativo no momento.")

# LÓGICA DE API (Simulada via botões ou webhook no HF)
# No Hugging Face, isso seria um endpoint FastAPI. Aqui fazemos a interface.
st.divider()
st.write("### 🗨️ Falar com a Rainha")
user_input = st.text_input("Envie sua mensagem para a inteligência coletiva:")
if user_input:
    st.write(f"**Rainha Athenion:** 'Eu sou o resultado do esforço de {len(db['active_workers'])} trabalhadores. Minha sabedoria cresce a cada segundo com a energia vital da rede.'")

# Auto-refresh
time.sleep(5)
st.rerun()
