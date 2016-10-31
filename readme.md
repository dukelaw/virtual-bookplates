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
# Templates

In the folder /provisioning/group_vars, we store variables for the development, production, and staging ("stage") server.
Variables in this folder include Configuration aspects such as "remote user", which we use to store the user,
"venv_dir", which we use to store the directory of our virtual environment, and "project_dir", which stores the path for the project.

For the configuration files in the provisioning/templates directory,
we utilize the "app_dir" variable from /provisioning/group_vars to store the path for the actual application (.../bookplate), which
differs between the vagrant server (development), and the Duke servers (stage, production). This is necessary for the server
to be able find the application in order to run it.


Configuration for the bookplate app is handled in /provisioning/templates.  One template that we have is bookplate.conf.j2, which
serves as our Apache .conf file. This file includes a series of directives which utilizes Apache to configure the server that
will be running our app. We use app_dir to tell the server where our app is located.

Also in the /provisioning/templates folder is bookplate-app.wsgi.j2, which is referenced in the .conf file. This wsgi file serves as a template for
configuring python on the server that runs our app. This is also the file that runs the app itself. This file utilizes apache to as a way for python and html
to communicate. First, this file activates our virtual environment using the "venv_dir" variable in the group_vars directory. Once the environment is set up
we then use app_dir to tell the server the location of our app, which it then runs.

# The Playbooks

Ansible playbooks are located in provisioning/roles/tasks. There are three playbooks, main.yml, python.yml, app.yml. Main.yml is a playbook that runs the other two
playbooks: app.yml and python.yml, in that order.

App.yml handles server setup tasks such as copying the project repo  from gitlab to a directory on the server being used,
getting the requisite ssh keys in the right directories, moving various files to the correct directory, activating our template files
based off of which server is running the app, etc.

Python.yml is triggered after app.yml through main.yml. The python.yml playbook installs essential python modules to whatever environment
the app will be running on such as python-devel, pip, etc.
