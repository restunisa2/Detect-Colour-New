import streamlit as st
import numpy as np
import cv2
import base64
from PIL import Image
from io import BytesIO

# Judul aplikasi
st.title("Program Pengenalan Warna")

# Fungsi untuk mendeteksi warna
def detect_color(hue, saturation, value):
    if saturation < 3:
        return "PUTIH"
    elif value < 50:
        return "HITAM"
    elif 3 < saturation < 40:
        return "ABU-ABU"
    elif hue < 5:
        return "MERAH"
    elif hue < 20:
        return "ORANGE"
    elif hue < 30:
        return "KUNING"
    elif hue < 70:
        return "HIJAU"
    elif hue < 125:
        return "BIRU"
    elif hue < 145:
        return "UNGU"
    elif hue < 170:
        return "PINK"
    else:
        return "MERAH"

# Fungsi untuk memproses gambar
def process_image(image_data):
    # Decode base64 image
    image_data = image_data.split(",")[1]
    image = Image.open(BytesIO(base64.b64decode(image_data)))
    frame = np.array(image)

    # Konversi frame dari RGB ke HSV
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
    height, width, _ = frame.shape

    # Koordinat tengah frame
    cx = int(width / 2)
    cy = int(height / 2)

    # Mengambil nilai warna piksel di tengah frame
    pixel_center = hsv_frame[cy, cx]
    hue = pixel_center[0]
    saturation = pixel_center[1]
    value = pixel_center[2]

    # Deteksi warna
    color = detect_color(hue, saturation, value)

    # Tambahkan teks warna ke gambar
    cv2.putText(frame, color, (cx - 100, cy - 150), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 8)

    return frame

# Mengambil parameter kueri dari URL
query_params = st.query_params()

# Memeriksa apakah parameter "action" adalah "process_image"
if query_params.get("action") == ["process_image"]:
    image_data = query_params.get("image", [None])[0]  # Ambil gambar dari query params, default ke None

    if image_data is not None:
        processed_image = process_image(image_data)  # Proses gambar
        st.image(processed_image, caption="Hasil Deteksi Warna", use_column_width=True)  # Tampilkan gambar yang sudah diproses
    else:
        st.error("Tidak ada data gambar yang ditemukan.")
else:
    st.warning("Silakan kirim gambar dengan parameter 'action=process_image' dalam URL.")

