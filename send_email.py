import smtplib
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(sender_email, sender_password, receiver_email, subject, content):
    # smtp_server = "smtp.163.com"
    # smtp_port = 465

    # if type(receiver_email) == list:
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = ", ".join(receiver_email)
    msg['Subject'] = subject

    #添加正文 (纯文本)
    # msg.attach(MIMEText(content, 'plain'))
    #添加正文 (HTML) 格式更规范
    msg.attach(MIMEText(content, 'html'))
    server = smtplib.SMTP("smtp.163.com", 25)

    try:
        server.starttls()
        server.login(sender_email, sender_password) #登录邮箱
        # send email
        server.sendmail(sender_email, receiver_email, msg.as_string())
        print('Email sent!')
    except Exception as e:
        print(f"Error: {e}")
    finally:
        server.quit()


sender_email = 'lsc03129934@163.com'
sender_password = 'liu3124488'
# receiver_email = 'lsc03129934@163.com'
# receiver_email = 'liuxinrannn0123@163.com'
receiver_email = ['lsc03129934@163.com','liuxinrannn0123@163.com','menglingchao0115@163.com','3141437436@qq.com','2571510186@qq.com','dorgon.aisin@gmail.com']
# receiver_email = ['dorgon.aisin@gmail.com']
subject = 'Test Email'
# content = 'A test email from Python script'
content = """
<html>
    <body>
        <p>Hello Guys!<p>
        <p>This is an email from a Python script<p>
        <p>Please do not do any reply!<p>
        <p>Thx :)<p>
        <div style="text-align: right; margin-top: 50px;">
            <p>Best Regards!</p>
            <p><strong>Dorgon Aisin</strong></p>
            <p><em>ChiHan Tech Inc.</em></p>
        </div>
    </body>
</html>
"""

# for i in range(5):
#     time.sleep(1)
send_email(sender_email, sender_password, receiver_email, subject, content)