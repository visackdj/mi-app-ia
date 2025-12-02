import streamlit as st
import google.generativeai as genai

# 1. Configuración de la página
st.set_page_config(page_title="Mi App IA", page_icon="🤖")
st.title("Mi Asistente Personal 🤖")

# 2. Conexión segura con Google (La clave no está visible aquí)
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except:
    st.error("Falta la API Key en los secretos.")

# 3. Interfaz del Chat
model = genai.GenerativeModel('gemini-pro')

# Historial simple (se borra al recargar la página)
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar mensajes anteriores
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Cuadro de texto para escribir
if prompt := st.chat_input("Escribe tu pregunta aquí..."):
    # Mostrar lo que escribiste
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Generar respuesta
    with st.chat_message("assistant"):
        response = model.generate_content(prompt)
        st.markdown(response.text)
    st.session_state.messages.append({"role": "assistant", "content": response.text})
