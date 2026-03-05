import streamlit as st
import pdfplumber
import pandas as pd

st.title("📊 Estrattore Tabelle PDF - Fix")

uploaded = st.file_uploader("Carica PDF", type="pdf")

if uploaded is not None:
    with pdfplumber.open(uploaded) as pdf:
        st.subheader("📋 Tabelle trovate")
        
        for i, page in enumerate(pdf.pages):
            tables = page.extract_tables()
            st.write(f"**Pagina {i+1}**: {len(tables or [])} tabelle")
            
            for table_idx, table in enumerate(tables or []):
                if table and len(table) > 1:
                    # NON concat - crea DF per ogni tabella
                    df_table = pd.DataFrame(table[1:], columns=table[0])
                    df_table['Pagina'] = i+1
                    df_table['Tabella'] = table_idx+1
                    
                    st.write(f"Tabella {table_idx+1} (righe: {len(df_table)})")
                    st.dataframe(df_table, use_container_width=True, hide_index=True)
                    st.markdown("---")
        
        st.success("✅ Fatto! Ogni tabella mostrata separatamente.")
