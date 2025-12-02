import streamlit as st
import google.generativeai as genai

# 1. Configuración visual (Título e icono de fuerza)
st.set_page_config(page_title="Coach IA", page_icon="💪")
st.title("Mi Entrenador Personal 💪")
st.caption("Rutinas, nutrición y consejos de entrenamiento.")

# 2. Conexión segura
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except:
    st.error("⚠️ Falta la API Key. Configúrala en los 'Secrets' de Streamlit.")

# 3. Instrucciones del Entrenador (Aquí definimos su personalidad)
instrucciones = """
Eres un entrenador personal experto, motivador y directo.
Tu trabajo es crear rutinas de ejercicio, explicar técnica y dar consejos de nutrición.
Si te piden una rutina, pregunta siempre qué equipo tienen disponible.
Usa formato de listas y emojis para que sea fácil de leer en el celular.
"""

# Usamos el modelo 'gemini-1.5-flash' que es el más rápido y estable actualmente
model = genai.GenerativeModel(
    'gemini-1.5-flash',
    system_instruction=instrucciones
)

# 4. Chat y Memoria
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar historial
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Lógica de respuesta
if prompt := st.chat_input("Ej: Rutina de pecho en casa..."):
    # Guardar lo que escribiste
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    try:
        # Generar respuesta
        with st.chat_message("assistant"):
            chat = model.start_chat(history=[])
            # Enviamos el contexto de la conversación
            response = model.generate_content(prompt)
            st.markdown(response.text)
        
        # Guardar respuesta
        st.session_state.messages.append({"role": "assistant", "content": response.text})
    
    except Exception as e:
        st.error(f"Error de conexión: {e}")
