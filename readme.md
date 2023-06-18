### Blogging app api

# API DOCUMENTATION :https://documenter.getpostman.com/view/17012881/2s93si1q1d#e8af89ed-97ec-4424-9970-296dea8f6be3

### Note 
The bonous requirement Rate limiting to prevent api abuse it is done by the 
```
'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/sec',
        'user': '1000/day'
    },

```

steps to start the server
step 1: Create virtual environment<br/>
`python -m venv your_virtual_environment_name`

step 2: Activate virtual environment
if linux:<br/>
    `source your_virtual_environment_name/bin/activate`
if windowns:<br/>
    `your_virtual_environment_name\Source\Activate`

step 3: Install the packages<br/>
`pip install -r requirements.txt`

setp 4: Spin the server<br/>
`python manage.py runserver`


## Run the test 

after activating the your_virtual_environment_name
run command `python manage.py test`

