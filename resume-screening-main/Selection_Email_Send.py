import smtplib as s

from flask import render_template


def selection_mail(x):

    ob =s.SMTP('smtp.gmail.com',587)
    ob.ehlo()
    ob.starttls()
    ob.login('sahilgupta89177@gmail.com','zblghbgxwsnfhmgr')

    subject="Resume Shortlisted"

    body="Congratulation your resume is shortlisted"
    message="subject:{}\n\n{}".format(subject,body)



    ob.sendmail('sahilgupta89177@gmail.com', x, message)
    print('Mail Sent Successfully')
    ob.quit()
