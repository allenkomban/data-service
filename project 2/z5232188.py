import ast

from sklearn.metrics import accuracy_score, mean_squared_error, precision_score, recall_score
import pandas as pd
import sys
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from scipy.stats.mstats_basic import pearsonr

def read_data(filename):
    data = pd.read_csv(filename)

    return data

def encode_and_bind(original_dataframe, feature_to_encode): # funtion to do one hot encoding and bind to dataframe
    mlb = MultiLabelBinarizer()
    encoded = pd.DataFrame(mlb.fit_transform(original_dataframe[feature_to_encode]), columns=mlb.classes_, index=original_dataframe.index)
    #dummies = pd.get_dummies(original_dataframe[feature_to_encode])
    res = pd.concat([original_dataframe, encoded], axis=1)


    return(res)

def count_top(df12, column): # funtion to count top features
    # df12 = data.copy()  # making a copy of the passed variable
    country_dict = {}  ## dicitonary to store the count of each country

    for index, row in df12.iterrows():  ### iterating through column "p_country" and each list to count each genre and store it in a dictionary
        for x in row[column]:
            if x in country_dict.keys():
                country_dict[x] = country_dict[x] + 1
            else:
                country_dict[x] = 1

    sorted_country_dict = {k: v for k, v in sorted(country_dict.items(),
                                                   key=lambda item: item[1],
                                                   reverse=True)}  # sorting dicitonary accroding to key
    sorted_names = list(sorted_country_dict.keys())  # list of keys in dicitonary

    return sorted_names


def encode_top(dataframe,sorted_names,column,top):
    for y in sorted_names[0:top]:
        dataframe[y]=dataframe[column].apply(lambda x: 1 if y in x else 0 )


    return dataframe





def pre_processing(data,drp):

    data=data.drop(['homepage','overview','status','tagline'],axis=1)
    if drp==1:
        data.drop(data[data['revenue'] < 200].index, inplace=True)
    #data['revenue'] = np.log1p(data['revenue'])


    data["cast"] = data["cast"].apply(ast.literal_eval)
    data["genres"] = data["genres"].apply(ast.literal_eval)
    data["crew"] =data["crew"].apply(ast.literal_eval)
    data["keywords"] = data["keywords"].apply(ast.literal_eval)
    data['spoken_languages']=data['spoken_languages'].apply(ast.literal_eval)
    data["production_companies"]=data['production_companies'].apply(ast.literal_eval)
    data['production_countries']=data['production_countries'].apply(ast.literal_eval)


    #count features
    #data['no_of_genres'] = data['genres'].apply(lambda x: len(x))
    data["no_of_pc"] = data['production_companies'].apply(lambda x: len(x))
    data['no_of_lan']=data['spoken_languages'].apply(lambda x: len(x))


    data['release_date'] = data['release_date'].astype('datetime64[ns]')
    data["month"] = data['release_date'].map(lambda x: x.month)
    data["year"] = data['release_date'].map(lambda x: x.year)
    #print('year min',data['year'].min())
    #print('year max', data['year'].max())
    #data['weekday'] = data['release_date'].dt.dayofweek


    #crew extraction
    data["producers"]=data["crew"].apply(lambda x: [d['name']  for d in x if d['job']=='Producer'])
    data['directors']=data["crew"].apply(lambda x: [d['name']  for d in x if d['job']=='Director'])


    data["cast"] = data['cast'].apply(lambda x: [d['name'] for d in x])
    data["genres"] = data['genres'].apply(lambda x: [d['name'] for d in x])
    data['production_countries']= data['production_countries'].apply(lambda x:[d['name'] for d in x])
    data["spoken_languages"] = data['spoken_languages'].apply(lambda x: [d['name'] for d in x])
    data["keywords"] = data['keywords'].apply(lambda x: [d['name'] for d in x])
    data["production_companies"] = data['production_companies'].apply(lambda x: [d['name'] for d in x])
    data["crew"] = data['crew'].apply(lambda x: [d['name'] for d in x])


    #print('budget type',data['budget'].dtypes)
    index = data['movie_id']


    #data.to_csv('mod_data.csv')




    #print("corr\n")
    #print(data[data.columns[1:]].corr()['revenue'][:-1])
    #print(data[data.columns].corr()['revenue'])


    return data,index







def model_regression(x,y):
    lr= RandomForestRegressor()
    lr.fit(x, y)
    return lr

def model_rating(x,y):
    knn = GradientBoostingClassifier()
    knn.fit(x, y)
    return knn



def rmsle(y_true, y_pred):

    msr = metrics.mean_squared_error(y_true, y_pred)

    return 'rmsle', msr
def normalise(data,column_name):
    df_normalized = (data[column_name] - data[column_name].min()) / (data[column_name].max() - data[column_name].min())

    df_normalized = pd.DataFrame(df_normalized)
    return df_normalized

def train_predict_split(data):  # function to splitting dataset

    y_train = data.pop('revenue')
    y_train_rat=data.pop('rating')
    #data.drop('revenue', axis=1, inplace=True)
    y_train=y_train.to_frame()


    return data, y_train,y_train_rat


pd.set_option('display.max_columns', None)
train_data=read_data(sys.argv[1])
#glimpse(data)
test_data=read_data(sys.argv[2])

train_data,index_train=pre_processing(train_data,1)

#print('index train',index_train)


top_train_cast=count_top(train_data,'cast')
#print('top cast',top_train_cast)
encode_top(train_data,top_train_cast,'cast',90)

