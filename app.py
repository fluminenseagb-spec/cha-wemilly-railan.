import streamlit as st
import json
import os
from streamlit_autorefresh import st_autorefresh

# 1. Configuração da Página e Estilo CSS (O segredo do visual)
st.set_page_config(page_title="Lista de Presentes - Wemilly & Railan", page_icon="🏠", layout="centered")

st.markdown("""
    <style>
    /* Fundo e Fonte */
    .stApp {
        background-color: #FDF8F5;
    }
    
    /* Card do Cabeçalho */
    .header-card {
        background: linear-gradient(180deg, #A68472 0%, #D4BBA9 100%);
        padding: 40px 20px;
        border-radius: 0px 0px 30px 30px;
        text-align: center;
        color: white;
        margin: -60px -20px 20px -20px;
    }
    
    /* Estilo dos Títulos de Categoria */
    .cat-header {
        color: #5D4037;
        font-weight: bold;
        border-bottom: 2px solid #D4BBA9;
        padding-bottom: 5px;
        margin-top: 30px;
    }

    /* Card de Item */
    .gift-card {
        background: white;
        padding: 15px;
        border-radius: 15px;
        box-shadow: 0px 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 10px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    /* Botão Selecionar */
    div.stButton > button {
        background-color: #D37546 !important;
        color: white !important;
        border-radius: 20px !important;
        border: none !important;
        padding: 5px 20px !important;
    }
    </style>
    
    <div class="header-card">
        <h1 style='font-family: serif;'>Chá de Casa Nova</h1>
        <h3 style='font-weight: 300;'>Wemilly & Railan</h3>
        <p>Escolha um presente e nos ajude a construir nosso lar com muito amor 🏠</p>
    </div>
""", unsafe_allow_html=True)

st_autorefresh(interval=5000, key="datarefresh")

DB_FILE = "lista_presentes.json"
LISTA_INICIAL = {
    "🍽️ Cozinha": ["Pratos fundos", "Pratos rasos", "Copos grandes", "Taças", "Talheres", "Xícaras"],
    "🥣 Utensílios": ["Refratários de vidro", "Garrafa de café", "Jarras de vidro", "Vasilhas (Café/Açúcar)", "Farinheira", "Açucareiro", "Manteigueira", "Colheres de silicone"],
    "🍳 Panelas": ["Panelas antiaderentes", "Frigideiras (P/M/G)", "Escorredor de macarrão", "Escorredor de louça"],
    "🛏️ Cama, Mesa e Banho": ["Cama super king", "Tapetes", "Panos de prato", "Cortinas"],
    "🔌 Eletro": ["Panela de arroz elétrica", "Cafeteira elétrica", "Air fryer"]
}

def carregar_dados():
    if not os.path.exists(DB_FILE):
        dados = {item: {"escolhido": False, "por": ""} for cat in LISTA_INICIAL.values() for item in cat}
        with open(DB_FILE, "w") as f: json.dump(dados, f)
        return dados
    with open(DB_FILE, "r") as f: return json.load(f)

dados = carregar_dados()

# --- Barra de Progresso ---
total = len(dados)
escolhidos = sum(1 for v in dados.values() if v["escolhido"])
percentual = int((escolhidos / total) * 100)

st.write(f"**{escolhidos} de {total} presentes escolhidos**")
st.progress(escolhidos / total)
st.write(f"✨ {percentual}% concluído")

# --- Lista de Presentes ---
for categoria, itens in LISTA_INICIAL.items():
    st.markdown(f"<h3 class='cat-header'>{categoria}</h3>", unsafe_allow_html=True)
    
    for item in itens:
        status = dados[item]
        with st.container():
            col1, col2 = st.columns([3, 2])
            
            with col1:
                if status["escolhido"]:
                    st.markdown(f"<span style='color: #9e9e9e;'><s>{item}</s></span>", unsafe_allow_html=True)
                else:
                    st.markdown(f"**{item}**")
            
            with col2:
                if status["escolhido"]:
                    st.button(f"🎁 Por {status['por']}", key=f"btn_{item}", disabled=True)
                else:
                    with st.popover("🎁 Selecionar"):
                        nome = st.text_input("Seu nome", key=f"nome_{item}")
                        if st.button("Confirmar", key=f"conf_{item}"):
                            if nome:
                                dados[item] = {"escolhido": True, "por": nome}
                                with open(DB_FILE, "w") as f: json.dump(dados, f)
                                st.success("Obrigado!")
                                st.rerun()

# Sidebar ADM
with st.sidebar:
    st.title("⚙️ Admin")
    if st.text_input("Senha", type="password") == "123":
        if st.button("Limpar Lista"):
            if os.path.exists(DB_FILE): os.remove(DB_FILE)
            st.rerun()