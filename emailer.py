import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
from smtplib import SMTP, SMTPRecipientsRefused, SMTPSenderRefused, SMTPDataError, SMTPNotSupportedError
from decouple import config


def emailer_datas(data_provided):
    context = ssl.create_default_context()
    recipients = [config('RECIPIENT_EMAIL', default="")]
    sender_email = config('SENDER_EMAIL', default="")
    smtp = SMTP(config('SMTP_SERVER', default=""), config('SMTP_PORT', default=""))
    smtp.set_debuglevel(1)
    smtp.ehlo()
    smtp.starttls()
    smtp.login(config('SENDER_EMAIL', default=""), config('SENDER_PASSWORD', default=""))

    msg = MIMEMultipart("alternative")
    msg['Subject'] = "DATAS ABERTAS"
    msg['From'] = formataddr(("ISEC WATCHER", sender_email))
    msg['To'] = ", ".join(recipients)

    str_list = ""
    for data in data_provided:
        str_list += f"Cadeira: {data['cadeira']} - Data: {data['data']}\n"

    html = f"""
        DATAS PROVIDED:\n
        {str_list}\n\n
        BEIJINHOS
    """
    msg.attach(MIMEText(html, "html"))

    try:
        smtp.sendmail(sender_email, [recipients, sender_email], msg.as_string())
    except (SMTPRecipientsRefused, SMTPSenderRefused, SMTPDataError, SMTPNotSupportedError) as e:
        pass
    finally:
        smtp.quit()


def emailer_notification():
    context = ssl.create_default_context()
    recipients = [config('RECIPIENT_EMAIL', default="")]
    sender_email = config('SENDER_EMAIL', default="")
    smtp = SMTP(config('SMTP_SERVER', default=""), config('SMTP_PORT', default=""))
    smtp.set_debuglevel(1)
    smtp.ehlo()
    smtp.starttls()
    smtp.login(config('SENDER_EMAIL', default=""), config('SENDER_PASSWORD', default=""))

    msg = MIMEMultipart("alternative")
    msg['Subject'] = "DATAS ABERTAS"
    msg['From'] = formataddr(("ISEC WATCHER", sender_email))
    msg['To'] = ", ".join(recipients)

    html = f"""
        SOMETHING IS UP WITH THE INFORESTUDANTE, CHECK IT\n\n
        BEIJINHOS
    """
    msg.attach(MIMEText(html, "html"))

    try:
        smtp.sendmail(sender_email, [recipients, sender_email], msg.as_string())
    except (SMTPRecipientsRefused, SMTPSenderRefused, SMTPDataError, SMTPNotSupportedError) as e:
        pass
    finally:
        smtp.quit()
