import os
from django.conf import settings

AUTHORIZED_USERS_FILE_PATH = os.path.join(settings.BASE_DIR, 'authorized_users.txt')
