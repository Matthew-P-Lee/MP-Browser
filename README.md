# MP-Browser

Prettied-up browser for MountainProject.  The goal of the project is to create an attractive
 single page climber's resume with the ability to apply different styles.   
 
I use this project to play with Python, Flask, Javascript, HTML/CSS and AWS.  If you find it useful,
we'd both be surprised!

## Database Schema

* Users
    * Id
    * First Name 
    * Last Name
    * City
    * PersonalText
    * Avatar	
* Ticks
    * UserId
    * RouteId
    * Date
* Routes
    * RouteId
    * Name
    * Rating
    * Location

## MPAPI_server.py - Microservices Flask server
RESTful API allows for the retrieval of routes, ticks and user profile data.

## MPAPI_classes.py - Common classes
Handles common data access to DynamoDB

## MPAPI_loader.py - Data loader script
the loader loads data from Mountain Project's API into DynamoDB.

## MPAPI_tests.py - Unit tests for MPAPI_classses
Tests the MPAPI classes using 'unittest'