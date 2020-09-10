from flask import Flask
from flask_restplus import Resource, Api
from flask_restplus import reqparse
import sqlite3
import json
import ast
import uuid
import requests
from datetime import datetime

API_KEY="AIzaSyD6-khCY5wCvJbq0JYCIyw75gfxTtgHt_o"

app = Flask(__name__)
api = Api(app, title="World Bank", description="API for World Bank Economic Indicators.")



def check_db(dbname,indicator):  # function to check if indicator exits in databse
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    c.execute("Select * from COLLECT where indicator_name = ? ",(indicator,) )
    tempvar = c.fetchall()
    rowcount = len(tempvar)
    #print("count from function",rowcount)
    conn.commit()
    conn.close()
    return rowcount

def check_db_id(dbname,id): #check data with id exists in db
    conn = sqlite3.connect(dbname)
    c = conn.cursor()

    c.execute("Select * from COLLECT where collection_id = ? ", (id,))
    tempvar = c.fetchall()
    rowcount = len(tempvar)
    #print("count from function", rowcount)

    conn.commit()
    conn.close()
    return rowcount


def create_db(filename):  # function creates db

    conn = sqlite3.connect(filename)
    c = conn.cursor()
    c.execute("CREATE TABLE if not exists COLLECT (collection_id text,uri text,indicator_name text,creation_time text,entries text)")
    conn.commit()
    conn.close()


def insert_db(dbname,cleaned_data): # function inserts data into db
    conn = sqlite3.connect(dbname)
    c = conn.cursor()

    c.execute("INSERT INTO COLLECT VALUES (?,?,?,?,?)",
              [cleaned_data["id"], cleaned_data["uri"], cleaned_data["indicator_id"], cleaned_data['creation_time'],json.dumps(cleaned_data["data"])])
    conn.commit()
    conn.close()

def delete_db(dbname,collection_id):  # function delete data into db
    conn=sqlite3.connect(dbname)
    collection_id=str(collection_id)
    c=conn.cursor()
    c.execute("DELETE FROM COLLECT WHERE collection_id = ? ",(collection_id,))
    conn.commit()
    conn.close()


#def check_table(dbname,collection_id):



def clean_data(data): # clean the data from our source

    cleaned = []
    for x in data:
        if x['value'] == None:
            pass
        else:
            x['indicator_value'] = x['indicator']['value']
            x['indicator']=x['indicator']['id']
            x['country']=x['country']['value']
            cleaned.append(x)

    total_cleaned={}
    unique=str(uuid.uuid1())

    #print("cleaned;",cleaned)
    total_cleaned['indicator_id']=cleaned[0]['indicator']
    total_cleaned['creation_time']=str(datetime.now())
    total_cleaned['id']=unique
    total_cleaned["uri"]="/collection/"+unique
    total_cleaned['data']=cleaned


    return total_cleaned


def get_data(indicator):  # get the data from url
    url = "http://api.worldbank.org/v2/countries/all/indicators/{}?date=2013:2018&format=json&per_page=1000".format(indicator)
    isbn_url_book="https://api2.isbndb.com/book/9781934759486?with_prices=1"
    h={'Authorization': '44183_b1efe24c13bed43cb8dcad3abd974e73'}
    google_url_book="https://www.googleapis.com/books/v1/volumes?q=isbn:9780743477123&key={}".format(API_KEY)
    #print("url\n",url)
    response = requests.get(isbn_url_book,headers=h)
    #print("response,",response)
    data = response.text
    print("data:",data)

    parsed = json.loads(data)
    print("parsed",parsed)
    print("parsed['book']['image']:", parsed['book']['image'])
    print("length of parsed",len(parsed))
    print("length of pased book",len(parsed["book"]))
    if len(parsed)==1:
        return -1
    #print("parsed[0]",parsed[0])
    #print("parsed[1]",parsed[1])
    #print(len(parsed[1]))

    print("cleaned data:",cleaned)
    #print("cleaned",cleaned)
    #print("len cleaned",len(cleaned))

    return cleaned


parser_q1 = reqparse.RequestParser()
parser_q1.add_argument('indicator_id',required=True)

@api.route('/collection')
class collection(Resource):
    @api.response(201, 'Collection Created Successfully')
    @api.response(200, 'Collection exist')
    @api.response(404, 'Collection does not exists')
    @api.doc(description="Add a new Collection")
    @api.expect(parser_q1, validate=True)
    def post(self):

        args = parser_q1.parse_args()
        indicator_id = args.get('indicator_id')

        count = check_db('z5232188.db', indicator_id)
        if count > 0:  # if data already exist

            return {"message": f"the indicator id {indicator_id} already exist in our datatable!"}, 200




        pure_data=get_data(indicator_id)

        if pure_data==-1:  #if the indicator enterred is invalid
            return {"message": f"the indicator id {indicator_id} doesn't exist in the data source!"}, 404
        insert_db("z5232188.db", pure_data)

        return {
            "indicator_id": pure_data['indicator_id'],
            "uri": pure_data["uri"],
            "id":pure_data["id"] ,
            "creation_time": pure_data['creation_time']},201


    def get(self):
        conn = sqlite3.connect('z5232188.db')
        c = conn.cursor()
        c.execute('SELECT * from COLLECT  ')
        table = c.fetchall()
        conn.close()
       # print("table-content",table)
        list=[]
        for x in table:
            #print("x",x)
            dict={}
            dict["uri"]=x[1]
            dict["id"]=x[0]
            dict["creation_time"]=x[3]
            dict["indicator"]=x[2]
            list.append(dict)

        return list


