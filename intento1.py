import streamlit as st
from PIL import Image
import qrcode
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from io import BytesIO

# Función para generar el QR
def generar_qr(link):
    qr = qrcode.make(link)
    buf = BytesIO()
    qr.save(buf)
    buf.seek(0)
    return buf

# Función para generar el PDF
def generar_pdf(nombre_empresa, buf_qr, afiche_image):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    
    # Dibuja el afiche de fondo, asumiendo que afiche_image es un PIL Image
    afiche_image_reader = ImageReader(afiche_image)
    c.drawImage(afiche_image_reader, 0, 0, width=612, height=792)
    
    # Coloca el QR en el centro
    qr_image = ImageReader(buf_qr)
    qr_size = 150
    c.drawImage(qr_image, (612 - qr_size) / 2, (792 - qr_size) / 2, width=qr_size, height=qr_size)

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer

st.title("Bienvenido/a al Programa de Finanzas Personales")

st.write("""
Como parte de la colaboración entre ACHS y la Universidad de Chile, estamos entusiasmados de presentarte este exclusivo Programa de Finanzas Personales. Este programa no solo busca enriquecer tu conocimiento financiero, sino también facilitar herramientas para mejorar el bienestar económico de toda tu comunidad laboral.

**Tu rol es clave.** Como encargado/a de la difusión de este programa, te invitamos a ser el puente que lleve esta oportunidad única a tus compañeros/as, ayudándoles a tomar control de su bienestar financiero y, por ende, de su calidad de vida.

Por favor, introduce el nombre de tu empresa en el campo siguiente. Tras hacerlo, podrás descargar un afiche personalizado para promover el programa entre tus compañeros/as, junto con un enlace para que puedan inscribirse y participar activamente.

¡Juntos, podemos hacer una diferencia significativa en nuestra comunidad!
""")

nombre_empresa = st.selectbox("Introduce el nombre de tu empresa:", ["", "Coca Cola", "Empresa A", "Empresa B", "Empresa C", "Universidad de Chile"])

if st.button("Generar Afiche con QR"):
    link = f"https://www.ejemplo.com/{nombre_empresa.replace(' ', '-').lower()}"
    buf_qr = generar_qr(link)
    
    afiche_path = "path_to_your_poster_image.webp"  # No olvides actualizar esto con la ruta correcta
    try:
        afiche_image = Image.open(afiche_path)
        pdf = generar_pdf(nombre_empresa, buf_qr, afiche_image)
        
        st.download_button(label="Descargar Afiche en PDF",
                           data=pdf,
                           file_name=f"afiche_{nombre_empresa.replace(' ', '_').lower()}.pdf",
                           mime="application/pdf")
        # Muestra el enlace para que los usuarios puedan copiarlo
        st.text_input("Copia este enlace para compartir:", link, help="Puedes copiar este enlace y compartirlo con tus compañeros/as.")
        
    except FileNotFoundError:
        st.error(f"El archivo no fue encontrado en {afiche_path}")
    except Exception as e:
        st.error(f"Error al abrir la imagen: {e}")
