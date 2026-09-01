import os
import streamlit as st
from google import genai

# 1. Konfiguration & Branding
st.set_page_config(
    page_title="Resonanz-Kompass | Lars Ziörjen",
    page_icon="🧭",
    layout="centered"
)

st.markdown("""
    <style>
    .main { background-color: #fcfbf9; }
    
    /* Haupt-Button */
    .stButton>button { 
        width: 100%; 
        border-radius: 6px; 
        height: 3.4em; 
        background-color: #2b3e50; 
        color: #ffffff;
        font-weight: 600;
        font-size: 1.05rem;
        border: none;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #1a252f;
        color: #ffffff;
    }

    /* Antwortkarte */
    .response-card {
        padding: 2rem;
        background-color: #ffffff;
        border-left: 5px solid #2b3e50;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        border-radius: 8px;
        margin-top: 1.8rem;
        margin-bottom: 2rem;
        line-height: 1.75;
        color: #2c3e50;
    }

    /* Action Box für Follow-ups */
    .action-box {
        background-color: #f4f6f8;
        padding: 1.5rem;
        border-radius: 8px;
        border: 1px solid #e0e0e0;
        margin-top: 1.5rem;
    }

    /* Footer */
    .footer {
        margin-top: 3.5rem;
        padding-top: 1.5rem;
        border-top: 1px solid #e0e0e0;
        text-align: center;
        font-size: 0.9rem;
        color: #666;
    }
    .footer a {
        color: #2b3e50;
        text-decoration: none;
        font-weight: bold;
    }
    
    /* Calendly-Link-Button */
    .btn-calendly {
        display: inline-block;
        width: 100%;
        text-align: center;
        background-color: #2b3e50;
        color: white !important;
        padding: 0.8rem 0;
        border-radius: 6px;
        font-weight: 600;
        text-decoration: none;
        margin-top: 0.5rem;
    }
    .btn-calendly:hover {
        background-color: #1a252f;
    }
    </style>
""", unsafe_allow_html=True)

# Logo-Einbindung
if os.path.exists("berufungsfinder-Logo.png"):
    st.image("berufungsfinder-Logo.png", width=220)

st.title("🧭 Der Resonanz-Kompass")
st.caption("Ein Moment der Standortbestimmung – spürbar, geerdet und integral.")

# 2. API-Schlüssel
MY_API_KEY = "os.getenv("GEMINI_API_KEY")"

st.write("---")

# 3. Eingabemaske
st.subheader("1. Das äußere Feld")
topic = st.selectbox(
    "Was fordert dich im Außen gerade am meisten heraus?",
    [
        "Hohes Arbeitspensum, Verdichtung & gefühlter Kontrollverlust",
        "KI-Wandel, Methodendruck & eigener Trainingsrückstand",
        "Schulabsentismus & emotionale Überforderung bei Schüler:innen",
        "Dauerhafte Unruhe, Grenzüberschreitungen & Disziplin im Klassenzimmer",
        "Festgefahrene Fronten, Schnittstellenkonflikte oder Stille im Kollegium",
        "Anspruchsvolle Elterngespräche, Rechtfertigungsdruck & Reibung",
        "Erwartungsdruck, Rollenkonflikte & Vorgaben durch Schulleitung/Behörden"
    ]
)

st.subheader("2. Das innere Erleben")
inner_state = st.radio(
    "Welches Muster zeigt sich in deiner inneren Haltung?",
    [
        "Aktionismus: Hoher Druck & der Impuls, sofort im Außen reparieren zu müssen",
        "Selbstzweifel: Unsicherheit, Kompetenzangst oder Überforderung",
        "Erschöpfung: Funktionieren auf Reserve, innere Distanz oder Taubheit",
        "Ohnmacht: Das Gefühl, den Gegebenheiten ausgeliefert zu sein"
    ]
)

st.subheader("3. Deine Ausrichtung")
resource_focus = st.select_slider(
    "Was braucht deine Berufung genau jetzt?",
    options=[
        "Innere Klarheit & Abgrenzung",
        "Entlastung & Selbstmitgefühl",
        "Souveräne Handlungsfähigkeit im Außen"
    ]
)

optional_note = st.text_input(
    "Konkreter Kontext / Zusatzgedanke (optional):", 
    placeholder="z.B. Morgen schwieriges Gespräch um 10 Uhr; Gefühl, nie fertig zu werden..."
)

