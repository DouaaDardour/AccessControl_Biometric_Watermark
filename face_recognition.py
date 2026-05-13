import cv2
import numpy as np
import os

recognizer = cv2.face.LBPHFaceRecognizer_create()
detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

def train_model():
    faces = []
    labels = []
    label_id = 0
    label_map = {}

    for root, dirs, files in os.walk("../dataset"):
        for dir_name in dirs:
            if dir_name.startswith("."): 
                continue
            person_path = os.path.join(root, dir_name)
            label = label_id
            label_map[label] = dir_name
            label_id += 1

            for file in os.listdir(person_path):
                if file.lower().endswith((".jpg", ".png", ".jpeg")):
                    img_path = os.path.join(person_path, file)
                    img = cv2.imread(img_path, 0)
                    faces_detected = detector.detectMultiScale(img, 1.3, 5)
                    for (x, y, w, h) in faces_detected:
                        face_roi = img[y:y+h, x:x+w]
                        faces.append(face_roi)
                        labels.append(label)

    if len(faces) == 0:
        print("❌ Aucun visage trouvé dans dataset/ !")
        return False

    recognizer.train(faces, np.array(labels))
    recognizer.save("../models/trained_model.yml")
    print(f"✅ Modèle entraîné avec succès ! ({len(faces)} visages)")
    print("Utilisateurs :", list(label_map.values()))
    return True

def recognize_face(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        roi = gray[y:y+h, x:x+w]
        try:
            id_, confidence = recognizer.predict(roi)
            if confidence < 65:   # seuil ajustable
                return id_, "Autorisé"
            else:
                return None, "Inconnu"
        except:
            return None, "Inconnu"
    return None, "Aucun visage"

if __name__ == "__main__":
    train_model()