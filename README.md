### Final Project
A student connect app in **Django** that can be used to respond to incoming questions sent by customers.

### How to get Started?

#### Setup
- Install Python3 ( Instructions [here](https://docs.python-guide.org/starting/installation/) )
- Clone this repository and navigate to top-level directory
- Activate the venv 
- Install all required packages.
    ```
    python3 -m pip install -r requirements.txt
    ```
- To create an account in admin by running
    ```
    python3 manage.py createsuperuser
    ```
- Run the app
    ```
    python3 manage.py runserver
    ```
- Navigate to http://127.0.0.1:8000/ to see the campus connect website
- Navigate to http://127.0.0.1:8000/admin to see the administration interface

#### Working of the app
###### Student Connect Interface
- Student can register and login and also share their their posts.
- Student can follow another student and aslo like each other posts.
- Student can see followers and followings.


###### Agent Interface
<li>In the Admin interface, login using the agent credentials</li>


#### Features Implemented
- Form based interface for students to post.
