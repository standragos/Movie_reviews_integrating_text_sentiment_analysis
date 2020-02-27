#!"E:\Proiect Licenta\movie classifier\venv\Scripts\python.exe"
# EASY-INSTALL-ENTRY-SCRIPT: 'clf==0.5.7','console_scripts','clf'
__requires__ = 'clf==0.5.7'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('clf==0.5.7', 'console_scripts', 'clf')()
    )
