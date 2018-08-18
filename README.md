# MP-Browser

Pretty browser for MountainProject.  

MP-API_loader.py - Data loader script
the loader loads data from Mountain Project's API into DynamoDB.

Database Schema

* Users
*	Id
*	First Name
*	Last Name
*	City
*	PersonalText
*	Avatar	
Ticks
	UserId
	RouteId
	Date
Routes
	RouteId
	Name
	Rating
	Location

MP-API.py - Microservices Flask server
REST PAOI