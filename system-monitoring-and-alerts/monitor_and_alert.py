import psutil
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def check_system_metrics(cpu_threshold, disk_threshold, memory_threshold):
    """Check system metrics and return a list of alerts if thresholds are exceeded."""
    alerts = []

    # Check CPU usage
    cpu_usage = psutil.cpu_percent(interval=1)
    if cpu_usage > cpu_threshold:
        alerts.append(f"CPU usage is high: {cpu_usage}%")

    # Check Disk space
    disk_usage = psutil.disk_usage('/')
    if disk_usage.percent > disk_threshold:
        alerts.append(f"Disk space is low: {disk_usage.percent}% used")

    # Check Memory usage
    memory_usage = psutil.virtual_memory().percent
    if memory_usage > memory_threshold:
        alerts.append(f"Memory usage is high: {memory_usage}% used")

    return alerts

def send_alert_email(subject, body, to_email, from_email, smtp_server, smtp_port, smtp_user, smtp_password):
    """Send an alert email."""
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_password)
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
    print("Alert email sent!")

if __name__ == "__main__":
    # Configuration
    CPU_THRESHOLD = 80  # percent
    DISK_THRESHOLD = 90  # percent
    MEMORY_THRESHOLD = 80  # percent

    ALERT_EMAIL = 'alert@example.com'
    FROM_EMAIL = 'monitor@example.com'
    SMTP_SERVER = 'smtp.example.com'
    SMTP_PORT = 587
    SMTP_USER = 'smtp_user'
    SMTP_PASSWORD = 'smtp_password'

    # Check system metrics
    alerts = check_system_metrics(CPU_THRESHOLD, DISK_THRESHOLD, MEMORY_THRESHOLD)

    if alerts:
        alert_subject = "System Monitoring Alert"
        alert_body = "\n".join(alerts)
        send_alert_email(
            subject=alert_subject,
            body=alert_body,
            to_email=ALERT_EMAIL,
            from_email=FROM_EMAIL,
            smtp_server=SMTP_SERVER,
            smtp_port=SMTP_PORT,
            smtp_user=SMTP_USER,
            smtp_password=SMTP_PASSWORD
        )
