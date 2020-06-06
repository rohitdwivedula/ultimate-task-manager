# Installation and runtime instructions

1. Create a virtual environment `venv` for this project. 
2. `source venv/bin/activate` - activate the virtual environment.
3. `pip3 install -r requirements.txt`. Install the required libraries.
4. `python manage.py runserver`
5. REST API documentation can be dound in `docs`. 
6. `python manage.py send_reminders` is a Django custom management/admin command that was written to trigger reminder emails and Discord notifications to users. This can be set up as a CRON job to run every morning to automate this. 

# Acknowledgements
Home page photo "Do Something Great" courtesy of Clark Tibbs on Unsplash.