
# Railway Management System


This Django based railway management system is my bachelor's degree thesis. It has the following functionalities:

   * #### Book a ticket  
   * #### Register and log in users  
   * #### See live schedule for particular station

The system is build using **Django 4**, **Python 3.10**, **Bootstrap 5** with **Bootswatch** theme and **HTML 5**. Depending on the user's role, users have different available functionalities that they can use.  

![image](https://github.com/YordanovaT/RailwayManagementSystem/assets/109622871/0263ca54-33de-4faa-9079-df16e18abea5)

## Table of contents
*  [Installation](#Installation)  
* [Running the application](#Running the application)  
* [View the application](#View the application)

### [Installation](#Installation) 

**1. Create virtual environment**  
*From the **root** directory run:*

      python -m venv venv  

**2. Activate the environment**  
*On MacOS:* 

    source venv/bin/activate
*On Windows :*  

    venv\scripts\activate

**3. Install required dependencies**  
*From the **root** directory run:* 

    pip install -r requirements.txt

**4. Run migrations**  
*From the **root** directory run:*  

    python manage.py makemigrations

*Then run:*  

    python manage.py migrate

**5. Create Django admin user in order to have access to the Django Admin Panel:**  
*From the **root** directory run:*  

    python manage.py createsuperuser

*When prompted, enter an email, first and last name, mobile and password.*  

### [Running the application](#Running the application)  

*From the **root** directory run:*  

    python manage.py runserver

### [View the application](#View the application)  

*Go to [http://127.0.0.1:8000/](http://127.0.0.1:8000/)*