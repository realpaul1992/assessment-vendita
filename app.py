import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

#########################
# Funzione grafico GENERALE (design preso dal tuo codice preferito)
#########################
def crea_grafico_generale(punteggi, aree, file_nome):
    # Calcoliamo le percentuali
    df = pd.DataFrame({
        'Area': aree,
        'Punteggio': punteggi
    })
    df['Percentuale'] = (df['Punteggio'] / 20) * 100  # 20 è il punteggio massimo

    labels = df['Area'].values
    stats = df['Percentuale'].values
    num_vars = len(labels)

    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    stats = np.concatenate((stats, [stats[0]]))
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(12, 12), subplot_kw=dict(polar=True))
    ax.fill(angles, stats, color='blue', alpha=0.25)
    ax.plot(angles, stats, color='blue', linewidth=2)

    # Linea tratteggiata per punteggio ottimale (85% = 17/20)
    valore_ottimale = 85  
    ottimale_stats = [valore_ottimale] * (num_vars + 1)
    ax.plot(angles, ottimale_stats, color='orange', linestyle='dashed', linewidth=2)

    for angle in angles[:-1]:
        ax.plot([angle, angle], [0, 100], color='black', linewidth=1, linestyle='solid')

    ax.set_ylim(0, 100) 

    # Etichette percentuali
    for stat, angle in zip(stats, angles):
        ax.text(angle, stat + 5, f'{stat:.1f}%', size=10, horizontalalignment='center', verticalalignment='bottom')

    # Etichette delle aree
    for label, angle in zip(labels, angles[:-1]):
        ax.text(angle, 110, label, size=12, horizontalalignment='center', verticalalignment='center')

    plt.title('Analisi Reparto Commerciale', fontsize=18, pad=80)

    import matplotlib.patches as mpatches
    orange_patch = mpatches.Patch(color='orange', label='Punteggio Ottimale')
    fig.legend(handles=[orange_patch], loc='upper center', bbox_to_anchor=(0.5, 0.97), fontsize=16, frameon=False)

    ax.set_xticklabels([])
    ax.set_thetagrids([])

    fig.savefig(file_nome, dpi=100)
    return fig

#########################
# Funzione grafico SINGOLA AREA (senza linea ottimale, senza legenda, senza etichette angolari)
#########################
def crea_grafico_singola_area(punteggi_domande, domande, file_nome, titolo_area=''):
    # Convertiamo i punteggi (1-4) in percentuale (4 = 100%)
    punteggi_percentuali = [(p / 4) * 100 for p in punteggi_domande]
    num_domande = len(domande)

    angles = np.linspace(0, 2 * np.pi, num_domande, endpoint=False).tolist()
    punteggi_percentuali += punteggi_percentuali[:1]  # completa il cerchio
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(14, 14), subplot_kw=dict(polar=True))
    fig.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)

    ax.fill(angles, punteggi_percentuali, color='blue', alpha=0.25)
    ax.plot(angles, punteggi_percentuali, color='blue', linewidth=2)

    # Linee radiali in nero
    for angle in angles[:-1]:
        ax.plot([angle, angle], [0, 100], color='black', linewidth=2, linestyle='solid')

    # Cerchi concentrici
    r_grids = [20, 40, 60, 80, 100]
    ax.set_ylim(0, 100)
    ax.set_rgrids(r_grids, labels=[''] * len(r_grids), angle=0)

    # Etichette percentuali sui cerchi (posizionate a 90°)
    for r_tick in r_grids:
        ax.text(np.radians(90), r_tick, f'{r_tick}%', size=12, horizontalalignment='center', verticalalignment='center')

    # Etichette percentuali delle domande
    for percentuale, angle in zip(punteggi_percentuali[:-1], angles[:-1]):
        ax.text(angle, percentuale + 10, f'{percentuale:.0f}%', size=12,
                horizontalalignment='center', verticalalignment='bottom')

    # Etichette delle domande
    # Le mettiamo più distanti (ad es. 130), ed usiamo wrap=True per andare a capo
    for domanda, angle in zip(domande, angles[:-1]):
        ax.text(angle, 130, domanda, size=12,
                horizontalalignment='center', verticalalignment='center', wrap=True)

    # Rimuoviamo le etichette degli angoli (45°, 135°, etc.)
    ax.set_xticklabels([])
    ax.set_thetagrids([])

    # Niente linea ottimale, niente legenda
    plt.title(titolo_area, fontsize=18, pad=40)

    fig.savefig(file_nome, dpi=100)
    return fig

