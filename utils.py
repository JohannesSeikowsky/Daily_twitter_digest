# utils
import os, smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime, timedelta
import config

def send(target, subject, content):
	""" sending email """
	email_acc = config.email_account
	email_pw = config.email_pw

	mail = smtplib.SMTP("smtp.gmail.com", 587)
	mail.ehlo()
	mail.starttls()
	mail.login(email_acc, email_pw)

	msg_content = "Subject:{} \n\n {}".format(subject, content)
	mail.sendmail(email_acc, target, msg_content)
	mail.close()


def send_html(receiver, msg_content):

	sender = config.email_account
	receiver = receiver

	# set up message container
	msg = MIMEMultipart('alternative')
	msg['Subject'] = "Daily Twitter Digest"
	msg['From'] = sender
	msg['To'] = receiver

	# Plain-text and an HTML versions of message
	html = msg_content
	"""\
	<html>
	  <head></head>
	  <body>
	    <p>Hi!<br>
	       How are you?<br>
	       Here is the <a href="http://www.python.org">link</a> you wanted.
	    </p>
	  </body>
	</html>
	"""

	# Record the MIME types of messages
	part = MIMEText(html, 'html')

	# Attach parts into message container
	msg.attach(part)

	# Login and send
	email_acc = config.email_account
	email_pw = config.email_pw

	mail = smtplib.SMTP("smtp.gmail.com", 587)
	mail.ehlo()
	mail.starttls()
	mail.login(email_acc, email_pw)

	mail.sendmail(sender, receiver, msg.as_string())
	mail.close()


def digest_delivered_today():
	""" checks whether a digest has already been delivered today """
	todays_date = datetime.now().strftime("%d.%m")

	sent_dates = []
	with open(config.sent_dates_path) as f:
		for each in f:
			sent_dates.append(each[:-1])

	if todays_date in sent_dates:
		return True
	else:
		return False


def record_digest_delivery():
	""" records the date to ensure that no digest is sent twice in a day """
	with open(config.sent_dates_path, "a") as f:
		todays_date = datetime.now().strftime("%d.%m")
		f.write(todays_date + "\n")