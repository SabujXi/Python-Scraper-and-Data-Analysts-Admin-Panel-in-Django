import os, sys
sys.path.append(os.getcwd())
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dataproject.settings")
# Setup django
import django
django.setup()
print("Successfully setup django")
