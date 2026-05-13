import sys
import cv2
import winsound
import random
from datetime import datetime
from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton, QLabel, 
                             QVBoxLayout, QWidget, QHBoxLayout, QFrame, QMessageBox, 
                             QTableWidget, QTableWidgetItem, QComboBox)
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QFont
import matplotlib.pyplot as plt
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

from database import init_db, add_log
from face_recognition import recognize_face
from watermark import embed_watermark, extract_watermark
from email_alert import send_alert

translations = {
    "fr": {"title": "🔒 BIOMETRIC GUARD", "start": "▶️ DÉMARRER CAMÉRA", "stop": "⏹️ ARRÊTER", 
           "demo": "🚀 MODE DÉMO", "graph": "📊 Graphiques", "pdf": "📄 Exporter PDF",
           "door_closed": "🚪 PORTE FERMÉE", "door_open": "🚪 PORTE OUVERTE ✅",
           "total": "Total Accès", "success": "Taux Réussite", "alerts": "Alertes", "verify": "Vérifier"},
    "ar": {"title": "🔒 BIOMETRIC GUARD - نظام ذكي", "start": "▶️ تشغيل الكاميرا", "stop": "⏹️ إيقاف",
           "demo": "🚀 وضع العرض", "graph": "📊 الرسوم", "pdf": "📄 تصدير PDF",
           "door_closed": "🚪 الباب مغلق", "door_open": "🚪 الباب مفتوح ✅",
           "total": "إجمالي الدخول", "success": "نسبة النجاح", "alerts": "التنبيهات", "verify": "التحقق"}
}

class AccessControlApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_lang = "fr"
        self.setWindowTitle(translations[self.current_lang]["title"])
        self.setGeometry(30, 30, 1350, 920)
        self.setStyleSheet("QMainWindow { background-color: #0f172a; } QLabel { color: #e2e8f0; } QPushButton { background-color: #1e2937; color: #67e8f9; border: 2px solid #67e8f9; border-radius: 10px; padding: 12px; font-weight: bold; } QPushButton:hover { background-color: #67e8f9; color: #0f172a; }")

        init_db()
        self.total_access = 0
        self.success = 0
        self.alerts = 0
        self.setup_ui()
        self.load_logs()

    def setup_ui(self):
        central = QWidget()
        main_layout = QVBoxLayout(central)

        # Langue
        lang_layout = QHBoxLayout()
        self.lang_combo = QComboBox()
        self.lang_combo.addItems(["Français 🇫🇷", "العربية 🇹🇳"])
        self.lang_combo.currentIndexChanged.connect(self.change_language)
        lang_layout.addStretch()
        lang_layout.addWidget(self.lang_combo)
        main_layout.addLayout(lang_layout)

        self.header = QLabel(translations[self.current_lang]["title"])
        self.header.setFont(QFont("Arial", 32, QFont.Weight.Bold))
        self.header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.header.setStyleSheet("color: #67e8f9; background-color: #1e2937; padding: 20px; border-radius: 15px;")
        main_layout.addWidget(self.header)

        dash = QHBoxLayout()
        self.lbl_total = self.create_card(translations[self.current_lang]["total"], "0")
        self.lbl_success = self.create_card(translations[self.current_lang]["success"], "0%")
        self.lbl_alert = self.create_card(translations[self.current_lang]["alerts"], "0")
        dash.addWidget(self.lbl_total)
        dash.addWidget(self.lbl_success)
        dash.addWidget(self.lbl_alert)
        main_layout.addLayout(dash)

        btns = QHBoxLayout()
        self.btn_start = QPushButton(translations[self.current_lang]["start"])
        self.btn_start.clicked.connect(self.start_camera)
        self.btn_stop = QPushButton(translations[self.current_lang]["stop"])
        self.btn_stop.clicked.connect(self.stop_camera)
        self.btn_stop.setEnabled(False)
        self.btn_demo = QPushButton(translations[self.current_lang]["demo"])
        self.btn_demo.clicked.connect(self.start_demo_mode)
        self.btn_graph = QPushButton(translations[self.current_lang]["graph"])
        self.btn_graph.clicked.connect(self.show_graphs)
        self.btn_pdf = QPushButton(translations[self.current_lang]["pdf"])
        self.btn_pdf.clicked.connect(self.export_pdf)

        btns.addWidget(self.btn_start)
        btns.addWidget(self.btn_stop)
        btns.addWidget(self.btn_demo)
        btns.addWidget(self.btn_graph)
        btns.addWidget(self.btn_pdf)
        main_layout.addLayout(btns)

        self.lbl_door = QLabel(translations[self.current_lang]["door_closed"])
        self.lbl_door.setFont(QFont("Arial", 26, QFont.Weight.Bold))
        self.lbl_door.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_door.setStyleSheet("background-color: #ef4444; color: white; padding: 18px; border-radius: 12px;")
        main_layout.addWidget(self.lbl_door)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        main_layout.addWidget(self.table)

        self.setCentralWidget(central)

        self.cap = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

    def create_card(self, title, value):
        frame = QFrame()
        frame.setStyleSheet("background-color: #1e2937; border-radius: 12px; padding: 15px;")
        layout = QVBoxLayout(frame)
        lbl_t = QLabel(title)
        lbl_t.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_v = QLabel(value)
        lbl_v.setFont(QFont("Arial", 28, QFont.Weight.Bold))
        lbl_v.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(lbl_t)
        layout.addWidget(lbl_v)
        return frame

    def change_language(self, index):
        self.current_lang = "ar" if index == 1 else "fr"
        self.header.setText(translations[self.current_lang]["title"])
        self.btn_start.setText(translations[self.current_lang]["start"])
        self.btn_stop.setText(translations[self.current_lang]["stop"])
        self.btn_demo.setText(translations[self.current_lang]["demo"])
        self.btn_graph.setText(translations[self.current_lang]["graph"])
        self.btn_pdf.setText(translations[self.current_lang]["pdf"])
        self.lbl_door.setText(translations[self.current_lang]["door_closed"])
        self.load_logs()

    def start_camera(self):
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            QMessageBox.critical(self, "Erreur", "Impossible d'ouvrir la caméra")
            return
        self.btn_start.setEnabled(False)
        self.btn_stop.setEnabled(True)
        self.timer.start(30)

    def stop_camera(self):
        self.timer.stop()
        if self.cap: self.cap.release()
        self.btn_start.setEnabled(True)
        self.btn_stop.setEnabled(False)

    def start_demo_mode(self):
        self.btn_demo.setEnabled(False)
        self.demo_index = 0
        self.demo_timer = QTimer()
        self.demo_timer.timeout.connect(self.run_demo_step)
        self.demo_timer.start(1500)

    def run_demo_step(self):
        if self.demo_index >= 12:
            self.demo_timer.stop()
            self.btn_demo.setEnabled(True)
            return
        status = random.choice(["Autorisé", "Autorisé", "Inconnu", "Refusé"])
        action = "ACCÈS AUTORISÉ" if status == "Autorisé" else "INTRUSION / INCONNU"
        if status == "Autorisé":
            self.open_door()
        else:
            self.trigger_alert()
        wm_file = embed_watermark(action, random.randint(1, 5))
        add_log(random.randint(1, 5), action, wm_file)
        self.update_dashboard(status == "Autorisé")
        self.load_logs()
        self.demo_index += 1

    def open_door(self):
        self.lbl_door.setText(translations[self.current_lang]["door_open"])
        self.lbl_door.setStyleSheet("background-color: #22c55e; color: white; padding: 18px; border-radius: 12px;")
        winsound.Beep(900, 350)
        QTimer.singleShot(2200, self.close_door)

    def close_door(self):
        self.lbl_door.setText(translations[self.current_lang]["door_closed"])
        self.lbl_door.setStyleSheet("background-color: #ef4444; color: white; padding: 18px; border-radius: 12px;")

    def trigger_alert(self):
        self.alerts += 1
        winsound.Beep(300, 800)

    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret: return
        user_id, status = recognize_face(frame)
        authorized = (user_id is not None and status == "Autorisé")
        action = "ACCÈS AUTORISÉ" if authorized else "INTRUSION / INCONNU"
        color = (0, 255, 0) if authorized else (0, 0, 255)
        if not authorized:
            self.trigger_alert()
        wm_file = embed_watermark(action, user_id if user_id else 0)
        add_log(user_id if user_id else 0, action, wm_file)
        cv2.putText(frame, action, (50, 80), cv2.FONT_HERSHEY_SIMPLEX, 1.8, color, 4)
        cv2.imshow("BIOMETRIC GUARD - Caméra", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            self.stop_camera()
        self.update_dashboard(authorized)
        self.load_logs()

    def update_dashboard(self, authorized):
        self.total_access += 1
        if authorized: self.success += 1
        rate = int((self.success / self.total_access) * 100) if self.total_access > 0 else 0
        self.lbl_total.findChildren(QLabel)[1].setText(str(self.total_access))
        self.lbl_success.findChildren(QLabel)[1].setText(f"{rate}%")
        self.lbl_alert.findChildren(QLabel)[1].setText(str(self.alerts))

    def load_logs(self):
        import sqlite3
        conn = sqlite3.connect('../database.db')
        c = conn.cursor()
        c.execute("SELECT timestamp, user_id, action, watermark FROM logs ORDER BY id DESC LIMIT 15")
        rows = c.fetchall()
        conn.close()
        self.table.setRowCount(len(rows))
        self.table.setHorizontalHeaderLabels(["Heure", "ID", translations[self.current_lang]["verify"], "Action"])
        for i, row in enumerate(rows):
            self.table.setItem(i, 0, QTableWidgetItem(str(row[0])))
            self.table.setItem(i, 1, QTableWidgetItem(str(row[1])))
            self.table.setItem(i, 3, QTableWidgetItem(str(row[2])))
            btn = QPushButton(translations[self.current_lang]["verify"])
            btn.clicked.connect(lambda checked, p=row[3]: self.verify_watermark(p))
            self.table.setCellWidget(i, 2, btn)

    def verify_watermark(self, path):
        if extract_watermark(path):
            QMessageBox.information(self, "✅ Authentique", "Tatouage + QR Code intact !")
        else:
            QMessageBox.critical(self, "❌ Fraude", "Le log a été modifié !")

    def show_graphs(self):
        if self.total_access == 0:
            QMessageBox.information(self, "Info", "Aucun accès enregistré pour le moment.")
            return
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        fig.suptitle('Statistiques BIOMETRIC GUARD', fontsize=16, color='#67e8f9')
        labels = ['Accès Autorisés', 'Refusés / Inconnus']
        sizes = [self.success, self.total_access - self.success]
        ax1.pie(sizes, labels=labels, autopct='%1.1f%%', colors=['#22c55e', '#ef4444'])
        ax1.set_title('Taux de Réussite')
        heures = list(range(8, 20))
        acces = [random.randint(3, 18) for _ in heures]
        ax2.plot(heures, acces, marker='o', color='#67e8f9', linewidth=3)
        ax2.set_title('Accès par heure')
        ax2.set_xlabel('Heure')
        ax2.set_ylabel('Nombre d\'accès')
        ax2.grid(True)
        plt.show()

    def export_pdf(self):
        doc = SimpleDocTemplate("Rapport_Biometric_Guard.pdf", pagesize=A4)
        styles = getSampleStyleSheet()
        elements = []
        elements.append(Paragraph("<b>Rapport Final - Système de Contrôle d'Accès Biométrique</b>", styles['Title']))
        elements.append(Paragraph(f"Généré le {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
        import sqlite3
        conn = sqlite3.connect('../database.db')
        c = conn.cursor()
        c.execute("SELECT timestamp, user_id, action FROM logs ORDER BY id DESC LIMIT 30")
        data = [['Heure', 'ID Utilisateur', 'Action']] + c.fetchall()
        conn.close()
        table = Table(data)
        table.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1e40af')),
                                   ('TEXTCOLOR', (0,0), (-1,0), colors.white),
                                   ('GRID', (0,0), (-1,-1), 1, colors.black)]))
        elements.append(table)
        doc.build(elements)
        QMessageBox.information(self, "✅ Succès", "Rapport PDF généré !\nNom : Rapport_Biometric_Guard.pdf")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AccessControlApp()
    window.show()
    sys.exit(app.exec())