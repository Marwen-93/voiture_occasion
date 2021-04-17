import re
import pandas as pd

df = pd.read_csv('/home/marwen/Desktop/voiture_occasion/voiture.csv')

car =['abarth', 'alfaromeo', 'alpine', 'artega', 'astonmartin', 'audi', 'bentley', 'bmw', 'bmwalpina', 'cadillac', 'caterham', 'chevrolet', 'chrysler', 'citroen', 'cupra', 'dacia', 'daihatsu', 'dodge', 'donkervoort', 'ds', 'ferrari', 'fiat', 'ford', 'genesis', 'honda', 'hummer', 'hyundai', 'infiniti', 'isuzu', 'jaguar', 'jeep', 'kia', 'ktm', 'lada', 'lamborghini', 'lancia', 'land rover', 'lexus', 'lotus', 'lynk co', 'maseati', 'mazda', 'mclaren', 'mercedes', 'mg', 'mia electric', 'mini', 'mitsubishi', 'nissan', 'opel', 'peugeot', 'polestar', 'porsche', 'renault', 'rollsroyce', 'saab', 'seat', 'skoda', 'smart', 'ssangyong', 'subaru', 'suzuki', 'tesla', 'toyota', 'volkswagen', 'volvo']

# drop nan

df.dropna(inplace=True)
# drop Unnamed 0 
df.drop('Unnamed: 0',axis=1,inplace=True)
# remove Prix : DT from  coloum prices
df['prices'] =df['prices'].apply(lambda x: x.replace(' ',''))
df['prices'] =df['prices'].apply(lambda x: x.split(':')[1])
df['prices']= df['prices'].apply(lambda x : x.replace('DT',''))
df['prices']= df['prices'].apply((lambda x : x.replace('25000EURO','82000')))
df['prices'] = df['prices'].astype(int)

df['prices']=df['prices'].apply(lambda x : x if x>1000 else x*1000)

# remove cv from colum CV
df['cv']=df['cv'].astype(str)
df['cv']=df['cv'].apply(lambda x: x.split(' ')[0])


# change colum date to annee_publication and "Hier" to the date of excration and keep only the month and the year
df.rename(columns={'date': 'annee_publication'}, inplace=True)
df['annee_publication']=df['annee_publication'].apply(lambda x: x.replace('Hier 0:20','26 Mars 2021'))
df['annee_publication']=df['annee_publication'].apply(lambda x: x[-4:])
df['annee_publication']=df['annee_publication'].astype(int)

# remove Km from Km cloumn
df['km']=df['km'].apply(lambda x: x.replace('Km','').replace(' ',''))
df['km'] = df['km'].astype(int)
df['km']  = df['km'].apply(lambda x : x if x>1000 else x*1000)
# change calender to mise_en_vente and keep the year only
df.rename(columns={'calender': 'mise_en_vente'}, inplace=True)
df['mise_en_vente']=df['mise_en_vente'].astype(str)
df['mise_en_vente']=df['mise_en_vente'].apply(lambda x: x[-4:])
df['mise_en_vente']=df['mise_en_vente'].astype(int)
# add age colum
df['age']= df['annee_publication']-df['mise_en_vente']


df.rename(columns={'car_names': 'description'}, inplace=True)
df['description'] = df['description'].apply(lambda x :x.lower())
df['description'] = df['description'].apply(lambda x : x.replace('citroën','citroen'))
df['description'] = df['description'].apply(lambda x : x.replace('citron','citroen'))
df['description'] = df['description'].apply(lambda x :  x.replace('smartmercedes','mercedes' ))

# add colum description_long
df['description_long'] = df['description'].apply(lambda x :len(x.split(' ')))


# get nom_voiture colum and serie_voitures
df['description'] = df['description'].apply(lambda x :x.split(' '))
def Intersection(lst1, lst2):
    return set(lst1).intersection(lst2)
df['nom_voiture']=df['description'].apply(lambda  x: set(x).intersection(set(car) ))
df['nom_voiture']=df['nom_voiture'].astype(str)
df['nom_voiture']=df['nom_voiture'].apply(lambda x: re.sub('[^a-zA-Z]+', '', x))
df['description']=df['description'].apply(lambda x :' '.join(x))
for i in range(len(df['description'])):
    try:
        df['description'][i]=df['description'][i].split(df['nom_voiture'][i])[1]
    except:
        -1
df['description']  =  df['description'].apply(lambda x :x.lstrip())

df['serie_voitures']  =  df['description'].apply(lambda x :x.split(' ')[0])

df.drop('description',axis=1,inplace=True)

data =df[df['nom_voiture']!='set']



data.to_csv('/home/marwen/Desktop/selenium/voiture_occasion/data_cars_cleaned',index=False)
