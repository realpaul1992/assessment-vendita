import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import os
from docx import Document
from docx.shared import Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from io import BytesIO

# Mappatura dei valori per la scala 1-5
scala_risposte = {
    1: "Assente/Inesistente",
    2: "Molto poco strutturato",
    3: "Presente ma non ottimizzato",
    4: "Ben strutturato",
    5: "Eccellente/ottimizzato"
}

def selettore_valori_domanda(domanda, key):
    val = st.radio(domanda, options=[1,2,3,4,5], index=2, format_func=lambda x: scala_risposte[x], key=key)
    return val

aree = [
    "Visione e Strategia di Vendita",
    "Processi di Vendita",
    "Script e Protocolli di Vendita",
    "Tecnologia e CRM",
    "Formazione e Sviluppo del Team di Vendita",
    "Misurazione e KPI"
]

domande = {
    "Visione e Strategia di Vendita": {
        "principali": [
            "Esiste una visione chiara e condivisa degli obiettivi di vendita?",
            "I target di vendita sono coerenti con le risorse e comunicati al team?",
            "C'è una strategia di vendita chiara per raggiungere gli obiettivi?",
            "L’efficacia delle strategie viene monitorata regolarmente?",
            "Il management fornisce linee guida e supporto chiari?"
        ],
        "controllo": "Hai una documentazione scritta che descrive obiettivi e strategie?"
    },
    # Le altre aree rimangono uguali
}

st.title("Assessment Reparto Commerciale")
st.write("Compila le seguenti domande per ogni area, poi clicca su 'Genera Grafici' per visualizzare i risultati.")

nome_cliente = st.text_input("Nome del Cliente:", "Francesco Ramundo")
nome_azienda = st.text_input("Nome dell'Azienda:", "rarosrl.com")

punteggi_aree = {}
controlli_aree = {}

for area in aree:
    st.subheader(area)
    punteggi_principali = []
    for i, domanda_principale in enumerate(domande[area]["principali"]):
        val = selettore_valori_domanda(domanda_principale, key=area+str(i))
        punteggi_principali.append(val)

    domanda_controllo = domande[area]["controllo"]
    val_controllo = selettore_valori_domanda("(Controllo) " + domanda_controllo, key=area+"controllo")

    punteggi_aree[area] = punteggi_principali
    controlli_aree[area] = val_controllo

def crea_radar(labels, values, title, max_score=5):
    vals_perc = [(v/max_score)*100 for v in values]
    N = len(labels)
    angles = np.linspace(0, 2*np.pi, N, endpoint=False)
    vals_perc += vals_perc[:1]
    angles = np.concatenate((angles, [angles[0]]))

    fig, ax = plt.subplots(figsize=(12,12), subplot_kw=dict(polar=True))
    ax.set_theta_offset(np.pi/2 + 0.1)
    ax.set_theta_direction(-1)

    ax.fill(angles, vals_perc, color='blue', alpha=0.25)
    ax.plot(angles, vals_perc, color='blue', linewidth=2)

    ax.set_ylim(0,100)
    plt.title(title, fontsize=16, pad=80)
    return fig

if st.button("Genera Grafici"):
    medie_aree = {}
    for area in aree:
        media = np.mean(punteggi_aree[area])
        controllo = controlli_aree[area]
        if media >=4 and controllo <=2:
            media = max(1, media - 1)
            st.warning(f"L'area '{area}' aveva media {np.mean(punteggi_aree[area]):.2f}, ma a causa della bassa risposta di controllo ({controllo}), il punteggio è stato ridotto a {media:.2f}.")
        medie_aree[area] = media

    st.header("Risultati Generali")
    fig_generale = crea_radar(aree, [medie_aree[a] for a in aree], "Analisi Reparto Commerciale")
    st.pyplot(fig_generale)

    base_dir = "Programma Test vendita"
    cliente_dir = os.path.join(base_dir, nome_cliente)
    os.makedirs(cliente_dir, exist_ok=True)

    fig_generale.savefig(os.path.join(cliente_dir, "grafico_generale.png"), dpi=300, bbox_inches='tight')

    # Generazione del documento Word
    doc = Document()
    doc.add_heading('SALES ASSESSMENT', level=1)
    doc.add_paragraph(f"Report generato per {nome_cliente} - {nome_azienda}")
    doc.add_picture(os.path.join(cliente_dir, "grafico_generale.png"), width=Inches(6))

    doc_name = f"report_assessment_{nome_cliente}.docx"
    doc_path = os.path.join(cliente_dir, doc_name)
    doc.save(doc_path)

    # Pulsante di download
    with open(doc_path, "rb") as file:
        word_file = file.read()

    st.download_button(
        label="📥 Scarica il Report Word",
        data=word_file,
        file_name=doc_name,
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )

    st.success("Il report è stato generato con successo! Puoi scaricarlo usando il pulsante sopra.")
