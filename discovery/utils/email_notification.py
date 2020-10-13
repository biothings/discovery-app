import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import config


def send_mail(sendto, subject, message, alt_text=""):
    """A utility function to send an html email.
       message should be a HTML string, alt_text can be provided
       as a text-only version.
    """
    # Ref: https://docs.aws.amazon.com/ses/latest/DeveloperGuide/examples-send-using-smtp.html

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    # msg['From'] = email.utils.formataddr((SENDERNAME, SENDER))
    msg['From'] = config.EMAIL_DEFAULT_FROM
    msg['To'] = sendto
    # Comment or delete the next line if you are not using a configuration set
    # msg.add_header('X-SES-CONFIGURATION-SET',CONFIGURATION_SET)

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(alt_text, 'plain')
    part2 = MIMEText(message, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)

    # Try to send the message.
    try:
        server = smtplib.SMTP(config.EMAIL_HOST, config.EMAIL_PORT)
        server.ehlo()
        server.starttls()
        #stmplib docs recommend calling ehlo() before & after starttls()
        server.ehlo()
        server.login(config.EMAIL_HOST_USER, config.EMAIL_HOST_PASSWORD)
        server.sendmail(msg['From'], msg['To'], msg.as_string())
        server.close()
    # Display an error message if something goes wrong.
    except Exception as e:
        print("Error: ", e)
    else:
        print("Email sent!")
