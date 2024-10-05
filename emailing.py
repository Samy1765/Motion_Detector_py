import smtplib
from email.message import EmailMessage
import imghdr

password="trog xcwt rvzz pmvd"

def send_email(image_path):
   email=EmailMessage()
   email['Subject']='Motion Dectected'
   email.set_content("We Just Saw Someone Near Your House")

   with open(image_path,"rb") as file:
      file_data = file.read()
      file_type = imghdr.what(None, file_data)
   
   email.add_attachment(file_data,maintype="image",subtype=file_type)

   gmail=smtplib.SMTP("smtp.gmail.com",587)
   gmail.ehlo()
   gmail.starttls()
   gmail.login("swayamdeshmukh1765p@gmail.com",password)
   gmail.sendmail("swayamdeshmukh1765p@gmail.com","swayamdeshmukh1765p@gmail.com",email.as_string())
   gmail.quit()
