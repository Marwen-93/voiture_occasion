# used-car-price-Tunisia-prediction
-Sreate a model that can estimate price of second hand car based on some information 
-Scrap more than 4000 car data from automobile Tunisian website for a second-hand car using python and selenium
-Clean the data and extract car name and model from the description
-Optimize different model and find best parameter using grid search cv
## Create web scraper using selenium
--using python and selenium i create web scraper to extract different data and save it in voiture.csv:
prices: car price en TND.<br>
car_names:the name field with description.<br>
cv:FISCAL POWER.<br>
fuel:fiscal power of a car.<br>
trasmission:type of transmission.<br>
date:date of publication on the website.<br>
location:the location of the owner.<br>
type_seller: private or professional.<br>
km:distance in Kilometer.<br>
calender:the release day.<br>
etat:condition of the car.<br>
## Clean the data
most of the columns mixed with unnecessary strings, the field of name cars turn out that website used as description also so I export the name of the car and her series from the description and renamed the field in a more proper way
the shape of the data changed from (4957, 12) to  (3010, 14)<br>

**before cleaning **<br>

![befor cleaning](https://github.com/Marwen-93/used-car-price-Tunisia-prediction/blob/main/voiture.png)<br>

**after cleaning<br>

![after cleaning](https://github.com/Marwen-93/used-car-price-Tunisia-prediction/blob/main/data_leaned.png)<br>


![fuel](https://github.com/Marwen-93/voiture_occasion/blob/master/photo/fuel.png)<br>


![fuel](https://github.com/Marwen-93/voiture_occasion/blob/master/photo/fuel.png)<br>
