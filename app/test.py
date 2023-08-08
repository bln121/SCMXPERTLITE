import random
import smtplib
import string


def generate_random_string(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

random_string = generate_random_string()
print(random_string)

server=smtplib.SMTP('smtp.gmail.com',587)
#adding TLS security 
server.starttls()
#get your app password of gmail ----as directed in the video
#password='*************'
email="lakshminarayanabachu802@gmail.com"
password="qwaccvzyenijymwh"
server.login(email,password)
#generate OTP using random.randint() function
otp=''.join([str(random.randint(0,9)) for i in range(4)])
msg='Hello, Your OTP is '+str(otp)
sender='lakshminarayanabachu802@gmail.com'  #write email id of sender
receiver='lakshminarayanabachu802@gmail.com' #write email of receiver
#sendi
server.sendmail(sender,receiver,msg)
server.quit()