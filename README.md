<h1 align="center">Theatre Booking App </h1>
<br>
<h6 align="center">

[![CodeFactor](https://www.codefactor.io/repository/github/akshat2602/theatre-booking-app/badge)](https://www.codefactor.io/repository/github/akshat2602/theatre-booking-app) 
![Django Test and Build](https://github.com/akshat2602/theatre-booking-app/workflows/Django%20Test%20and%20Build/badge.svg)

</h6>


## FOSSEE details :

#### Email : [akshatsharma2602@gmail.com](mailto:akshatsharma2602@gmail.com)
#### Linkedin : [https://www.linkedin.com/in/akshat-sharma-2602/](https://www.linkedin.com/in/akshat-sharma-2602/)
#### Github : [https://github.com/akshat2602](https://github.com/akshat2602)    


## About the project :
This project is a simple server that manages Theatre occupancy. It is built using Python and Django alongside Django REST Framework. Apart from this no other libraries or databases have been used.
You are building an application for a new theatre in town. The backend application is supposed to be used by users in the theatre to gauge and manage occupancy. The theatre is a new Arena theatre for live performances and does not assign fixed seating number assignments to its patrons. 3 API endpoints have been developed as mentioned below:

### Occupy a seat -[Endpoint URL - /occupy/ ] 
The Endpoint will be given the person's name and ticket ID (this should be a UUID field, tickets will not contain information about the seat number beforehand) as input and outputs the seat number which will be occupied. If the seating is full, the appropriate error message is returned.

### Vacate a seat - [Endpoint URL - /vacate/ ]: 
This Endpoint takes the seat number which the person will be vacating and frees that slot up to be used by other people.

### Get Person/Seat information - [Endpoint URL - /get_info/<NAME or SEATNUM or TICKETID> ]: 
This Endpoint can take either the seat number or person’s name or ticket ID for the input and returns the person’s name, ticket ID, and slot number.

### Get number of empty seats - [Endpoint URL - /get_empty_seats/ ]:
This Endpoint doesn't take any data and returns the number of empty seats in the theatre. 

## Start Server Locally :
* ### Docker Image - 
   **Make sure you have docker installed. If not, refer: https://docs.docker.com/install/** \
   `docker-compose build app` \
   `docker-compose up app`
* ### Download code and run - 
    **1. [Download](https://github.com/akshat2602/theatre-booking-app/archive/master.zip) and extract the zip of Project and cd inside**\
    **OR** \
    `git clone https://github.com/akshat2602/theatre-booking-app.git` \
    `cd theatre-booking-app` \
    **2.** `sudo pip3 install virtualenv`  **OR**  `sudo pip install virtualenv`\
    **3.** `virtualenv venv`\
    **4.** `source venv/bin/activate`\
    **5.** `cd src`\
    **6.** `pip install -r requirements.txt`\
    **7. Run Tests -** `python manage.py test`\
    **8. Run Server -** `python manage.py runserver`


## Highlights of the Project :
* PEP-8 Coding guidelines followed
* Docker used to containerize the project
* Used Django Server for backend
* Added several tests for the Django project
* API Endpoints created for seat booking, vacating a seat and getting info related to a booked seat
* Used Swagger for API Documentation 


## Details of the project :
 * Project can be used by the theatre authorities to book a seat.
 * Project can be used by the theatre authorities to vacate a seat.
 * Project can be used by the theatre authorities to get details of a booking.
 * The number of seats available in the theatre can be configured using the .env file.
 * No database usage is allowed, hence, all the information regarding a ticket is stored in a dictionary which is initialized as soon as the server starts.
 * Apart from the specified endpoints in the task description another endpoint is added to show number of empty seats in the theatre.
 * API documentation has been implemented on the endpoint `localhost:8000/swagger/`
