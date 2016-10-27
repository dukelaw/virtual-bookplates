Bookplate application
=====================

Documentation

====================

This application is an application that will add a link to the bottom of a record's catologing page linking to a record's bookplate. The bookplate
itself will include a link back to the original cataloging record.

Development Enviroment
====================

1. Install virtualenv: virtualenv venv --always-copy
2. Activate virtualenv: . venv/bin/activate
3. Install required modules from requirements.txt = pip freeze > requirements.txt
 - pip freeze captures what is already installed. The pipe directs these modules to requirements.txt
 - confused on what modules are installed in your virualenv? use pip freeze!
4. export FLASK_APP=bookplate.py
5. export FLASK_DEBUG=1
6. flask run --debugger --host=0.0.0.0

Example

===================
Linking the Configuration file
===================

To link the configuration file (bookplate.conf) to the testing/production machine(vagrant): ln -s /etc/httpd/conf.d /vagrant/bookplate/conf/bookplate.conf

For the development machine(test-apps) we need to git clone environment so apahce can find conf file.

Example: http://localhost:8050/005031541

# staging

Run ansible from the development vagrant environment:

`$ ansible-playbook -vvv --ask-become-pass -i provisioning/stage provisioning/site.yml
`
