import streamlit as st
import google.generativeai as genai

st.title("🕵️‍♂️ Diagnóstico de Llave")

try:
    # 1. Obtenemos la clave
    api_key = st.secrets["GOOGLE_API_KEY"]
    st.write(f"✅ Clave detectada (Termina en: ...{api_key[-5:]})")
    genai.configure(api_key=api_key)
    
    # 2. Preguntamos a Google qué modelos ve esta clave
    st.write("### 📋 Lista de Modelos Disponibles:")
    
    modelos = list(genai.list_models())
    encontrado = False
    
    if not modelos:
        st.error("❌ Tu clave funciona, pero NO ve ningún modelo. ¡Necesitas una clave nueva!")
    else:
        for m in modelos:
            st.code(m.name) # Muestra el nombre técnico
            if "gemini-1.5-flash" in m.name:
                encontrado = True
        
        if encontrado:
            st.success("✅ ¡Tu clave SÍ ve el modelo 'gemini-1.5-flash'! El error anterior era raro.")
        else:
            st.warning("⚠️ Tu clave funciona, pero NO tiene permiso para usar Flash o Pro. Necesitas crear una clave en un proyecto nuevo.")

except Exception as e:
    st.error(f"Error grave de conexión: {e}")
