<h1 align="center">Packford - Django Storage Facility Website</h1>

<p align="center">
  <img width="500" src="https://github.com/priyanktejani/packford-django-storage-facility-website/blob/master/documentation/logo.png">
</p>

<br>

<p align="center"> Allows clients to order and return collection of crates and items for storage.</p>
<div align="center">

</div>

<p align="center">
	<a href="https://github.com/priyanktejani/packford-django-storage-facility-website/blob/master/documentation/problem-case-study.pdf">Problam case study</a>&nbsp;&nbsp;&nbsp;
</p>

## Installation

1. Clone this repository or download as zip.

```sh
git clone https://github.com/priyanktejani/packford-django-storage-facility-website
```

2. Install required packages

```sh
$ pip install -r requirements.txt
```

3. Run the server on your local computer

```sh
$ python manage.py runserver
```

## Directory structure

    `|-- accounts                        # account app (register and login functionality)
     |    `-- forms.py                   # account app forms
     |    `-- models.py                  # account app models (database logic)
     |    `-- views.py                   # account app response logic 
     |    `-- urls.py                    # account app urls
     |
    `|-- adminpackford                   # adminpackford app (add, manage client and employee functionality)
     |    `-- models.py                  # adminpackford app models 
     |    `-- views.py                   # adminpackford app response logic 
     |    `-- urls.py                    # adminpackford app urls
     |
    `|-- carts                           # cart app (add, remove cart products functionality)
     |    `-- models.py                  # cart app models
     |    `-- views.py                   # cart app response logic 
     |    `-- urls.py                    # cart app urls  
     |
    `|-- clients                         # client app (contains clients dashboard, ordered and returned products details)
     |    `-- forms.py                   # client app forms
     |    `-- models.py                  # client app models
     |    `-- views.py                   # client app response logic 
     |    `-- urls.py                    # client app urls  
     |
    `|-- inventory                       # inventory app (contains crates and items details)
     |    `-- forms.py                   # inventory app forms
     |    `-- models.py                  # inventory app models
     |    `-- views.py                   # inventory app response logic 
     |    `-- urls.py                    # inventory app urls  
     |
    `|-- orders                          # order app (contains client order, return, shipping, and billing details)
     |    `-- models.py                  # order app models
     |    `-- views.py                   # order app response logic
     |    `-- urls.py                    # order app urls  
     |
    `|-- packford                        # packford app
     |    `-- settings.py                # packford app settings
     |    `-- views.py                   # packford app response logic 
     |    `-- urls.py                    # packford app urls
     |          
    `|-- static                          # static files 
     |    |-- admin                      # django admin static files
     |    |-- assets                     # packford app static files
     |          |-- css                  
     |          |-- images               
     |          |-- js                   
     |                
    `|-- templates                       # project templates
     |    |-- accounts              	 
     |    |-- adminpackford              
     |    |-- clients               
     |    |-- inventory                
     |    |-- orders               
     |    |-- layouts               
     |
     `-- db.sqllite3                     # database
    
  

## Database diagram

![Screenshot](https://github.com/priyanktejani/Packford-Django-Storage-Facility-Website/blob/master/documentation/project_visualized.png)

## Screenshots

<p align="center">
	<img width=49%; src="https://github.com/priyanktejani/packford-django-storage-facility-website/blob/master/documentation/screenshots/admin_dashboard.png">
	<img width=49%; src="https://github.com/priyanktejani/packford-django-storage-facility-website/blob/master/documentation/screenshots/client_dashboard.png">
</p>

## License

MIT. Copyright (c) [MIT License](./LICENSE).


## Credits

The project is made possible using [Mazer](https://zuramai.github.io/mazer/) Open-source Bootstrap 5 Admin Dashboard.
