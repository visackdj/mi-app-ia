import streamlit as st
import google.generativeai as genai

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Coach IA", page_icon="💪")
st.title("Mi Entrenador Personal 💪")
st.caption("Rutinas, nutrición y consejos de entrenamiento.")

# --- CONEXIÓN Y SELECTOR AUTOMÁTICO DE MODELO ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    
    # 1. Buscamos qué modelos tienes disponibles
    modelos_disponibles = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    
    # 2. Intentamos elegir el mejor en orden de preferencia
    nombre_modelo = ""
    if "models/gemini-1.5-flash" in modelos_disponibles:
        nombre_modelo = "models/gemini-1.5-flash"
    elif "models/gemini-pro" in modelos_disponibles:
        nombre_modelo = "models/gemini-pro"
    else:
        # Si no están los habituales, tomamos el primero que funcione
        nombre_modelo = modelos_disponibles[0]
        
    # st.success(f"Conectado usando: {nombre_modelo}") # Descomenta para ver cuál eligió
    
    # 3. Creamos el Entrenador con el modelo encontrado
    instrucciones = "Eres un entrenador personal experto. Responde breve, motivador y usa listas."
    model = genai.GenerativeModel(nombre_modelo, system_instruction=instrucciones)

except Exception as e:
    st.error(f"Error de conexión: {e}")
    st.stop()

# --- CHAT Y MEMORIA ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar historial
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- LÓGICA DE RESPUESTA ---
if prompt := st.chat_input("Ej: Rutina de pierna en casa..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    try:
        with st.chat_message("assistant"):
            # Enviamos el historial completo para que recuerde la conversación
            chat_history = [{"role": m["role"], "parts": [m["content"]]} for m in st.session_state.messages if m["role"] != "system"]
            
            # Generar respuesta (usando invoke o chat según librería, aquí simplificado)
            chat = model.start_chat(history=[])
            response = chat.send_message(prompt)
            
            st.markdown(response.text)
        
        st.session_state.messages.append({"role": "assistant", "content": response.text})
    
    except Exception as e:
        st.error(f"Ocurrió un error: {e}")
