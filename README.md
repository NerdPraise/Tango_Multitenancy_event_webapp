# Tango_Multitenancy_event_webapp
A multitenant model of a simple RESTful API for managing calendar events and conference room availability for Tango Limited

### Requirements :
```
python == 3.9.1
Django >= 3.0.0
```
 
API References
### Usage
1. Clone project
2. Create .env file and add a key value pair with the key DJANGO_SECRET_KEY `DJANGO_SECRET_KEY="soome value"`
3. Run `python -m venv venv` to create a virtual environment
4. Run `pip install -r requirements.txt` to install all the necessary required packages
5. Run `python manage.py runserver` to start server and follow code snippet
### Test
cd into root directory and run `python manage.py test tests.unit.test_<feature>`

```python
valid_event_data = {
        "user": "1",
        "event_name": "Management",
        "meeting_agenda": "Info about work",
        "start_time": "2018-06-29 08:16",
        "end_time": "2018-06-29 08:19",
        "participants": [
            "admin@admin.admin"],
    }

valid_conference_data = {
    "name": 'Room A",
    "address": "Some place"
}

``` 

##### NB: This project was made with some assumptions in mind 
1. Once a room is booked, it can't be booked again, this is to avoid implementing additional business requirements that aren't required
2. Tenancy system adopted is a shared schema, shared database system
3. The endpoints are user timezone-aware but not the admin dashboard 
4. The concept of company tenancy is made abstract to user
5. No user management api 