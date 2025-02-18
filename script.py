import qrcode
import csv
import os
import pandas as pd
from uuid import uuid4
from tqdm import tqdm
from colorama import Fore, Style, init
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

# Initialiser colorama pour gérer les couleurs
init(autoreset=True)

# Configuration pour l'envoi d'emails
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_ADDRESS = "your_email@gmail.com"  # Remplacez par votre adresse email
EMAIL_PASSWORD = "your_password"  # Remplacez par votre mot de passe sécurisé

# Chemin du dossier où les QR codes seront enregistrés
QR_CODES_FOLDER = "qr_codes"

# Fichier CSV pour enregistrer les informations
CSV_FILE = "participants.csv"

# Créer le dossier pour les QR codes si nécessaire
if not os.path.exists(QR_CODES_FOLDER):
    os.makedirs(QR_CODES_FOLDER)

# Initialiser le fichier CSV si nécessaire
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Identifiant", "Nom", "Prénom", "Email", "QR_Code_Fichier"])

def send_email(recipient_email, qr_filename, nom, prenom):
    """
    Envoie un email avec le QR code en pièce jointe.
    """
    print(Fore.BLUE + f"📧 Envoi du QR Code à {recipient_email}...")
    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = recipient_email
        msg["Subject"] = "Votre QR Code pour la tombola"
        
        html_body = f"""
        <html>
        <body>
            <p>Bonjour <b>{prenom} {nom}</b>,</p>
            <p>Merci de participer à notre tombola ! Voici votre QR Code :</p>
            <img src="cid:qr_code" alt="QR Code" style="width:200px;height:200px;"/>
            <p>Bonne chance !</p>
        </body>
        </html>
        """
        msg.attach(MIMEText(html_body, "html"))

        with open(qr_filename, "rb") as img:
            img_data = img.read()
        img_part = MIMEImage(img_data, name=os.path.basename(qr_filename))
        img_part.add_header("Content-ID", "<qr_code>")
        img_part.add_header("Content-Disposition", "inline; filename=qr_code.png")
        msg.attach(img_part)

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)

        print(Fore.GREEN + f"✔️ Email envoyé à {recipient_email} avec succès.")
    except Exception as e:
        print(Fore.RED + f"❌ Erreur lors de l'envoi de l'email : {e}")

def generate_qr_code(nom, prenom, email):
    """
    Génère un QR code pour un participant donné.
    """
    identifiant = str(uuid4())
    qr_content = f"ID: {identifiant}\nNom: {nom}\nPrénom: {prenom}\nEmail: {email}"
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_content)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    qr_filename = f"{QR_CODES_FOLDER}/{identifiant}.png"
    img.save(qr_filename)
    
    with open(CSV_FILE, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([identifiant, nom, prenom, email, qr_filename])
    
    print(Fore.GREEN + f"✔️ QR Code généré pour {prenom} {nom}.")
    send_email(email, qr_filename, nom, prenom)

def main():
    """
    Fonction principale pour gérer l'entrée des utilisateurs.
    """
    while True:
        print(Fore.YELLOW + "\nAjout d'un nouveau participant (laisser vide pour arrêter).")
        nom = input(Fore.CYAN + "Nom : ").strip()
        if not nom:
            break
        prenom = input(Fore.CYAN + "Prénom : ").strip()
        if not prenom:
            break
        email = input(Fore.CYAN + "Email : ").strip()
        if not email:
            break
        
        print(Fore.BLUE + "🔄 Génération du QR Code en cours...")
        for _ in tqdm(range(10), desc="Progression"):
            time.sleep(0.1)
        
        generate_qr_code(nom, prenom, email)

if __name__ == "__main__":
    main()
