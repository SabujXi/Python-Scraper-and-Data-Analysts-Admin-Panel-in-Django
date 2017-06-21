import os, sys
# if __name__ == '__main__':
#     # Setup environ
sys.path.append(os.getcwd())
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dataproject.settings")

# Setup django
import django
django.setup()

print("Successfully setup django")
# else:
#     print("It's not running as main script")
#     sys.exit(1)
