# cornershop-backend-test-henriquez

## Prerequisites

Before running the application, the following actions must be performed for proper operation

### Create Slack App

 - Open link https://api.slack.com/apps
 - Press "Create New App" button
 - Chose "From an app manifest"
 - Select a Workspace
 - Press Next
 - Paste Slack App manifest [from this YAML slack app manifest file](slack_app_manifest.yml)
 - Press Next
 - Press Create
 - Press button "Install to Workspace"
 - Review permisions and allow
 - Go to "OAuth & Permissions"
 - Copy Bot User OAuth Token


### Set OAuth Token into env variable
Create `.env` into `backend_test` folder with this example content
```
SLACK_OAUTH_TOKEN=xoxb-code-example
```


## Running the development environment

* `make up`
* `dev up`
* `dev celery` (`celery -A backend_test worker -Q celery -E -l info`) [ in a new terminal ]
* `celery -A backend_test beat -l INFO` [ in a new terminal ]

##### Rebuilding the base Docker image

* `make rebuild`

##### Resetting the local database

* `make reset`


### Create Nora user
Open a python shell and create Nora (admin) user

_Example:_
```python
from django.contrib.auth.models import User
u = User.objects.create_user("nora", "nora@cornershop.com", "nora123")
u.save()
```

### Hostnames for accessing the service directly

* Local: http://127.0.0.1:8000/

## User Manual

To read a brief user manual, [click here](./manual/README.md)

## Software Development Considerations

To read a brief user manual, [click here](./manual/development.md)