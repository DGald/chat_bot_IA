# Desarrollado por: Danilo Galdámez
# Proyecto: Chatbot de Soporte Técnico con NLP Multilingüe

import streamlit as st
from difflib import get_close_matches
from deep_translator import GoogleTranslator

st.set_page_config(page_title="IA Support Chat")

# Base de conocimiento (Claves en minúsculas para mejor coincidencia)
conocimiento = {
    "contraseña": "Por seguridad, debes dirigirte físicamente a Soporte Técnico para un reset presencial.",
    "vpn": "Recuerda: La clave de VPN es la misma de tu equipo. Tu usuario ahora es Inicial + Cargo (Ej: DPROGRAMADOR).",
    "oc no carga": "Limpia el caché de tu navegador: Configuración -> Historial -> Borrar Cookies y Caché.",
    "abastecimiento": "Si falla, intenta ejecutar como Admin y usa las credenciales de la cuenta 'Administrator'.",
    "active directory": "Para resetear en AD, activa siempre la opción 'El usuario debe cambiar la contraseña en el siguiente inicio'."
}

st.title("🤖 Asistente de Soporte con IA")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("¿En qué puedo ayudarte? / How can I help you?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # --- PASO 1: TRADUCIR SIEMPRE A ESPAÑOL PRIMERO ---
        # Esto convierte "I have VPN issues" en "Tengo problemas con la VPN"
        translator = GoogleTranslator(source='auto', target='es')
        prompt_es = translator.translate(prompt).lower()
        
        # --- PASO 2: BUSCAR PALABRAS CLAVE EN EL TEXTO TRADUCIDO ---
        respuesta_encontrada = None
        for clave in conocimiento.keys():
            if clave in prompt_es: # Si la palabra 'vpn' o 'contraseña' está en la frase traducida
                respuesta_encontrada = conocimiento[clave]
                break
        
        # Si no hay coincidencia exacta, usamos el buscador de parecidos por si acaso
        if not respuesta_encontrada:
            coincidencias = get_close_matches(prompt_es, list(conocimiento.keys()), n=1, cutoff=0.4)
            if coincidencias:
                respuesta_encontrada = conocimiento[coincidencias[0]]

        # --- PASO 3: TRADUCIR LA RESPUESTA DE VUELTA SI ES NECESARIO ---
        if respuesta_encontrada:
            # Si el prompt original no estaba en español, traducimos la respuesta al inglés
            if prompt_es != prompt.lower():
                respuesta = GoogleTranslator(source='es', target='en').translate(respuesta_encontrada)
            else:
                respuesta = respuesta_encontrada
        else:
            respuesta = "Lo siento, no reconozco ese problema. / I'm sorry, I don't recognize that issue."

    except Exception:
        respuesta = "Error de conexión. Prueba en español."

    with st.chat_message("assistant"):
        st.markdown(respuesta)

    st.session_state.messages.append({"role": "assistant", "content": respuesta})
