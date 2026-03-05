import streamlit as st
import pdfplumber
import pandas as pd
import io

st.title("🧪 Test PDF - Preventivo")

uploaded = st.file_uploader("Carica PDF test", type="pdf")

if uploaded is not None:
    with pdfplumber.open(uploaded) as pdf:
        lines = []
        for i, page in enumerate(pdf.pages):
            # Prova prima extract_text() poi extract_text_lines()
            page_text = page.extract_text()
            if page_text:
                # Splitta per righe manualmente
                for j, line in enumerate(page_text.split('\n')):
                    text = line.strip()
                    if text and len(text) > 5:
                        lines.append({
                            'Pagina': i+1,
                            'Riga': j+1,
                            'Testo': text[:150],  # Max 150 char
                            'Lunghezza': len(text)
                        })
            
            # Fallback: extract_text_lines()
            page_lines = page.extract_text_lines()
            for line in page_lines:
                text = line.get('text', '').strip()
                if text and len(text) > 5 and text not in [l['Testo'] for l in lines[-10:]]:
                    lines.append({
                        'Pagina': i+1,
                        'Riga': len(lines)+1,
                        'Testo': text[:150],
                        'Lunghezza': len(text)
                    })
    
    if lines:
        df = pd.DataFrame(lines)
        st.success(f"✅ Trovate {len(df)} righe!")
        
        # Mostra TUTTE le colonne, larga, senza index
        st.dataframe(
            df, 
            use_container_width=True,
            hide_index=True,
            column_config={
                "Testo": st.column_config.TextColumn("📄 Testo riga", width="large"),
                "Pagina": st.column_config.NumberColumn("📄 Pagina"),
                "Riga": st.column_config.NumberColumn("🔢 Riga"),
                "Lunghezza": st.column_config.NumberColumn("📏 Char")
            }
        )
        
        st.download_button("💾 Scarica CSV", df.to_csv(index=False), "righe.pdf.csv")
    else:
        st.warning("❌ Nessuna riga trovata. Prova un PDF con testo selezionabile.")
