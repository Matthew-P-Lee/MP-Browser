# MP-Browser

Prettied-up browser for MountainProject.  The goal of the project is to create a climber's 
resume with different styles.   I use this project to play with Python, Flask, Javascript and AWS.

## Database Schema

* Users
    Id
    First Name 
    Last Name
    City
    PersonalText
    Avatar	
* Ticks
    UserId
    RouteId
    Date
* Routes
    RouteId
    Name
    Rating
    Location

## MP-API_server.py - Microservices Flask server
REST API allows for the retrieval of routes, ticks and user profile data.

## MP-API_classes.py - Common classes
Handles common data access to DynamoDB

## MP-API_loader.py - Data loader script
the loader loads data from Mountain Project's API into DynamoDB.