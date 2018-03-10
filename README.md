# graphmydata
This project builds a RESTful web service using Django allowing various statistical randomization designs including:
1. Complete randomization
2. Stratified complete randomization
3. Block randomization 
4. Stratified block randomization
5. Minimization randomization

The core computation is performed with R and result sent back to Django for web serving using RServe.  

# Install dependencies
1. Python related modules   
cd djangoR/src  
pip install -r requirements.txt  
pip install djangorestframework  
pip install markdown       # Markdown support for the browsable API.  
pip install django-filter  # Filtering support  

2. R related packages  
Within R Console, type:  
install.packages(c('Rserve', 'randomizeR', 'foreach', 'stringr'))  
install.packages("SRS", repos="http://R-Forge.R-project.org")  

# Start server  
1. start R server  
library(Rserve)  
Rserve(port=6000)  

2. Start the django web server  
cd djangoR/src  
python manage.py makemigrations  
python manage.py runserver  

# REST API call
The web service allow programming access using post request. One can also access the service with a browser using plugins such as chrome Advanced REST client. For example,  

Open browser for the following URL for test  
1. test by generating rnorm(30): http://127.0.0.1:8000/randomization/test?N=30  
2. Use Post method. For this, we recommend to install plugins, e.g. chrome Advanced REST client.  
An screenshot of using the Advanced REST client for complete randomization request is as following.   
<img src="https://github.com/nickytong/graphmydata/blob/master/djangoR/src/randomization/assets/REST%20API%20using%20chrome%20Advanced%20REST%20extension.png" align="center" height="400" width="600" hspace="30"/>

