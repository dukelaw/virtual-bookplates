import sys
### activate environment
activate_this = '/var/www/.virtualenvs/bookplate-venv/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))
### activate environment
sys.path.insert (0, '/vagrant/bookplate')
from bookplate import app as application
