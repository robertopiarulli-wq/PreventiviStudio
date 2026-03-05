import streamlit as st
import pdfplumber
import pandas as pd
import io
from PIL import Image

st.title("🧪 Test PDF Completo - Testo + Immagini")

uploaded = st.file_uploader("Carica PDF", type="pdf")

if uploaded is not None:
    images_data = []
    
    with pdfplumber.open(uploaded) as pdf:
        all_lines = []
        all_images = []
        
        for i, page in enumerate(pdf.pages):
            # === TESTO ===
            page_text = page.extract_text()
            if page_text:
                for j, line in enumerate(page_text.split('\n')):
                    text = line.strip()
                    if text and len(text) > 3:
                        all_lines.append({
                            'Pagina': i+1,
                            'Riga': j+1, 
                            'Testo': text[:100],
                            'Ha_Immagine': '❌'
                        })
            
            # === IMMAGINI ===
            for img_idx, img in enumerate(page.images):
                try:
                    img_bytes = img["stream"].get_data()
                    img_pil = Image.open(io.BytesIO(img_bytes))
                    
                    all_images.append({
                        'Pagina': i+1,
                        'Immagine': f'img_p{i+1}_{img_idx}',
                        'Testo': f'Immagine {img_idx+1} Pg.{i+1}',
                        'Ha_Immagine': '✅'
                    })
                    
                    # Salva in session per preview
                    st.session_state[f'img_p{i+1}_{img_idx}'] = img_pil
                    
                except:
                    pass
        
        # Combina testo + immagini
        df = pd.DataFrame(all_lines + all_images)
        
        st.success(f"✅ {len(all_lines)} righe testo + {len(all_images)} immagini!")
        
        # Tabella con 4 colonne chiare
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Testo": st.column_config.TextColumn("📄 Testo/Desc", width="large"),
                "Pagina": st.column_config.NumberColumn("📄 Pg"),
                "Riga": st.column_config.NumberColumn("🔢 Riga"),
                "Ha_Immagine": st.column_config.TextColumn("🖼️ Img")
            }
        )
        
        # Preview immagini
        if all_images:
            st.subheader("🖼️ Anteprime Immagini")
            for img_key in st.session_state:
                if img_key.startswith('img_p'):
                    st.image(st.session_state[img_key], caption=img_key, width=200)
