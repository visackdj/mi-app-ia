import streamlit as st
import google.generativeai as genai

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Coach IA", page_icon="💪")
st.title("Mi Entrenador Personal 💪")
st.caption("Rutinas, nutrición y consejos de entrenamiento.")

# --- CONEXIÓN INTELIGENTE ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    
    # 1. Obtenemos la lista de TODOS los modelos disponibles para tu cuenta
    modelos = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    
    # 2. BÚSQUEDA INTELIGENTE DEL MEJOR MODELO
    modelo_usar = None
    
    # Prioridad A: Buscar cualquier modelo que diga "flash" (son rápidos y con buen límite gratuito)
    for m in modelos:
        if "flash" in m:
            modelo_usar = m
            break # Encontramos uno, dejamos de buscar
    
    # Prioridad B: Si no hay flash, buscar "gemini-pro"
    if not modelo_usar:
        for m in modelos:
            if "gemini-pro" in m and "exp" not in m: # Evitamos los experimentales
                modelo_usar = m
                break

    # Prioridad C: Si todo falla, usar el primero de la lista (aunque sea experimental)
    if not modelo_usar:
        modelo_usar = modelos[0]

    # Mostrar discretamente qué modelo se eligió (para que sepas)
    print(f"Modelo seleccionado: {modelo_usar}") 

    # 3. Configurar el cerebro
    instrucciones = "Eres un entrenador personal experto. Responde de forma breve, motivadora y usa listas."
    model = genai.GenerativeModel(modelo_usar, system_instruction=instrucciones)

except Exception as e:
    st.error(f"Error de conexión: {e}")
    st.stop()

# --- CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ej: Rutina de pierna en casa..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    try:
        with st.chat_message("assistant"):
            chat = model.start_chat(history=[])
            response = chat.send_message(prompt)
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
    
    except Exception as e:
        # Si da error 429 (Límite), avisamos bonito
        if "429" in str(e):
            st.warning("🚦 Tráfico alto: Espera 1 minuto y vuelve a intentar (Límite de uso gratuito).")
        else:
            st.error(f"Error: {e}")
