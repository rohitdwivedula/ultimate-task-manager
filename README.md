# Installation and runtime instructions

1. Create a virtual environment `venv` for this project. 
2. `source venv/bin/activate` - activate the virtual environment.
3. `pip3 install -r requirements.txt`. Install the required libraries.
4. `python manage.py runserver`

# Feature Ideas

1. **Data Ownership**: To make sure that users retain complete control of their data, an option to export all data as a JSON/CSV file would be nice. 
2. **2FA**: Adding a layer of security in addition to the password, we could probably implement time-based two-factor authentication, using something like Google Authenticator.  