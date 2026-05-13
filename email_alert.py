import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

def send_alert(action, user_id=None):
    sender_email = "tonemail@gmail.com"          # ← CHANGE
    app_password = "ton_app_password"            # ← Mot de passe d'application Gmail
    receiver_email = "tonemail@gmail.com"        # ← Ton email

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = f"🚨 ALERTE - {action}"

    body = f"""
    ALERTE DE SÉCURITÉ - BIOMETRIC GUARD
    Action : {action}
    ID Utilisateur : {user_id if user_id else 'Inconnu'}
    Date : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    """
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(sender_email, app_password)
        server.send_message(msg)
        server.quit()
        print(f"✅ Email d'alerte envoyé : {action}")
    except Exception as e:
        print(f"❌ Erreur email : {e}")