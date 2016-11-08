# Virtual Bookplates

# Summary

This application is an application that will add a link to the bottom of a
record's cataloging page linking to a record's bookplate. The bookplate itself
will include a link back to the original cataloging record.

Links to the application such as https://extranet2.law.duke.edu/bookplate/004231017


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

Example: http://localhost:8080/005031541

# Staging

Run ansible from the development vagrant environment:

`$ ansible-playbook -vvv --ask-become-pass -i provisioning/stage provisioning/site.yml`

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

# instructions for manual deployment on production machine(extranet)
- log into root: sudo -s
- Go to the project directory: cd /srv/www/virtual-bookplates
- Clone the project repo: git clone git@gitlab.oit.duke.edu:law-library-webapps/virtual-bookplates.git
- provisioning/site.yml is the first playbook that runs. site.yml triggers provisioning/appservers.yml.
- According to appservers.yml, the first modules that need to be installed are the directives listed in the "common" playbooks. And then after that we need to install the modules described in the "appservers" playbooks.
- So let's start with the "common" playbooks (virtual-bookplates/provisioning/roles/common/tasks)
  - To get the order of the "common" playbooks, go to main.yml. You'll see that the order goes yum.yml, packages.yml, and then system.yml
  - Going to yum.yml, you need do "yum install [module_name]" for the following modules:
    - yum-conf-repos
    - yum-conf-epel
    - libxml2-devel
    - libxslt-devel
  - The modules listed in packages.yml should already be installed.
  - Moving on to system.yml
    - All we need to do is install mod_wsgi: yum install mod_wsgi
- Now we turn our attention to the appservers playbooks (provisioning/roles/appservers/tasks)
  - go to main.yml and see that python.yml runs first and then app.yml.
  - from python.yml we need to install python-devel and pip:
    - yum install python-devel
    - yum install python-pip
  - Now we move on to app.yml. Since this playbook involves installing app-specific dependencies, we need to install a virtual environment
    - yum install python-virtualenv
    -  cd /srv/dls/extranet (this is where our virtualenv needs to go)
    - virtualenv .virtualenvs/bookplate-venv (creating the env)
    - source .virtualenvs/bookplate-venv/bin/activate (activating the env)
    - cd /srv/www/virtual-bookplates
  - Now that the virtualenv is set up, we can now install the modules into this environment that are listed in requirements.txt.
    - pip install -r requirements.txt
  - Next, we need to move our configuration files (.wsgi and .conf):
    - First we move the .wsgi file. Move to the /bookplate directory and then type: cp ../provisioning/roles/appservers/templates/bookplate-app.wsgi.j2
    - Then take off the .j2: mv bookplate-app.wsgi.j2 bookplate-app.wsgi
    - Now we need to edit the .wsgi file. Open it up in vi/vim and replace the venv_dir and app_dir with their respective paths (paths listed in provisioning/group_vars/production)
    - Next we need to move the .conf file. cd into bookplate/conf and copy the file over: cp ../../provisioning/roles/appservers/templates/bookplate.conf.j2
    - remove the .j2: mv bookplate.conf.j2 bookplate.conf
    - Now we need to edit the .conf file. Open it up in vi/vim and replace app_dir with it's respective path (listed in provisioning/group_vars/production)
    - next we need to create a link to this file in extranet's conf directory
      - cd srv/dls/extranet
      - ln -s /srv/www/virtual-bookplates/bookplate/conf/bookplate.conf bookplate.conf
  - this should handle all the configuration.
  - now cd /srv/www/virtual-bookplates
  - apachectl restart
  - go to: https://extranet2.law.duke.edu/bookplate/005130938 to test.
  - to pull in code changes, make sure you're in /srv/www/virtual-bookplates and do: git pull origin master
