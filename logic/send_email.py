from util import sendgrid_wrapper as sgw

try:
    sgw.notify_admins('This is a test message', 'Test Subject')
except Exception as e:
    print(e)