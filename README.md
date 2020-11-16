# Modec 2XS Test

## Technologies
* Django & Django-rest Framework
* Python 3.8.5
* MySQL
* Docker & Docker-Compose

## How to Run
To run this application you will need to first, create a `.env` file from the `.env.example`
Run the following commands to build and start the application using docker
```sh
$ make docker-build
$ make docker-start
$ make docker-migrate
```
The application should start on port `8080`.

If `docker-migrate` failed to connect to MySQL, wait a couple of seconds (in order for the MySQL container to start) and try it again

## Endopoints & How to use.

|Endpoint|Method|Action|
| ------ | ------ |------ |
|/vessels/|GET| List all vessels|
|/vessels/|POST| Create vessel|
|/vessels/{vessel_code}/equipments/|GET|List all active equipments from vessel
|/vessels/{vessel_code}/equipments/|POST|Create equipment for vessel
|equipments/deactivate/|PATCH| Deactivate a list of equipments

## Choices and strategies

In this section I will describe the technologies used in the project and the reasons why I chose them.

### Django & Django REST

As specified in the email, Python was mandatory.
For that reason I chose Django. A framework with good documentation, community market adhesion even though I had never worked with it I was confident that it would be a safe and effective choice.
After little research I found the Django Rest Framework. It is a powerful and flexible toolkit for building Web APIs and given the test's requirements seemed like a perfect fit.

I chose a stable yet recent Python version that met all Django's requirements

### MySQL Database

The database was a clear choice after having read the test's requirements. All entities and relations were well defined without much intricacies. Other factors that weighted my decision was the built-in Django ORM and my familiarity with this database.

### Docker & Server 

Docker is my go to technology for my local development.
At first I was focused on creating a structure that could have been easily deployed, with different environments and pipelines. But this approach was taking too much time so I gave up as this was not required by the test.


### Modelling

As described by the test's requirements there is a clear one-to-many relationship between the `vessel` entitie the `equipment` entitie. This is easily implemented using Django. Clear business rules were given for the `code` propertie of each entitie but not the other ones, and for that reason I chose to use the given example as basic rules for each field.  

In spite of the downsides of using a string as primary-key, I took this aproach for the `vessel` entitie in order to speed up development and prevent multiple queries later on to make a more "readable" urls.

### Resources
 
Most of the heavy-lifting here were done by the Django and Django Rest Framework.
Because of the relationship between `vessel` and `equipment` it made sense to me to expose most of the `equipment` resources under `vessel`. 

Most of the resources were implemented with this in mind. 
I got a bit confused by the third requirement. `3 – Setting an equipment’s status to inactive. The input data should be one or a list of equipment code.`
I chose to make a resource that receives a list of codes and therefore can receive a list with only one item. It made no sense to me creating a different resource to handle a single code even though this is what I undertood from this requirement...
 
 ### Testing

 Because persistence is handled by the framework it made little to no sense creating unit tests to ensure the ORM behaviour.

 Therefore, I focused on unit tests that were capable of assuring the models behaviour and its porperties and acceptance tests for the resources.


 ### Final notes
 I had quite a bit of fun with this little project. It is quite simple and yet it made me study most of what the framework I chose to work on had to offer. Django really have a unique project structure and I found it quite interesting.

 This project could benefit from some improvements like a CI/CD, better input validation, logging and  more tests, because there is no such thing as too many tests.



