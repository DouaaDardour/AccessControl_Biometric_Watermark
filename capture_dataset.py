import cv2
import os
from datetime import datetime

def capture_for_person(person_name, num_photos=12):
    folder = f"dataset/{person_name}"
    os.makedirs(folder, exist_ok=True)
    
    # === ESSAI DE PLUSIEURS CAMÉRAS ===
    cap = None
    for index in [0, 1, 2]:
        cap = cv2.VideoCapture(index)
        if cap.isOpened():
            print(f"✅ Caméra trouvée sur l'index {index}")
            break
        cap.release()
    
    if not cap or not cap.isOpened():
        print("❌ Impossible d'ouvrir la webcam !")
        print("   → Vérifie que ta caméra n'est pas utilisée par Zoom/Teams")
        print("   → Essaie de redémarrer ton PC")
        return
    
    print(f"\n🎥 Capture pour {person_name}")
    print("   Appuie sur 'C' pour prendre une photo")
    print("   Appuie sur 'Q' pour terminer\n")
    
    count = 0
    while count < num_photos:
        ret, frame = cap.read()
        if not ret:
            print("Erreur lecture caméra")
            break
            
        cv2.imshow(f"Capture - {person_name} ({count+1}/{num_photos})", frame)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('c') or key == ord('C'):
            filename = f"{folder}/photo_{datetime.now().strftime('%H%M%S')}.jpg"
            cv2.imwrite(filename, frame)
            count += 1
            print(f"✅ Photo {count}/{num_photos} sauvegardée")
        elif key == ord('q') or key == ord('Q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    print(f"✅ {count} photos sauvegardées dans {folder}")

# ====================== LANCEMENT ======================
if __name__ == "__main__":
    print("=== CAPTURE AUTOMATIQUE DATASET ===")
    capture_for_person("1-Hamdi", 12)
    capture_for_person("2-Ali", 12)
    print("\n🎉 Dataset rempli ! Relance maintenant : python src/face_recognition.py")
      