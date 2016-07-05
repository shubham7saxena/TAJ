# Teaching Assistance Judge
(***the work is currently in progress***)

# How to set up the project at your local machine?

I guess pip is install at your local machine if not then do:

``` sh
(For Debian based machine)
sudo apt-get install python-pip

(for RedHats)
yum install python-pip
```

``` sh
pip install virtualenv
virtualenv <folder-name>
e.g. #virtualenv CodeJudge
```

Change the directory to folder which you have created
e.g. cd CodeJudge
``` sh
source bin/activate
```

Then clone the repositry and move to folder codejudge and follow these steps:
``` sh
pip install -r requirements.txt
```

For running the application:
``` sh
cd Codejudge
python manage.py makemigrations
python manage migrate
python manage.py runserver
```
go to localhost:8000 to start exploring