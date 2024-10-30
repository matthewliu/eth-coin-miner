import sendgrid
import sendgrid.helpers.mail as sgh
from config import constants

class Email(object):
    def __init__(self, email, name):
        self.email = email
        self.name = name

class Attachment(object):
    def __init__(self, content, type, file_name, disposition, content_id):
        self.content = content
        self.type = type
        self.file_name = file_name
        self.disposition = disposition
        self.content_id = content_id

def notify_admins(message, subject=None):
    if 'localhost' in constants.HOST or 'pagekite' in constants.HOST:
        recipients=[Email(constants.DEV_EMAIL, constants.DEV_EMAIL)]
        subject = 'DEV: ' + str(subject) if subject else str(message)
    else:
        recipients = [Email(constants.DEV_EMAIL, constants.DEV_EMAIL)]
        subject = str(subject) if subject else str(message)

    send_message(
		sender=Email(constants.DEV_EMAIL, constants.DEV_EMAIL),
		recipients=recipients,
		subject=subject,
		body_text=message,
		body_html=message,
		categories=['my-app', 'notify_admins'])

def send_message(sender, recipients, subject, body_text, body_html, 
    attachments=None, ccs=None, bccs=None, categories=None, send=True):
    
    sg_api = sendgrid.SendGridAPIClient(constants.SENDGRID_API_KEY)
    mail = sgh.Mail()
    mail.from_email = sgh.Email(sender.email, sender.name)
    mail.subject = subject
    
    for recipient in recipients:
        personalization = sgh.Personalization()
        personalization.add_to(sgh.Email(recipient.email, recipient.name))

        if ccs:
            for cc in ccs:
                personalization.add_cc(sgh.Email(cc.email))
        if bccs:
            for bcc in bccs:
                personalization.add_bcc(sgh.Email(bcc.email))
        mail.add_personalization(personalization)

    mail.add_content(sgh.Content("text/plain", body_text))
    mail.add_content(sgh.Content("text/html", body_html))

    if attachments:
        for attach in attachments:
            attachment = sgh.Attachment()
            attachment.file_content = sgh.FileContent(attach.content)
            attachment.file_type = sgh.FileType(attach.type)
            attachment.file_name = sgh.FileName(attach.file_name)
            attachment.disposition = sgh.Disposition(attach.disposition)
            attachment.content_id = sgh.ContentId(attach.content_id)
            mail.add_attachment(attachment)
    if categories:
        for category in categories:
            mail.add_category(sgh.Category(category))
    if send:
        response = sg_api.client.mail.send.post(request_body=mail.get())
        print(response.status_code)
        print(response.body)
        print(response.headers)


