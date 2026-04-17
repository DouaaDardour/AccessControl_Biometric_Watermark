# 🔒 BIOMETRIC GUARD - Système de Contrôle d'Accès Biométrique avec Tatouage Numérique

**Projet de fin de module** - Biométrie, Tatouage Numérique et Sécurité Numérique (ING-4 SSIRF)

---

## 📋 Description du Projet

Un système complet de contrôle d'accès par **reconnaissance faciale** avec :
- Tatouage numérique (LSB) des logs pour garantir l'intégrité
- QR Code visible sur chaque log
- Interface moderne Dark Mode
- Simulation de porte avec animation + son
- Mode Démo automatique
- Multi-langue (Français / العربية)
- Graphiques en temps réel
- Export PDF du rapport

---

## ✨ Fonctionnalités Principales

- Authentification faciale en temps réel (OpenCV + LBPH)
- Tatouage invisible + QR Code sur chaque log
- Animation de porte + sons (accès autorisé / alerte)
- Dashboard en temps réel (taux de réussite, alertes...)
- Mode Démo (12 accès simulés automatiquement)
- Support arabe / français
- Graphiques (camembert + courbe)
- Export PDF professionnel
- Alertes email

---

## 🛠️ Technologies Utilisées

- **Python 3.13**
- OpenCV + LBPH Face Recognizer
- PyQt6 (interface)
- SQLite
- Pillow + qrcode
- Matplotlib (graphiques)
- ReportLab (PDF)
- Winsound + Pygame (sons)

---

## 📁 Structure du Projet
AccessControl_Biometric_Watermark/
├── src/
│   ├── main.py                 ← Application principale
│   ├── database.py
│   ├── face_recognition.py
│   ├── watermark.py            ← Tatouage + QR Code
│   ├── email_alert.py
│   └── tests_robustesse.py
├── dataset/                    ← Photos d'entraînement
├── logs/                       ← Logs tatoués + QR
├── models/                     ← Modèle LBPH
├── database.db
└── README.md
text---

## 🚀 Comment exécuter le projet

```bash
# 1. Activer l'environnement
venv\Scripts\activate

# 2. Lancer l'application
python src/main.py

🎥 Démonstration

Mode Démo : Clique sur le bouton "MODE DÉMO"
Change la langue avec le menu en haut
Teste la reconnaissance faciale avec ta webcam


👨‍💻 Auteur
Douaa Dardour & khayem zribi 
Projet réalisé dans le cadre du module Biométrie & Tatouage Numérique

⭐ N'hésite pas à mettre une étoile si tu trouves ce projet utile !










Projet réalisé dans le cadre du module Biométrie & Tatouage Numérique

⭐ N'hésite pas à mettre une étoile si tu trouves ce projet utile !
