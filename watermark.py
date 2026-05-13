from PIL import Image, ImageDraw
import numpy as np
import qrcode
from datetime import datetime
import os

def embed_watermark(action, user_id):
    text_log = f"ACCES - {action} - ID:{user_id} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    img = Image.new('RGB', (650, 220), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    draw.text((30, 40), text_log, fill=(0, 0, 0))

    # Tatouage invisible LSB
    watermark_text = "PROJET1-2026-HamdiChebbi-TATOUAGE"
    binary_wm = ''.join(format(ord(c), '08b') for c in watermark_text)

    pixels = np.array(img).astype(np.int16)
    idx = 0
    for i in range(pixels.shape[0]):
        for j in range(pixels.shape[1]):
            for k in range(3):
                if idx < len(binary_wm):
                    pixels[i, j, k] = (pixels[i, j, k] & ~1) | int(binary_wm[idx])
                    idx += 1

    watermarked_img = Image.fromarray(pixels.astype(np.uint8))

    # QR Code visible
    qr = qrcode.QRCode(version=1, box_size=5, border=2)
    qr.add_data(watermark_text)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="#1e40af", back_color="white").resize((130, 130))
    watermarked_img.paste(qr_img, (480, 50))

    os.makedirs("../logs", exist_ok=True)
    filename = f"../logs/log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    watermarked_img.save(filename)

    print(f"✅ Log tatoué + QR Code créé : {filename}")
    return filename

def extract_watermark(image_path):
    try:
        img = np.array(Image.open(image_path))
        binary = ""
        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                for k in range(3):
                    binary += str(img[i, j, k] & 1)
                    if len(binary) >= 8 * len("PROJET1-2026-HamdiChebbi-TATOUAGE"):
                        break
        extracted = "".join(chr(int(binary[i:i+8], 2)) for i in range(0, len(binary), 8))
        wm = extracted[:len("PROJET1-2026-HamdiChebbi-TATOUAGE")]

        if wm == "PROJET1-2026-HamdiChebbi-TATOUAGE":
            print("✅ Tatouage + QR Code intact")
            return True
        else:
            print("❌ Tatouage modifié")
            return False
    except:
        return False