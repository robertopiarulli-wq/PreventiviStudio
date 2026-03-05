import streamlit as st
import pdfplumber
import pandas as pd

st.title("📊 Estrattore Tabelle PDF")

uploaded = st.file_uploader("Carica PDF", type="pdf")

if uploaded is not None:
    with pdfplumber.open(uploaded) as pdf:
        all_tables = []
        
        for i, page in enumerate(pdf.pages):
            # === ESTRAI TABELLE (non testo libero) ===
            tables = page.extract_tables()
            
            for table_idx, table in enumerate(tables or []):
                if table and len(table) > 1:  # Salta tabelle vuote
                    df_table = pd.DataFrame(table[1:], columns=table[0])  # Prima riga = header
                    df_table['Pagina'] = i+1
                    df_table['Tabella'] = table_idx+1
                    all_tables.append(df_table)
            
            # Debug: mostra layout tabelle
            st.write(f"📄 Pg {i+1}: {len(tables or [])} tabelle trovate")
        
        if all_tables:
            # Unisci tutte le tabelle
            df_final = pd.concat(all_tables, ignore_index=True)
            
            st.success(f"✅ {len(df_final)} righe tabella estratte!")
            
            # MOSTRA 5 COLONNE + Pagina/Tabella
            st.dataframe(
                df_final,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "0": st.column_config.TextColumn("Colonna 1"),
                    "1": st.column_config.TextColumn("Colonna 2"),
                    "2": st.column_config.TextColumn("Colonna 3"),
                    "3": st.column_config.TextColumn("Colonna 4"),
                    "4": st.column_config.TextColumn("Colonna 5"),
                    "Pagina": st.column_config.NumberColumn("📄 Pg"),
                }
            )
            
            st.download_button("💾 CSV", df_final.to_csv(index=False), "tabelle.csv")
        else:
            st.warning("❌ Nessuna tabella trovata. Prova extract_text()...")
