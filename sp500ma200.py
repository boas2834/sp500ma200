import pandas as pd
import yfinance as yf
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

def get_sp500_data():
    # Holen der S&P 500 Daten über die letzten 214+ Tage (200-Tage-Gleitender-Durchschnitt + 14 Tage für den Trend)
    sp500 = yf.Ticker("^GSPC")
    data = sp500.history(period="1y")

    # Berechnen des 200-Tage-Gleitenden-Durchschnitts (MA 200)
    data['MA200'] = data['Close'].rolling(window=200).mean()

    # Aktueller Schlusskurs und 200-Tage-Durchschnitt
    current_price = data['Close'][-1]
    current_ma200 = data['MA200'][-1]

    # Berechnen der prozentualen Abweichung für die letzten 14 Tage
    data['Deviation'] = ((data['Close'] - data['MA200']) / data['MA200']) * 100
    last_14_days_deviation = data['Deviation'][-14:]  # Die letzten 14 Tage der Abweichung

    # Aktuelle Abweichung
    deviation_percentage = last_14_days_deviation[-1]
    
    return current_price, current_ma200, deviation_percentage, last_14_days_deviation


def display_results(current_price, current_ma200, deviation_percentage, last_14_days_deviation):
    # Ergebnisse auf dem Bildschirm anzeigen und gleichzeitig als E-Mail-Inhalt vorbereiten
    results = []
    results.append(f"S&P 500 Daten - {datetime.now().strftime('%Y-%m-%d')}")
    results.append(f"")
    results.append(f"Erstellt auf SRV 192.168.1.50")
    results.append(f"")
    results.append(f"Aktueller Wert des SP500: {current_price:.2f}$")
    results.append(f"200-Tage-Gleitender-Durchschnitt (MA 200): {current_ma200:.2f}$")
    results.append(f"")
    results.append(f"")
    results.append(f"Prozentuale Abweichung (heute): {deviation_percentage:.2f} %")
    results.append(f"")
    results.append(f"")


    # Kauf-/Verkauf-Empfehlung basierend auf heutiger Abweichung
    if deviation_percentage < 0:
        results.append("Verkaufssignal")
    elif 0 <= deviation_percentage < 10:
        results.append("Halten")
    else:
        results.append("Kaufsignal")


    # Trend der letzten 14 Tage mit Handlungsempfehlung hinzufügen
    results.append("\nTrend der prozentualen Abweichung der letzten 14 Tage:")
    for i, deviation in enumerate(last_14_days_deviation, start=1):
        date = (datetime.now() - pd.Timedelta(days=14-i)).strftime('%Y-%m-%d')
       if deviation < 0:
            recommendation = "Verkaufssignal"
        elif 0 <= deviation < 10:
            recommendation = "Halten"
        else:
            recommendation = "Kaufsignal"
        results.append(f"Tag {i} ({date}): {deviation:.2f} % - {recommendation}")

    # Ausgabe auf dem Bildschirm
    for line in results:
        print(line)

    # Inhalte für die E-Mail zurückgeben
    return "\n".join(results)

def load_recipients(file_path):
    # Einlesen der E-Mail-Empfänger aus einer Textdatei
    with open(file_path, "r") as file:
        recipients = [line.strip() for line in file if line.strip()]
    return recipients

def send_email(content, recipient_email):
    # E-Mail Konfiguration
    sender_email = "MAILADRESSE@domain.com"
    password = "HIER DAS PASSWORT "

    # E-Mail Inhalt
    subject = f"S&P 500 Daten und Trendanalyse - {datetime.now().strftime('%Y-%m-%d')}"
    body = content

    # E-Mail erstellen
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # SMTP-Server verbinden und E-Mail senden
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)  # Beispiel für Gmail SMTP
        server.starttls()  # TLS-Verschlüsselung starten
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.close()
        print(f"E-Mail erfolgreich an {recipient_email} gesendet!")
    except Exception as e:
        print(f"Fehler beim Senden der E-Mail an {recipient_email}: {e}")


# Empfänger einlesen und E-Mail an jeden einzeln senden
recipients = load_recipients("recipients.txt")
for recipient in recipients:
    send_email(email_content, recipient)

# Skript ausführen
current_price, current_ma200, deviation_percentage, last_14_days_deviation = get_sp500_data()
email_content = display_results(current_price, current_ma200, deviation_percentage, last_14_days_deviation)



