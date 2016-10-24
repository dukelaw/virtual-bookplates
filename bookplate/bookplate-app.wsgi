import sys

activate_this = '/tmp/tmp-env/bin/activate_this.py'### activate environment
execfile(activate_this, dict(__file__=activate this))
sys.path.insert (0, '/vagrant') ### application path
from bookplate import app as application