@api.route('/collection/<string:collection_id>')
@api.response(200, 'OK')
@api.response(404, 'Not Found')
class delete_get(Resource):

    def delete(self,collection_id):
        #print("format of collection id",collection_id.format)

        count=check_db_id("z5232188.db",collection_id)
        if count==0:
            return {"message":" No collection with the input id exists"},404

        delete_db("z5232188.db",collection_id)

        return {"message": "Collection = {} is removed from the database!".format(collection_id),"id":"{}".format(collection_id)},200

    def get(self,collection_id):
        conn = sqlite3.connect('z5232188.db')
        c = conn.cursor()
        c.execute("SELECT * FROM COLLECT WHERE collection_id = ? ",(collection_id,))
        table = c.fetchall()
        conn.close()
        dict={}
        count = check_db_id("z5232188.db", collection_id)
        if count == 0:
            return {"message": " No collection with the input id exists"}, 404

        entries_list=[]
        for x in table:
            list_of_data = ast.literal_eval(x[4])

            dict['id']=x[0]
            dict['indicator']=x[2]
            dict['indicator_value']=list_of_data[0]['indicator_value']
            dict['creation_time']=x[3]
            for t in list_of_data:
                entries_dict={}
                entries_dict['country']=t["country"]
                entries_dict['date']=t['date']
                entries_dict['value']=t['value']
                entries_list.append(entries_dict)

        dict['entries']=entries_list

        return dict,200



@api.route('/collection/<string:collection_id>/<string:year>/<string:country>')
class id_year_country(Resource):
    @api.response(200, 'Collection Retrived')
    @api.response(404, 'Collection does not exists in database')
    @api.response(400, "wrong input for year or country,check again")
    @api.doc(description='Retrieve economic indicator value for given country and a year')

    def get(self, collection_id,year,country):
        conn = sqlite3.connect('z5232188.db')
        c = conn.cursor()
        c.execute("SELECT * FROM COLLECT WHERE collection_id = ? ", (collection_id,))
        table = c.fetchall()
        conn.close()
        flag=1
        dict={}
        dict['id']=collection_id

        count = check_db_id("z5232188.db", collection_id)
        if count == 0:
            return {"message": " No collection with the input id exists"}, 404

        for x in table:
            list_of_data = ast.literal_eval(x[4])
            dict['indicator'] = x[2]

            for t in list_of_data:
                if( str(t['date'])==str(year) ):

                    if(str(t['country'])==str(country) ):
                        dict['country']=country
                        dict['year']=year
                        dict['value']=t['value']
                        flag=0
        if flag==1:
            return {"message": " wrong input for year or country,check again"}, 400


        #print(dict)

        return dict,200



parser = reqparse.RequestParser()
parser.add_argument('q',type=int)
@api.route('/collection/<string:collection_id>/<string:year>')
class question_6(Resource):
    @api.response(200, 'Retrieve Collection Successfully')
    @api.response(404, 'Collection not existed in the Dataset')
    @api.response(400, 'Wrong input')
    @api.doc(description="Retrieve a Top/Bottom Collection by year")

    @api.expect( parser )
    def get(self,collection_id,year):
        #print("collection id nd year",collection_id,year,)
        args = parser.parse_args()
        q = args.get('q')
        conn = sqlite3.connect('z5232188.db')
        c = conn.cursor()
        c.execute("SELECT * FROM COLLECT WHERE collection_id = ? ", (collection_id,))
        table = c.fetchall()
        conn.close()
        flag=0
        dict = {}
        dict['id'] = collection_id
        entries_list=[]
        count = check_db_id("z5232188.db", collection_id)
        if count == 0:
            return {"message": " No collection with the input id exists"}, 404

        for x in table:
            list_of_data = ast.literal_eval(x[4])
            dict['indicator'] = x[2]
            dict['indicator_value']=list_of_data[0]['indicator_value']
           # print("list of data:",list_of_data)

            for t in list_of_data:

                if t['date']==year:
                    flag=1

                    entries_dict = {}

                    entries_dict['country'] = t["country"]
                    entries_dict['value'] = t['value']
                    entries_list.append(entries_dict)

        if flag==0:
            return {"message": " wrong input for year or country,check again"}, 400



        newlist = sorted(entries_list, key=lambda k: k['value'],reverse=True)
        length=len(newlist)
        #print(length)
       # print("q",q)

        if q==None:
            dict['entries']=newlist

        elif q >0:
            new_list_filtered=newlist[0:q]
            dict['entries']=new_list_filtered
        else:

            new_list_filtered=newlist[length-1+q:length-1]
            dict['entries'] = new_list_filtered


        return dict,200




if __name__ == '__main__':
    create_db("z5232188.db")


    app.run(debug=True)



