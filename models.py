import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

data = pd.read_csv('~/Desktop/selenium/voiture_occasion/data_cars_cleaned')

data_model= data[['cv','fuel','type_seller','etat','age','nom_voiture']]


data_model['km_x1000']=data['km']/1000
data_model['prices_x1000']=data['prices']/1000



# get dummies data
data_dum = pd.get_dummies(data_model, drop_first = True)

x = data_dum.drop('prices_x1000',axis = 1)
y = data_dum.prices_x1000.values



X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)


# linear regression model 1
import statsmodels.api as sm
X_sm = sm.add_constant(X_train)
model = sm.OLS(y_train,X_sm)
sm_model = model.fit()
print(sm_model.summary())


# linear regression model 2
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score
lR = LinearRegression()
cvs_lR= cross_val_score(lR, X_train, y_train, cv=3 ,scoring='neg_mean_absolute_error')
print(cvs_lR)
print('mean mean_absolute_error',np.mean(cvs_lR))


#lasso regression 
from sklearn.linear_model import Lasso
lS= Lasso()
cvs_lS= cross_val_score(lS,X_train, y_train, cv=3 ,scoring='neg_mean_absolute_error')
print(cvs_lS)
print('mean mean_absolute_error Lasso',np.mean(cvs_lS))


# Lasso tunnig alpha 
alpha=[]
erro=[]

for i in range(1,100):
    alpha.append(i/100)
    ls=Lasso(alpha=(i/100))
    cvs_ls= cross_val_score(ls,X_train, y_train, cv=3 ,scoring='neg_mean_absolute_error')
    erro.append(np.mean(cvs_ls))
plt.plot(alpha,erro)
err =tuple(zip(alpha,erro))
df_err = pd.DataFrame(err ,columns=['alpha','error'])
df_err[df_err.error==max(df_err.error)]

# Random Forest Regressor model
from sklearn.ensemble import RandomForestRegressor

rF = RandomForestRegressor()

cvs_rF= cross_val_score(rF,X_train, y_train, cv=3 ,scoring='neg_mean_absolute_error')

print(cvs_rF)
print('mean mean_absolute_error RandomForestRegressor',np.mean(cvs_rF))


# Gradient Boosting Regressor model

from sklearn.ensemble import GradientBoostingRegressor
gB = GradientBoostingRegressor()
cvs_gB= cross_val_score(gB,X_train, y_train, cv=3 ,scoring='neg_mean_absolute_error')
print(cvs_gB)
print('mean mean_absolute_error RandomForestRegressor',np.mean(cvs_gB))



# grid search for Random Forest Regressor model

from sklearn.model_selection import GridSearchCV
rFR = RandomForestRegressor(random_state=42)
param_grid = { 'n_estimators':range(200,300,10),'max_features': ['auto', 'sqrt', 'log2'],'max_depth' : [4,5,6,7,8],'criterion' :['mse', 'mae']}
CV_rfc = GridSearchCV(estimator=rFR, param_grid=param_grid, cv= 5)
CV_rfc.fit(X_train, y_train)

CV_rfc.best_score_
CV_rfc.best_estimator_ 

# grid search for Gradient Boosting Regressor model
parameters = {'learning_rate': [0.01,0.02,0.03,0.04]
              ,'subsample'    : [0.9, 0.5, 0.2, 0.1],
              'n_estimators' : [100,500,1000, 1500],
              'max_depth'    : [4,6,8,10]
              }
grid_gB = GridSearchCV(estimator=gB, param_grid = parameters, cv = 2, n_jobs=-1)
grid_gB.fit(X_train, y_train)

grid_gB.best_estimator_ 


# best estimator
rF=RandomForestRegressor(max_depth=8, n_estimators=210, random_state=42)
rF.fit(X_train, y_train)

gB=GradientBoostingRegressor(learning_rate=0.04, max_depth=4, n_estimators=1500,subsample=0.9)
gB.fit(X_train, y_train)
predict_gB= grid_gB.best_estimator_.predict(X_test)
predict_rFR =rF.predict(X_test)

from sklearn.metrics import mean_absolute_error


mean_absolute_error(y_test,predict_gB)
mean_absolute_error(y_test,predict_rFR)


import pickle as pl
pickl = {'model':grid_gB.best_estimator_ }
pl.dump(pickl, open('model_file'+".p","wb"))

file_name ='model_file.p'
with open(file_name,'rb') as pickled:
    data= pl.load(pickled)
    model = data['model']

X_test.iloc[1:].values

model.predict(X_test.iloc[1,:].values.reshape(1,-1))
