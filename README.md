# API Documentation
* The Partner API provides endpoints for registering new partners and retrieving courses associated with a partner's token. This API facilitates user registration with specific validation and unique token generation, and it allows for the retrieval of course information. This module is designed for Odoo version 16
* ====================================================================================

# Endpoints
## 1. Register Partner
- URL: /register_partner
- Method: POST
- Authentication: None
- Content-Type: application/json

## Request (Body Parameters:)
- name (string): The name of the partner. This field is required.
- phone (string): The phone number of the partner. It must be 12 digits long and start with "966". This field is required.
- user_type (string): The type of user. It must be either "lecture" or "student". This field is required.
- date_of_birth (string): The date of birth of the partner in the format YYYY-MM-DD. This field is optional.

## 2. Get Courses
- URL: /get_courses
- Method: GET
- Authentication: None
- Content-Type: application/json

## Request
- Token (string): The unique token of the partner. This field is required.


## How to Use
- Installation
  1. Clone the repository
  2. Install the required dependencies.

- Run the Application (Start the Odoo server)


## Note
- Ensure proper setup and configuration of Odoo before running the application.



## Thanks you for reading .
