import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
from config import constants
from util import sendgrid_wrapper as sgw

try:
    sgw.notify_admins('This is a test message', 'Test Subject')
except Exception as e:
    print(e)