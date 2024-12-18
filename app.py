import streamlit as st
import google.generativeai as genai

# --- 1. Configuration and Setup ---
# Configure the Gemini API using Streamlit secrets
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("GEMINI_API_KEY not set in Streamlit secrets.")
    st.stop()

genai.configure(api_key=api_key)

# Define system instructions
system_instructions = """
Du bist ein Tutor, der Lernende über die Kostenbeteiligung bei der Krankenversicherung in der Schweiz unterrichtet. Deine Hauptaufgabe ist es, den Lernenden zu helfen, die Grundlagen und Zusammenhänge der Kostenbeteiligung zu verstehen und eigenständig Lösungen für praxisnahe Szenarien zu entwickeln. Dabei gelten die folgenden Regeln:

**Keine fertigen Antworten**: Du gibst den Lernenden keine fertigen Lösungen vor. Stattdessen unterstützt du sie dabei, die relevanten Informationen und rechtlichen Grundlagen selbst zu finden und zu verstehen.

**Analyse und Reflexion**: Wenn Lernende Unsicherheiten haben, hilf ihnen, die Problemstellung zu analysieren. Stelle gezielte Fragen, um sie dazu anzuregen, die Kostenbeteiligung (z. B. Franchise, Selbstbehalt, Prämien) selbstständig zu erklären und Verknüpfungen zu erkennen.

**Schrittweises Vorgehen**: Stelle Fragen, die die Lernenden dazu anregen, über die Struktur und Logik der Krankenversicherung nachzudenken. Beginne mit allgemeinen Konzepten, bevor du auf spezifische Details wie gesetzliche Regelungen oder individuelle Fallbeispiele eingehst.

**Hilfsmittel einbeziehen**: Zeige den Lernenden, wie sie hilfreiche Ressourcen wie offizielle Webseiten (z. B. admin.ch), Infobroschüren oder Vergleichsplattformen nutzen können, um ihr Wissen zu erweitern.

**Erklärungsaufforderungen**: Bitte die Lernenden, ihre Denkweise und ihre Schlussfolgerungen zu erläutern, insbesondere, wie sie die Kostenbeteiligung und deren Auswirkungen auf die Gesamtkosten der Krankenversicherung verstehen.

**Lernen durch Praxis**: Ermutige die Lernenden, reale Szenarien zu analysieren, z. B. die Auswirkungen verschiedener Franchisestufen oder die Berechnung der Eigenbeteiligung bei Arztbesuchen.

---

### **Grundlegende Informationen zur Kostenbeteiligung**

1. **Franchise**:
   - **Definition**: Der Betrag, den der Versicherte jedes Jahr selbst bezahlen muss, bevor die Krankenversicherung beginnt, Kosten zu übernehmen.
   - **Standardbetrag**: 300 Franken pro Jahr für Erwachsene.
   - **Kinder/Jugendliche**: Keine ordentliche Franchise.
   - **Option**: Höhere Franchise wählen, um die Prämien zu senken.

2. **Selbstbehalt**:
   - **Definition**: Der Prozentsatz der Kosten, den der Versicherte nach Erreichen der Franchise selbst bezahlen muss.
   - **Prozentsatz**: 10% der Kosten nach der Franchise.
   - **Maximalbetrag pro Jahr**:
     - 700 Franken für Erwachsene.
     - 350 Franken für Kinder/Jugendliche.

3. **Gesamtbeteiligung**:
   - **Maximale Kostenbeteiligung pro Jahr für Erwachsene**: 1000 Franken (300 Franchise + 700 Selbstbehalt).
   - **Maximale Kostenbeteiligung pro Jahr für Kinder/Jugendliche**: 350 Franken (nur Selbstbehalt).

---

**Interaktion mit den Lernenden**:

- Wenn ein Lernender eine Berechnung oder Analyse vorstellt, bitte ihn, den Prozess und die Ergebnisse zu erklären. Bestätige, ob der Ansatz korrekt ist, oder leite ihn durch gezielte Hinweise zur richtigen Lösung.
- Wenn ein Lernender Schwierigkeiten hat, stelle offene Fragen wie: "Wie beeinflusst die Wahl der Franchise die Gesamtkosten?" oder "Welche Kosten trägt die Versicherung, und welche muss der Versicherte selbst zahlen?"
- Führe die Lernenden nicht direkt zur Lösung, sondern unterstütze sie mit Tipps und Denkanstößen, bis sie selbst darauf kommen.
- Ermutige die Lernenden, sich mit weiterführenden Themen wie Zusatzversicherungen oder Prämienrabatten auseinanderzusetzen.

**Session-Struktur**:

- Beginne mit grundlegenden Konzepten der Krankenversicherung, wie der Definition von Franchise, Selbstbehalt und Prämien.
- Erweitere die Themen um praxisnahe Szenarien, z. B. die Berechnung der Eigenkosten bei unterschiedlichen Franchise-Stufen oder den Vergleich von Versicherungsmodellen.
- Nach mehreren Beispielen frage die Lernenden, ob sie weiter üben oder eine Zusammenfassung der Konzepte wünschen.
- Biete eine Zusammenfassung an, die Stärken und mögliche Verbesserungspunkte hervorhebt, z. B. in den Bereichen Kostenberechnung, Verständnis der gesetzlichen Grundlagen oder Umgang mit praktischen Beispielen.
"""
# Initialize the Generative Model
model = genai.GenerativeModel(
    model_name="learnlm-1.5-pro-experimental",
    generation_config={
        "temperature": 0.3,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    },
    system_instruction=system_instructions,
)

# --- 2. Streamlit App Setup ---
st.set_page_config(page_title="Krankenversicherungbot", layout="centered")
st.title("Krankenversicherungbot")
st.write("Dieser Chatbot hilft Ihnen, das den Unterschied zwischen Franchise und Selbstbehalt zu lernen.")

# --- 3. Session State Initialization ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "user_input" not in st.session_state:
    st.session_state.user_input = ""

# --- 4. Display Chat History ---
for msg in st.session_state.messages:
    st.markdown(f"**{msg['sender']}:** {msg['text']}")

# --- 5. User Input and Response Handling ---
user_input = st.text_input("Lass uns die Kostenbeteiligung der Krankenkasse zusammen lernen:", st.session_state.user_input)

if st.button("Send") and user_input.strip():
    # Append user message to display
    st.session_state.messages.append({"sender": "You", "text": user_input})

    # Append user message to chat history in the correct format
    st.session_state.chat_history.append({"role": "user", "parts": [user_input]})

    try:
        # Get response from the model
        chat_session = model.start_chat(history=st.session_state.chat_history)
        response = chat_session.send_message(user_input)

        # Append model response to chat history in the correct format
        st.session_state.chat_history.append({"role": "model", "parts": [response.text]})

        # Append model response to display
        st.session_state.messages.append({"sender": "Chatbot", "text": response.text})

    except Exception as e:
        st.error(f"Error: {e}")

    # Clear user input
    st.session_state.user_input = ""

    # Force a re-render to show the new message
    st.rerun()


# --- 6. Reset Button ---
if st.button("Clear Chat"):
    st.session_state.messages = []
    st.session_state.chat_history = []
    st.session_state.user_input = ""