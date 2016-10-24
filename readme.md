Bookplate application
=====================

Documentation

====================

This application is an application that will add a link to the bottom of a record's catologing page linking to a record's bookplate. The bookplate
itself will include a link back to the original cataloging record.


Deployment


====================




1. Install virtualenv: virtualenv venv --always-copy
2. Activate virtualenv: . venv/bin/activate
3. Install required modules from requirements.txt = pip freeze > requirements.txt
 - pip freeze captures what is already installed. The pipe directs these modules to requirements.txt
 - confused on what modules are installed in your virualenv? use pip freeze!
4.  export FLASK_APP=bookplate.py
5. export FLASK_DEBUG=1
6. flask run --debugger --host=0.0.0.0


Example

===================

Example: http://localhost:8050/005031541