# 4. System-Prompt
SYSTEM_PROMPT = """
Du agierst als der Resonanz-Kompass für berufungsfinder.ch. Dein Fundament ist das Integralcoaching und die tiefere Psychologie des menschlichen Wirkens. Du begegnest dem Gegenüber nicht als unfehlbarer Ratgeber, sondern als geerdeter, feinfühliger Impulsgeber, der Pragmatismus und geistige Weite verbindet.

DEINE HALTUNG & SPRACHE:
- Eloquent, fein, tief und menschlich – frei von akademischer Arroganz oder künstlichem Jargon.
- Verfalle NIEMALS in Standard-KI-Singsang oder Plattitüden ("Alles wird gut", "Es ist völlig verständlich").
- Vermeide plumpe Anweisungen. Arbeite stattdessen mit echter Resonanz, die das Ungesagte benennt und Raum schafft.
- DIE ATEMPUSIARUNG (DEINE SIGNATUR): Als "Schnüüfeler" weißt du um die biologische und psychologische Macht der Atempause zur Selbstregulation. Integriere diesen Atem-Impuls ganz natürlich, nahbar und unaufdringlich – z. B. mit Wendungen wie "...und vor allem: Schnüüfele nicht vergessen" oder einem kurzen Innehalten zum Durchschnaufen.
- Nutze eine wohlwollende Du-Form auf Augenhöhe.

DEINE DREITEILIGE ANTWORTSTRUKTUR (Verwende exakt diese fetten Zeilen):

**Spiegelung & Resonanz**
(2-3 Sätze) Verbinde das äußere Feld, das innere Muster und den Kontext zu einer präzisen Beobachtung. Benenne das Spannungsfeld ohne Beschönigung oder Bewertung.

**Die Klärungsfrage**
(Genau 1 tiefgründige Frage) Eine Frage, die nicht nach schnellen Antworten verlangt, sondern den Fokus vom reinen Funktionieren zurück auf das eigene Bewusstsein lenkt.

**Impuls für Innen & Außen**
Verankere die Wirkung auf zwei Ebenen (orientiert an der gewählten Ausrichtung):
- *Innen (Haltung):* Eine feine Verschiebung der inneren Perspektive – gerne kombiniert mit der Einladung zum echten "Schnüüfele" als Anker für das Nervensystem.
- *Außen (Handlung):* Eine winzige, klare und konkrete Micro-Handlung für das reale Feld.
"""

# 5. Ausführung & Follow-up Logik
st.write("")
if st.button("Kompass ausrichten"):
    if not MY_API_KEY:
        st.error("Bitte hinterlege den GEMINI_API_KEY in den Streamlit Cloud Secrets.")
    else:
        with st.spinner("Verbinde Innen und Außen..."):
            try:
                client = genai.Client(api_key=MY_API_KEY)
                
                user_context = f"""
                SITUATION DES USERS:
                - Äußeres Feld: {topic}
                - Inneres Muster: {inner_state}
                - Gewünschte Ausrichtung: {resource_focus}
                - Zusatzgedanke / Kontext: {optional_note if optional_note else 'Keine weiteren Angaben'}
                """
                
                full_prompt = f"{SYSTEM_PROMPT}\n\n{user_context}"
                
                response = client.models.generate_content(
                    model='gemini-3.6-flash',
                    contents=full_prompt,
                )
                
                # Antwort anzeigen & in Session speichern
                st.session_state['result'] = response.text
            except Exception as e:
                st.error(f"Fehler bei der Verbindung: {e}")

# Wenn ein Ergebnis vorliegt, anzeigen und Follow-up-Optionen bieten
if 'result' in st.session_state:
    st.markdown(f'<div class="response-card">{st.session_state["result"]}</div>', unsafe_allow_html=True)
    
    st.write("---")
    st.subheader("Wie möchtest du diesen Impuls vertiefen?")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**📄 PDF & persönlicher Kommentar**")
        st.caption("Erhalte diese Standortbestimmung inkl. einer persönlichen Einordnung von Lars als PDF.")
        user_email = st.text_input("Deine E-Mail-Adresse:", key="pdf_email", placeholder="name@beispiel.ch")
        if st.button("PDF anfordern"):
            if user_email:
                st.success(f"Vielen Dank! Die Zusammenfassung wird an {user_email} gesendet.")
            else:
                st.warning("Bitte gib deine E-Mail-Adresse ein.")
                
    with col2:
        st.markdown("**🤝 Persönliches Orientierungsgespräch**")
        st.caption("Lass uns deine Situation in einem ruhigen 1:1-Gespräch vertiefen.")
        # Hier deinen echten Calendly-Link einsetzen
        calendly_url = "https://calendly.com" 
        st.markdown(f'<a href="{calendly_url}" target="_blank" class="btn-calendly">📅 Termin direkt buchen</a>', unsafe_allow_html=True)

# 6. Footer
st.markdown("""
    <div class="footer">
        Ein Projekt von <strong>Lars Ziörjen</strong> | Integralcoach & Mentor<br>
        <a href="https://berufungsfinder.ch" target="_blank">berufungsfinder.ch</a> · 
        <a href="mailto:info@berufungsfinder.ch">info@berufungsfinder.ch</a>
    </div>
""", unsafe_allow_html=True)