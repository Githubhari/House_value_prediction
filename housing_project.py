#importing th header files that we wanted

from numpy import array_equal
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.base import BaseEstimator,TransformerMixin
from numpy import c_
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestRegressor
import joblib
from pandas import *
import mysql.connector
import webbrowser
from time import sleep
import sys
import os
import socket

os.system("start c:\\xampp\\xampp_start.exe")
#sleep(3)
#os.system("start c:\\xampp\\xampp_stop.exe")

webbrowser.open('C:/xampp/htdocs/mainpage.html')

#all class and pipeline areas
rooms_ix,bedrooms_ix,population_ix,households_ix=3,4,5,6
class CombiniAtrrib(BaseEstimator,TransformerMixin):
    def __init__(self,bedrooms_per_room=True):
        self.bedrooms_per_room=bedrooms_per_room
    def fit(self,X,y=None):
        return self
    def transform(self,X):
        rooms_per_household=X[:,rooms_ix]/X[:,households_ix]
        population_per_household=X[:,population_ix]/X[:,households_ix]
        if self.bedrooms_per_room:
            bedrooms_per_room=X[:,bedrooms_ix]/X[:,rooms_ix]
            return c_[X,rooms_per_household,population_per_household,bedrooms_per_room]
        else:
            return c_[X,rooms_per_household,population_per_household]



#reading data

from pandas import *
housing_data=read_csv("F:\programming book\handson-ml2-master\datasets\housing\housing1.csv")


#this will cut the median_income into five categories and labels them all as [1,2,3,4,5]
housing_data["income_cat"]=cut(housing_data["median_income"],bins=[0.,1.5,3.0,4.5,6.,16],labels=[1,2,3,4,5])


split=StratifiedShuffleSplit(n_splits=1,test_size=0.2,random_state=42)
for train_index,test_index in split.split(housing_data,housing_data["income_cat"]):
    train_set=housing_data.iloc[train_index]
    test_set=housing_data.iloc[test_index]

#droping the income_cat

for i in (train_set,test_set):
    i.drop("income_cat",axis=1,inplace=True)

housing=train_set.drop("median_house_value",axis=1)
housing_label=train_set["median_house_value"].copy()


imputer=SimpleImputer(strategy="median")
housing_num=housing.drop("ocean_proximity",axis=1)


num_pipline=Pipeline([
    ("imputer",SimpleImputer(strategy="median"))
    ,("add_attrib",CombiniAtrrib()),
    ("std_scaler",StandardScaler())
])

num_attribs=list(housing_num)
cat_attrib=["ocean_proximity"]

transform=ColumnTransformer([
    ("num",num_pipline,num_attribs),
    ("cat",OneHotEncoder(),cat_attrib)
])

housing_pre=transform.fit_transform(housing)

"""params=[{"n_estimators":[100],"max_features":[8]}]
fores_reg2=RandomForestRegressor()
grid_search=grid_search=GridSearchCV(fores_reg2,params,cv=5,scoring="neg_mean_squared_error",return_train_score=True)
grid_search.fit(housing_pre,housing_label)"""


#model=grid_search.best_estimator_

model=joblib.load("C:\\Users\\komma\\second_model.pkl")

X_test=test_set.drop("median_house_value",axis=1)
Y_test=test_set["median_house_value"].copy()
X_test_pre=transform.fit_transform(X_test)
#print(model.score(X_test_pre,Y_test))

"""os.system("start c:\\xampp\\xampp_start.exe")
sleep(3)
os.system("start c:\\xampp\\xampp_stop.exe")"""

#connecting to the sql
try:
    con = mysql.connector.connect(
      host="localhost", user="root",
      password="", database="Projects")
    print(con)
    cursor = con.cursor()
    cursor.execute("select * from housing order by id desc limit 1")
    last_row=cursor.fetchall()
    id=last_row[0][0]
    cursor.close()
    con.close()
except:
    sys.exit()
    

while last_row[0][0]==id:
    #os.system("start c:\\xampp\\xampp_stop.exe")
    try:
        con = mysql.connector.connect(
          host="localhost", user="root",
          password="", database="Projects")
        cursor = con.cursor()
        cursor.execute("select * from housing order by id desc limit 1")
        last_row=cursor.fetchall()
        cursor.close()
        con.close()
    except mysql.connector.errors.OperationalError as e:
        print("hello")
        sys.exit()
    except (mysql.connector.errors.InterfaceError) as e:
        if e=="2003: Can't connect to MySQL server on 'localhost:3306' (10061 No connection could be made because the target machine actively refused it)":
            #con.close()
            print("hello")
            sys.exit()
        elif e=="Lost connection to MySQL server at 'localhost:3306', system error: 10054 An existing connection was forcibly closed by the remote host":
            print("hello")
            sys.exit()
        else:
            con.close()
            sleep(2.4)
    #print(last_row)
print(last_row)
a=list(last_row[0])
a.pop(0)
cats=['<1H OCEAN','INLAND','ISLAND','NEAR BAY','NEAR OCEAN']
by=a[-1]
cat=[]
for i in cats:
    if by==i:
        cat.append(1)
    else:
        cat.append(0)
rooms_per_households=a[3]/a[6]
population_per_households=a[5]/a[6]
bedrooms_per_room=a[4]/a[3]
extra=[rooms_per_households,population_per_households,bedrooms_per_room]+cat
a.pop()
a=a+extra
#print(a)

try:
    con = mysql.connector.connect(
      host="localhost", user="root",
      password="", database="Projects")
    cursor = con.cursor()
    st=str(model.predict([a])[0])
    st="insert into housing_results(Results) values("+st+")"
    cursor.execute(st)
    con.commit()
    cursor.close()
    con.close()
except:
    sys.exit()
finally:
    con.close()




"""
INSERT into housing(Longitude,Latitude,Housing_median_age,Total_rooms,Total_rooms,Population,Households,Median_income,Ocean_proximity) VALUES(-122.23,37.88,41,880,129,322,126,8.3252,'NEAR BAY');"""