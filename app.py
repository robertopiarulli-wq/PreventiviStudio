import streamlit as st
import pdfplumber
import pandas as pd
import io

st.title("🧪 Test PDF - Preventivo")

uploaded = st.file_uploader("Carica PDF test", type="pdf")

if uploaded is not None:
    # LEGGI DIRETTAMENTE DALL'OGGETTO UPLOADATO (no file temporaneo!)
    with pdfplumber.open(uploaded) as pdf:  # <-- CAMBIO QUI
        lines = []
        for i, page in enumerate(pdf.pages):
            page_lines = page.extract_text_lines()
            for line in page_lines:
                text = line.get('text', '').strip()
                if text and len(text) > 5:
                    lines.append({'page': i+1, 'riga': text[:200]})
    
    df = pd.DataFrame(lines)
    st.success(f"✅ Trovate {len(df)} righe!")
    st.dataframe(df.head(20))
    st.download_button("💾 Scarica CSV righe", df.to_csv(index=False), "righe.csv")
