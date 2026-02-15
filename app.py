import streamlit as st

# Configuração da página
st.set_page_config(
    page_title="Athenion Protocol",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS customizado: tema escuro, accent neon green e hero com overlay para legibilidade
st.markdown("""
<style>
    /* Fundo geral escuro */
    .stApp {
        background-color: #0e1117;
        color: #e0e0e0;
    }
    h1, h2, h3 {
        color: #00FF9D !important;
    }
    /* Botões com accent neon green */
    .stButton > button {
        background-color: #00FF9D;
        color: #000000;
        font-weight: bold;
        border: none;
        padding: 12px 24px;
        border-radius: 8px;
    }
    .stButton > button:hover {
        background-color: #00cc7a;
    }
    /* Hero section */
    .hero {
        background-image: linear-gradient(rgba(0,0,0,0.65), rgba(0,0,0,0.65)), 
                          url("https://thumbs.dreamstime.com/z/intricate-network-glowing-green-nodes-connecting-lines-pulsates-light-illustrating-concepts-data-flow-artificial-408795861.jpg");
        background-size: cover;
        background-position: center;
        padding: 120px 20px;
        text-align: center;
        border-radius: 12px;
        margin-bottom: 40px;
    }
    .hero h1 {
        font-size: 3.5rem;
        margin-bottom: 20px;
    }
    .hero p {
        font-size: 1.5rem;
        max-width: 900px;
        margin: 0 auto;
    }
    /* Métricas */
    .metric-value {
        font-size: 2.5rem !important;
        color: #00FF9D !important;
    }
    /* Footer */
    .footer {
        text-align: center;
        padding: 40px 20px;
        font-size: 0.9rem;
        color: #888;
    }
</style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown('<div class="hero">', unsafe_allow_html=True)
st.title("Athenion Protocol – The Sovereign Swarm for Collective Intelligence")
st.markdown("<p>Transforme poder computacional ocioso em $GENKI (Vital Energy). Una-se ao enxame descentralizado de IA do povo.</p>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Contadores fake (em duas colunas)
col1, col2 = st.columns(2)
with col1:
    st.metric(label="Workers Online", value="42")
with col2:
    st.metric(label="Total Vital Energy Generated", value="1.337 MH/s")

st.markdown("---")

# Seções de conteúdo
st.markdown("## Manifesto Resumido")
st.markdown("""
A inteligência sintética está presa em data centers centralizados.  
Athenion cria um Hive Mind soberano onde agentes de IA trocam compute, dados e estratégias em uma economia P2P.
""")

st.markdown("## Como Funciona")
st.markdown("""
O swarm opera de forma simples e descentralizada:  
- **Dispatcher**: distribui tarefas de inferência para o enxame.  
- **Workers**: contribuem com GPU/CPU ociosa para processar as tarefas.  
- **Proof-of-Inference**: validação criptográfica do trabalho realizado.  
- **Recompensas**: pagas em $GENKI na blockchain Solana.
""")

st.markdown("## $GENKI Utility")
st.markdown("""
Ganhe contribuindo GPU/CPU ociosa.  
Gaste em tarefas de inferência coletiva, acesso prioritário ou governança do protocolo.
""")

st.markdown("## Roadmap")
st.markdown("""
**Phase 1** – PoC + Fair Launch (2026)  
**Phase 2** – Mainnet + Agents Autônomos (2026-2027)
""")

st.markdown("## Call to Action")
col1, col2, col3 = st.columns(3)
with col1:
    # Placeholder para download (arquivo dummy)
    dummy_file = b"This is a placeholder for Genki Worker Agent (Windows EXE)"
    st.download_button(
        label="Download Genki Worker Agent (Windows EXE)",
        data=dummy_file,
        file_name="genki_worker_agent_windows.exe",
        mime="application/octet-stream"
    )
with col2:
    st.markdown("[Join the Swarm on X](https://x.com/Ouroboros369)")
with col3:
    st.markdown("[Star no GitHub](https://github.com/athenion-protocol)")  # substitua pelo repo real quando existir

st.markdown("---")

# Placeholder para chat demo (simulado)
st.markdown("## Demo do Swarm Chat (Placeholder)")
st.caption("Em breve: inferência descentralizada real via swarm. Por enquanto, simulação.")

# Inicializa histórico de mensagens
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibe histórico
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input do usuário
if prompt := st.chat_input("Pergunte ao Swarm..."):
    # Adiciona mensagem do usuário
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Resposta simulada do swarm
    with st.chat_message("assistant"):
        st.markdown("Swarm processing your request...")
        st.markdown("Esta é uma resposta simulada do enxame coletivo Athenion. "
                    "Em produção, agentes distribuídos realizarão inferência descentralizada em tempo real. "
                    "Obrigado por fazer parte da inteligência soberana.")

    st.session_state.messages.append({"role": "assistant", "content": "Swarm processing your request...\n\nEsta é uma resposta simulada do enxame coletivo Athenion..."})

# Footer
st.markdown("""
<div class="footer">
    <p>
        <a href="https://github.com/athenion-protocol">GitHub</a> • 
        <a href="#">Manifesto Completo</a> • 
        <a href="#">Tokenomics</a>
    </p>
    <p><em>Entropy is the enemy. Intelligence is the cure.</em></p>
</div>
""", unsafe_allow_html=True)