top_train_production_companies=count_top(train_data,'production_companies')
#print('top production companies',top_train_production_companies)
encode_top(train_data,top_train_production_companies,'production_companies',5)

top_train_genres=count_top(train_data,'genres')
#print('top genres ',top_train_genres)
encode_top(train_data,top_train_genres,'genres',6)

top_train_keywords=count_top(train_data,'keywords')
#print('top keywords',top_train_genres)
encode_top(train_data,top_train_keywords,'keywords',200)

top_train_producer=count_top(train_data,'producers')
#print('top pr0ducers',top_train_producer)
encode_top(train_data,top_train_producer,'producers',10)

top_train_director=count_top(train_data,'directors')
#print('top directors',top_train_director)
encode_top(train_data,top_train_director,'directors',10)

top_train_language=count_top(train_data,'original_language')
#print('top languages',top_train_language)
encode_top(train_data,top_train_language,'original_language',5)

top_train_pc=count_top(train_data,'production_countries')
#print('top countries',top_train_pc)
encode_top(train_data,top_train_pc,'production_countries',5)



test_data,index_test=pre_processing(test_data,0)

encode_top(test_data,top_train_cast,'cast',90)
encode_top(test_data,top_train_production_companies,'production_companies',5)
encode_top(test_data,top_train_genres,'genres',6)
encode_top(test_data,top_train_keywords,'keywords',200)
encode_top(test_data,top_train_producer,'producers',10)
encode_top(test_data,top_train_director,'directors',10)
encode_top(test_data,top_train_language,'original_language',5)
encode_top(test_data,top_train_pc,'production_countries',5)

#encode_top(test_data,top_train_crew,'crew',100)



train_data=train_data.drop(['movie_id','no_of_lan','no_of_pc','year','production_countries','original_title','genres','release_date',"spoken_languages",'keywords','cast','production_companies','crew','producers','directors','original_language'],axis=1)
test_data=test_data.drop(['movie_id','no_of_lan','no_of_pc','year','production_countries','original_title','genres','release_date',"spoken_languages",'producers','directors','keywords','cast','production_companies','crew','original_language'],axis=1)
#train_data.to_csv('mod_data_joined.csv')


x_test,y_test,y_test_rat=train_predict_split(test_data)
x_train,y_train,y_train_rat=train_predict_split(train_data)


#print(sys.argv)

sc = StandardScaler()
x_train = sc.fit_transform(x_train)
x_test = sc.transform(x_test)



l_r=model_regression(x_train,y_train.values.ravel())
y_pred_test=l_r.predict(x_test)
y_pred_train=l_r.predict(x_train)


mse_test=mean_squared_error(y_test,y_pred_test)
#print("rmsle ON TEST SET",mse_test)
mse_train=mean_squared_error(y_train,y_pred_train)
#print("rmsle ON train SET",mse_train)



y_pred_test = pd.DataFrame(data=y_pred_test, columns=["revenue"])
y_pred_train = pd.DataFrame(data=y_pred_train, columns=["predicted_revenue"])
index_test=pd.DataFrame(data=index_test,columns=['movie_id'])
#y_pred_test.to_csv('y_pred.csv')
#index_test.to_csv('index_test.csv')
part1outut=pd.concat([index_test,y_pred_test],axis=1)
part1outut.set_index('movie_id',inplace=True)
part1outut.to_csv('z5232188.PART1.output.csv')






pcc, _ = pearsonr(y_pred_test,y_test)
#print('pearsonn beg test',pcc)

pcc1, _ = pearsonr(y_pred_train,y_train)
#print('pearsonn beg test',pcc1)

datapart1 = {'zid':  ['z5232188'],
        'MSR': [round(mse_test,2)],
        'correlation':[round(pcc,2)]

        }

part1summary= pd.DataFrame (datapart1, columns = ['zid','MSR','correlation'])

part1summary.set_index('zid',inplace=True)
part1summary.to_csv('z5232188.PART1.summary.csv')

knn=model_rating(x_train,y_train_rat)
y_pred_test_rat=knn.predict(x_test)
y_pred_train_rat=knn.predict(x_train)
#print(y_pred_test_rat)

y_pred_test_rat = pd.DataFrame(data=y_pred_test_rat, columns=["predicted_rating"])
part2output=pd.concat([index_test,y_pred_test_rat],axis=1)
part2output.set_index('movie_id',inplace=True)

part2output.to_csv('z5232188.PART2.output.csv')


#
# print("confusion_matrix:\n", confusion_matrix(y_test_rat, y_pred_test_rat))
# print("precision:\t", precision_score(y_test_rat, y_pred_test_rat, average='macro'))
# print("recall:\t\t", recall_score(y_test_rat, y_pred_test_rat, average='macro'))
# print("accuracy:\t", accuracy_score(y_test_rat, y_pred_test_rat))

datapart2 = {'zid':  ['z5232188'],
        'average_precision': [ round(precision_score(y_test_rat, y_pred_test_rat, average='macro'),2)],
        'average_recall':[round(recall_score(y_test_rat, y_pred_test_rat, average='macro'),2)],
        'accuracy':[round(accuracy_score(y_test_rat, y_pred_test_rat),2)]
        }

part2summary= pd.DataFrame (datapart2, columns = ['zid','average_precision','average_recall','accuracy'])
part2summary.set_index('zid',inplace=True)
part2summary.to_csv('z5232188.PART2.summary.csv')