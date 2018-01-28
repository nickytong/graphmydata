# graphmydata

# Installation
1. Python related modules   
cd djangoR/src  
pip install -r requirements.txt  

pip install djangorestframework  
pip install markdown       # Markdown support for the browsable API.  
pip install django-filter  # Filtering support  

2. Rserve, within R Console, type:  
install.packages(c('Rserve', 'randomizeR', 'foreach', 'stringr'))  
install.packages("SRS", repos="http://R-Forge.R-project.org")  

# Start server  
1. start Rserver  

library(Rserve)  
Rserve(port=6000)  

# Start the server  
cd djangoR/src  
python manage.py makemigrations  
python manage.py runserver  

# REST API call
Open browser for the following URL for test  
1. test by generating rnorm(30): http://127.0.0.1:8000/randomization/test?N=30  
2. Use Post method. For this, we recommend to install plugins, e.g. chrome Advanced REST client.  
An screenshot of using the Advanced REST client for complete randomization request is as following.   
<img src="https://raw.githubusercontent.com/nickytong/drexplorer/master/inst/doc/new.jpg" align="center" height="500" width="800"/>