#########################
# Dati e interfaccia Streamlit
#########################

aree = [
    "Strategie e \ntattiche di vendita",
    "Processi di vendita",
    "Script e protocolli \ndi vendita",
    "Tecnologia e CRM",
    "Formazione e sviluppo venditori"
]

domande_aree = {
    "Strategie e \ntattiche di vendita": [
        "Hai una strategia chiara per raggiungere i tuoi obiettivi di vendita?",
        "Utilizzi protocolli di upselling e cross-selling efficaci?",
        "Adatti le tue strategie di vendita in base alle analisi dei dati?",
        "Hai una strategia per gestire le obiezioni dei clienti?",
        "Implementi regolarmente nuove tecniche di vendita basate su trend di mercato?"
    ],
    "Processi di vendita": [
        "Hai un processo standardizzato per guidare i clienti attraverso il processo di acquisto?",
        "Monitori, analizzi e ottimizzi regolarmente le performance del tuo processo di vendita?",
        "Integri il feedback dei clienti nel tuo processo di vendita?",
        "Hai un metodo chiaro per qualificare i lead?",
        "Utilizzi tecniche di closing efficaci?"
    ],
    "Script e protocolli \ndi vendita": [
        "Hai script di vendita per ogni persona del team vendita?",
        "Formi il tuo team sull'uso efficace degli script di vendita?",
        "Aggiorni regolarmente gli script in base ai risultati?",
        "Gli script includono strategie per affrontare obiezioni comuni?",
        "Misuri l'efficacia degli script attraverso un cruscotto di monitoraggio?"
    ],
    "Tecnologia e CRM": [
        "Hai un CRM in azienda?",
        "Formi regolarmente il team sull'uso ottimale del CRM?",
        "Analizzi i dati del CRM per migliorare le strategie di vendita?",
        "Utilizzi un cruscotto di monitoraggio per misurare le performance aziendali?",
        "Usi il CRM per personalizzare l'approccio ai clienti?"
    ],
    "Formazione e sviluppo venditori": [
        "Fornisci formazione continua ai tuoi venditori?",
        "Valuti regolarmente le competenze e le prestazioni del tuo team?",
        "Utilizzi tecniche di coaching o mentoring per i venditori?",
        "Ogni consulente commerciale compie le attività richieste dall'azienda in modo efficace?",
        "C'è un tasso di conversione alto?"
    ]
}

st.title("Analisi Reparto Commerciale")

# Punteggi totali (0-20)
punteggio_strat_tatt = st.number_input("Punteggio per Strategie e tattiche di vendita (0-20)", min_value=0, max_value=20, value=16)
punteggio_processi = st.number_input("Punteggio per Processi di vendita (0-20)", min_value=0, max_value=20, value=16)
punteggio_script = st.number_input("Punteggio per Script e protocolli di vendita (0-20)", min_value=0, max_value=20, value=14)
punteggio_tech = st.number_input("Punteggio per Tecnologia (CRM) e strumenti di supporto (0-20)", min_value=0, max_value=20, value=16)
punteggio_formazione = st.number_input("Punteggio per Formazione e sviluppo venditori (0-20)", min_value=0, max_value=20, value=14)

st.subheader("Dettaglio Domande per Area (1=No, 2=Non lo so, 3=Ci sto provando, 4=Sì)")
punteggi_domande_aree = {}
for area in aree:
    st.write(f"**{area}**")
    domande = domande_aree[area]
    punteggi_area = []
    for d in domande:
        val = st.number_input(d, min_value=1, max_value=4, value=2, key=area+d)
        punteggi_area.append(val)
    punteggi_domande_aree[area] = punteggi_area

if st.button("Genera Grafici"):
    # Grafico generale
    punteggi_aggregati = [
        punteggio_strat_tatt,
        punteggio_processi,
        punteggio_script,
        punteggio_tech,
        punteggio_formazione
    ]
    fig_generale = crea_grafico_generale(punteggi_aggregati, aree, 'grafico_generale.png')
    st.pyplot(fig_generale)

    st.subheader("Grafici per singola area (senza linea ottimale e senza legenda)")
    for area in aree:
        fig_area = crea_grafico_singola_area(
            punteggi_domande_aree[area],
            domande_aree[area],
            f"grafico_{area}.png",
            titolo_area=area
        )
        st.pyplot(fig_area)
