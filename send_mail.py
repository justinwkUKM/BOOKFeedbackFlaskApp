import smtplib
from email.mime.text import MIMEText


def send_mail(customer, book, publisher, rating, comments):
    port = 2525
    smtp_server = 'smtp.mailtrap.io'
    login = '098202cfb1b40f'
    password = '7798e6b0990ca9'
    message = f"<h3>New Feedback Submission</h3><ul><li>Customer: {customer}</li><li>Book: {book}</li><li>Publisher: {publisher}</li><li>Rating: {rating}</li><li>Comments: {comments}</li></ul>"

    sender_email = 'waquaskhalid@yahoo.com'
    receiver_email = 'waqasobeidy@gmail.com'
    msg = MIMEText(message, 'html')
    msg['Subject'] = 'MyBooks Feedback'
    msg['From'] = sender_email
    msg['To'] = receiver_email

    # Send email
    with smtplib.SMTP(smtp_server, port) as server:
        server.login(login, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())