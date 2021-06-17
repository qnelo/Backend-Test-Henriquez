# Software Development Considerations

## About Celery

There is a periodic task that runs every day 2 times that checks if there is a menu for that day and then generates and sends the messages for each user.

It was chosen to have only one recurring task, as it was considered a better option than generating multiple tasks for each menu that is created. In this way, Nora can plan the menu for the whole month or the whole year without creating tasks that must wait for a specific day to be executed.

## About Django

I chose to develop the application without using django rest framework for three reasons:

 - Since when asked if it should be used, it was specified that it is indistinct to use DRF or Django.
 - I had never worked with Django without using DRF, so it was a good learning option.
 - It was considered that it could be easier to test without having to use endpoints or develop a small web application that interacts with an API.

## About the creation of the application administrator user

It was left out of the scope of the challenge the creation or maintenance of system users, therefore each new user must be created using a python shell.

## About URL customization

To change the url with which slack sends the daily reminders, you must configure the `SERVER_URL` environment variable

```yaml
- SERVER_URL=http://localhost:8000
```

Inside the file [docker-compose.yml](../docker-compose.yml) in the `backend` service

---
[Back](../README.md)