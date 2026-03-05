import streamlit as st
import pdfplumber
import pandas as pd
import tempfile

st.title("🧪 Test PDF - Preventivo")

uploaded = st.file_uploader("Carica PDF test", type="pdf")
if uploaded:
    with tempfile.NamedTemporaryFile(suffix=".pdf") as tmp:
        tmp.write(uploaded.read())
        tmp_path = tmp.name
    
    lines = []
    with pdfplumber.open(tmp_path) as pdf:
        for i, page in enumerate(pdf.pages):
            page_lines = page.extract_text_lines()
            for line in page_lines:
                text = line.get('text', '').strip()
                if text and len(text)>5:  # Filtra vuoti
                    lines.append({'page': i+1, 'riga': text})
    
    df = pd.DataFrame(lines)
    st.dataframe(df.head(20))
    st.write(f"Trovate {len(df)} righe!")
