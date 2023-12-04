
###################################################
import smtplib as s

from flask import render_template


def rejection_mail(x):

    ob =s.SMTP('smtp.gmail.com',587)
    ob.ehlo()
    ob.starttls()
    ob.login('sahilgupta89177@gmail.com','zblghbgxwsnfhmgr')

    subject="Resume not Shortlisted"

    body='Thank you for your interest in our company, but after careful consideration, we regret to inform you that \nwe have decided not to move forward with your candidacy.'
    message="subject:{}\n\n{}".format(subject,body)



    ob.sendmail('sahilgupta89177@gmail.com', x, message)
    print("Send mail")
    print('Mail Sent Successfully')
    ob.quit()
