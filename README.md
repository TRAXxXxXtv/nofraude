# Générateur de QR Codes 

## Description
Ce projet est une application Python permettant de générer des QR Codes pour des participants à une tombola. Chaque participant reçoit un QR Code unique par email après son inscription. Les informations des participants sont enregistrées dans un fichier CSV.

## Fonctionnalités
- Génération d'un QR Code unique pour chaque participant
- Vérification des doublons pour éviter les inscriptions multiples
- Enregistrement des informations des participants dans un fichier CSV
- Envoi automatique du QR Code par email
- Affichage de la liste des participants enregistrés

## Prérequis
Avant d'exécuter le script, assurez-vous d'avoir installé les dépendances suivantes :

```bash
pip install qrcode pandas tqdm colorama smtplib
```

## Installation et Exécution
1. Clonez ce dépôt ou téléchargez les fichiers.
2. Installez les dépendances avec :
   ```bash
   pip install -r requirements.txt
   ```
3. Configurez votre adresse email et votre mot de passe dans le script (`EMAIL_ADDRESS` et `EMAIL_PASSWORD`).
4. Exécutez le script avec la commande :
   ```bash
   python script.py
   ```
5. Suivez les instructions pour ajouter des participants.

## Configuration des Emails
Ce script utilise un serveur SMTP (Gmail par défaut) pour l'envoi des emails. Assurez-vous d'activer l'option "Accès aux applications moins sécurisées" ou d'utiliser un mot de passe d'application.

## Structure du Projet
```
📁 qr_codes/              # Dossier contenant les QR Codes générés
📄 participants.csv       # Fichier CSV contenant les informations des participants
📄 script.py             # Script principal du projet
```

## Sécurité
Ne partagez pas votre mot de passe email en dur dans le script. Il est recommandé d'utiliser des variables d'environnement pour stocker les identifiants sensibles.

## Auteur
Ce projet a été réalisé par TRAX.

