Social Circle - a Social Network by Samuele Zecchini & Micaela Verucchi


Software neeeded to run our application : 

	-Django :
		pip install Django==1.8
		sudo pip install --upgrade Django 

	-virtualenv:
		sudo pip install virtualenv

	-virtualenvwrapper:
		sudo pip install virtualenvwrapper

	-pyOpenSSL:
		sudo pip install pyOpenSSL

	-twisted 
		#move to home dir
		cd ~

		#checkout the twisted project
		git clone https://github.com/twisted/twisted.git twisted-websocket 

		#switch to the most up to date websocket branch
		cd twisted-websocket
		git fetch
		git checkout websocket-4173-4
	 
		#install
		python setup.py install

How to run SocialCircle :

	-move to SN dir (where file manage.py is)

	-Start Django server:
		python manage.py runserver

	-Start Chat server:
		twistd -n -y chatserver.py	


