import streamlit as st
import google.generativeai as genai

# 1. Configuración de la página
st.set_page_config(page_title="Coach IA", page_icon="💪")
st.title("Mi Entrenador Personal 💪")
st.caption("Pídeme rutinas, dietas o consejos.")

# 2. Conexión a Google
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except:
    st.error("⚠️ No encontré la API Key. Revisa los 'Secrets'.")

# 3. Configuración del Modelo (USAMOS EL ESTÁNDAR COMPATIBLE)
# Usamos 'gemini-pro' que funciona en todas las cuentas
model = genai.GenerativeModel('gemini-1.5-flash')

# 4. Chat y Memoria
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar historial visual
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Lógica del Chat
if prompt := st.chat_input("Ej: Rutina de pecho para hoy..."):
    # Mostrar mensaje del usuario
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Generar respuesta
    with st.chat_message("assistant"):
        try:
            # Truco: Le decimos que es entrenador junto con tu pregunta
            prompt_entrenador = f"Actúa como un entrenador personal experto y responde esto: {prompt}"
            
            response = model.generate_content(prompt_entrenador)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Error: {e}")
