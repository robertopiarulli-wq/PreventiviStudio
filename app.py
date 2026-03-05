import streamlit as st
import pdfplumber

st.title("📊 PDF Completo - No Error")

uploaded = st.file_uploader("Carica PDF", type="pdf")

if uploaded is not None:
    with pdfplumber.open(uploaded) as pdf:
        for i, page in enumerate(pdf.pages):
            st.markdown(f"---\n**📄 Pagina {i+1}**")
            
            # === TESTO RIGHE ===
            page_text = page.extract_text()
            if page_text:
                lines = [line.strip() for line in page_text.split('\n') if line.strip()]
                st.write(f"📝 **{len(lines)} righe testo**")
                for j, line in enumerate(lines[:10]):  # Prime 10
                    st.write(f"**Riga {j+1}:** {line[:150]}")
                if len(lines) > 10:
                    st.write("... e altre")
            
            # === TABELLE (senza pandas) ===
            tables = page.extract_tables()
            if tables:
                st.write(f"📊 **{len(tables)} tabelle**")
                for t_idx, table in enumerate(tables):
                    st.write(f"**Tabella {t_idx+1}:**")
                    for row_idx, row in enumerate(table[:5]):  # Prime 5 righe
                        st.write(f"  Riga {row_idx+1}: {row}")
                    st.write("")
            
            # === IMMAGINI ===
            imgs = page.images
            if imgs:
                st.write(f"🖼️ **{len(imgs)} immagini**")
                for img_idx, img in enumerate(imgs):
                    st.write(f"  Immagine {img_idx+1}: {img['size']}")
