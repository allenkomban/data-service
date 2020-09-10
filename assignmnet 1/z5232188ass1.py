import ast
import json
import matplotlib.pyplot as plt
import pandas as pd
import sys
import os
import matplotlib.cm as cm

studentid = os.path.basename(sys.modules[__name__].__file__)


#################################################
# Your personal methods can be here ...
#################################################


def log(question, output_df, other):
    print("--------------- {}----------------".format(question))
    if other is not None:
        print(question, other)
    if output_df is not None:
        print(output_df.head(5).to_string())


def question_1(movies, credits):
    """
    :param movies: the path for the movie.csv file
    :param credits: the path for the credits.csv file
    :return: df1
            Data Type: Dataframe
            Please read the assignment specs to know how to create the output dataframe
    """

    #################################################
    # Your code goes here ...

    data1=pd.read_csv(movies)  ##reading the csv movie file
    data2=pd.read_csv(credits)  ##reading credits csv file
    df1=data1.merge(data2,on = 'id')   ## merging the two panda dataframes



    #################################################

    log("QUESTION 1", output_df=df1, other=df1.shape)
    return df1


def question_2(df1):
    """
    :param df1: the dataframe created in question 1
    :return: df2
            Data Type: Dataframe
            Please read the assignment specs to know how to create the output dataframe
    """

    #################################################
    # Your code goes here ...
    df2=df1.copy()    # making a copy of passed dataframe
    df2 = df2.filter([ 'id', 'title', 'popularity', 'cast', 'crew', 'budget', 'genres', 'original_language', 'production_companies', 'production_countries', 'release_date', 'revenue', 'runtime', 'spoken_languages', 'vote_average', 'vote_count'] )

    #################################################

    log("QUESTION 2", output_df=df2, other=(len(df2.columns), sorted(df2.columns)))
    return df2


def question_3(df2):
    """
    :param df2: the dataframe created in question 2
    :return: df3
            Data Type: Dataframe
            Please read the assignment specs to know how to create the output dataframe
    """

    #################################################
    # Your code goes here ...
    df3=df2.copy()               ## making a copy of the pandas frame

    df3=df3.set_index('id')             ## setting index to id column

    #################################################

    log("QUESTION 3", output_df=df3, other=df3.index.name)
    return df3


def question_4(df3):
    """
    :param df3: the dataframe created in question 3
    :return: df4
            Data Type: Dataframe
            Please read the assignment specs to know how to create the output dataframe
    """

    #################################################
    # Your code goes here ...
    df4=df3.copy()                         # making a copy of passed dataframe
    df4=df4.drop(df4[df4.budget==0].index)         ## dropping indexes where budget=0


    #################################################

    log("QUESTION 4", output_df=df4, other=(df4['budget'].min(), df4['budget'].max(), df4['budget'].mean()))
    return df4


def question_5(df4):
    """
    :param df4: the dataframe created in question 4
    :return: df5
            Data Type: Dataframe
            Please read the assignment specs to know how to create the output dataframe
    """

    #################################################
    # Your code goes here ...
    df5=df4.copy()                                                          # making a copy of passed dataframe
    df5["success_impact"]= (df5['revenue'] - df5['budget'])/ df5['budget']   # calculating success impact



    #################################################

    log("QUESTION 5", output_df = df5, other=(df5['success_impact'].min(), df5['success_impact'].max(), df5['success_impact'].mean()))
    return df5


def question_6(df5):
    """
    :param df5: the dataframe created in question 5
    :return: df6
            Data Type: Dataframe
            Please read the assignment specs to know how to create the output dataframe
    """

    #################################################
    # Your code goes here ...
    df6=df5.copy()   # making a copy of the passed variable

    df6["popularity"] = ((df6["popularity"] - df6["popularity"].min()) / (df6["popularity"].max() - df6["popularity"].min())) * 100   ## normalizeing the popularity


    #################################################

    log("QUESTION 6", output_df=df6, other=(df6['popularity'].min(), df6['popularity'].max(), df6['popularity'].mean()))
    return df6


def question_7(df6):
    """
    :param df6: the dataframe created in question 6
    :return: df7
            Data Type: Dataframe
            Please read the assignment specs to know how to create the output dataframe
    """

    #################################################
    # Your code goes here ...
    df7=df6.copy()                   #  making a copy of the passed variable
    df7['popularity']=df7['popularity'].astype('int16')       ##chaging the column to type int16


    #################################################

    log("QUESTION 7", output_df=df7, other=df7['popularity'].dtype)


    return df7


def question_8(df7):
    """
    :param df7: the dataframe created in question 7
    :return: df8
            Data Type: Dataframe
            Please read the assignment specs to know how to create the output dataframe
    """

    #################################################
    # Your code goes here ...
    df8=df7.copy()                        # making a copy of the passed variable
    df8["cast"]=df8["cast"].apply(ast.literal_eval)    # applying literal_eval
    df8["cast"]=df8['cast'].apply(lambda x: [d['character'] for d in x] )   # # iterating through the dicionary to make a list of  only dict['character'] elements
    df8["cast"]=df8["cast"].apply(sorted)                                 ## sorting the list
    df8["cast"] = df8['cast'].apply(lambda x: ','.join([str(elem) for elem in x]))   ## joining the list using commmas

    #################################################

    log("QUESTION 8", output_df=df8, other=df8["cast"].head(10).values)

    return df8


def question_9(df8):



    """
    :param df9: the dataframe created in question 8
    :return: movies
            Data Type: List of strings (movie titles)
            Please read the assignment specs to know how to create the output
    """

    #################################################
    # Your code goes here ...
    df9 = df8.copy()                                           #  making a copy of the passed variable
    df9["comma_count"] = df9['cast'].str.count(',')             #counting number of commas  in the column making another column
    df9 = df9.sort_values(by=['comma_count'], ascending=False)  # sorting the dataframe according to comma_count
    movies = df9["title"].tolist()                               # making a list of movies
    movies = movies[0:10]                                         #selecting the first 10 in them


    #################################################

    log("QUESTION 9", output_df=None, other=movies)
    return movies


def question_10(df8):



    """
    :param df8: the dataframe created in question 8
    :return: df10
            Data Type: Dataframe
            Please read the assignment specs to know how to create the output dataframe
    """

    #################################################
    # Your code goes here ...

    df10 = df8.copy()                                              # making a copy of the passed variable
    df10['release_date'] = pd.to_datetime(df10.release_date)        # changing the format to date type
    df10 = df10.sort_values(by=['release_date'], ascending=False)   # sorting acoording to the date

    #################################################

    log("QUESTION 10", output_df=df10, other=df10["release_date"].head(5).to_string().replace("\n", " "))
    return df10


def question_11(df10):
    """
    :param df10: the dataframe created in question 10
    :return: nothing, but saves the figure on the disk
    """

    #################################################
    # Your code goes here ...

    df11=df10.copy()                                                      # making a copy of the passed variable
    df11["genres"] = df11["genres"].apply(ast.literal_eval)                ## applying literal eval
    df11["gnr"] = df11['genres'].apply(lambda x: [d['name'] for d in x])  ##making a list of only dict['name'] from each dict
    gnrdict={}                                 ## dicitonary to store the count of each genres

    for index, row in df11.iterrows():           ### iterating through column gnr and each list to count each genre and store it in a dictionary
        for x in row["gnr"]:
            if x in gnrdict.keys():             # checking if the genre is already stored
                gnrdict[x]=gnrdict[x]+1
            else:
                gnrdict[x] = 1            # incrementing the value by 1


    sorted_gnr_dict = {k: v for k, v in sorted(gnrdict.items(), key=lambda item: item[1])}    #
    gnr_list=list(sorted_gnr_dict.keys())  # getting list of keys

    count_list=list(sorted_gnr_dict.values())   # getting list of values

    othercount= count_list[0]+count_list[1]+count_list[2]+count_list[3]     #counting for other category
    count_list=count_list[4:]                      ## list of count excluding lowest 3
    gnr_list=gnr_list[4:]                          ## list of genres excpet last 4
    count_list.insert(len(count_list),othercount)  # adding count of others
    gnr_list.append('other')                   # adding other category

    plt.clf()    #clearing plot figure

    plt.figure(figsize=(7,7))
    labels=gnr_list
    values=count_list
    plt.pie(values,  labels=labels, autopct='%1.1f%%')    # plotting the pie chart
    plt.title('genres')                                   # giving title for the plot



    #################################################

    plt.savefig("{}-Q11.png".format(studentid))


def question_12(df10):
    """
    :param df10: the dataframe created in question 10
    :return: nothing, but saves the figure on the disk
    """

    #################################################
    # Your code goes here ...
    df12=df10.copy()                                                          # making a copy of the passed variable
    country_dict = {}                                                           ## dicitonary to store the count of each country
    df12["p_country"] = df12["production_countries"].apply(ast.literal_eval)     ## applying literal eval
    df12["p_country"] = df12['p_country'].apply(lambda x: [d['name'] for d in x])   ##making a list of only dict['name']  from each dict .
    for index, row in df12.iterrows():                       ### iterating through column "p_country" and each list to count each genre and store it in a dictionary
        for x in row["p_country"]:
            if x in country_dict.keys():
                country_dict[x]=country_dict[x]+1
            else:
                country_dict[x] = 1

    sorted_country_dict = {k: v for k, v in sorted(country_dict.items(), key=lambda item: item[0])}        # sorting dicitonary accroding to key
    sorted_country_names = list(sorted_country_dict.keys())                            # list of keys in dicitonary

    sorted_country_count = list(sorted_country_dict.values())                   # list of values in dictionary
    plt.clf()                                                              ##clearing plot

    plt.bar(sorted_country_names, sorted_country_count, color='green')           ## plotting bar graph
    plt.xticks(rotation=90)                                          # making  angle of xtick labels 90 degree


    plt.title("Production Country")         #setting the title
    plt.tight_layout()                  # fitting everything in the figure
    #################################################

    plt.savefig("{}-Q12.png".format(studentid))


def question_13(df10):
    """
    :param df10: the dataframe created in question 10
    :return: nothing, but saves the figure on the disk
    """

    #################################################
    # Your code goes here ...
    df13=df10.copy()
    plt.clf()
    plt.figure(figsize=(10, 10))                                                         # making a plot figure
    df13["spoken_languages"] = df13["spoken_languages"].apply(ast.literal_eval)             # applying literal eval
    df13["language"] = df13['spoken_languages'].apply(lambda x: [d['name'] for d in x])  # getting a list of dict['name'] from each dict in row
    df13["language"]=df13["language"].str.get(0)                                           # making the column to contain only one


    groups = df13.groupby("language")                             # defining groups by the language column, this will give different colours to the plot
    for name, group in groups:
        plt.plot(group["vote_average"], group["success_impact"], marker="o", linestyle="", label=name )   ## ploting the scatter plot

    plt.legend( loc='center left', bbox_to_anchor=(1, 0.5))
    plt.tight_layout()                                            #fitting everything in the plot


    #################################################

    plt.savefig("{}-Q13.png".format(studentid))



if __name__ == "__main__":
    df1 = question_1("movies.csv", "credits.csv")
    df2 = question_2(df1)
    df3 = question_3(df2)
    df4 = question_4(df3)
    df5 = question_5(df4)
    df6 = question_6(df5)
    df7 = question_7(df6)
    df8 = question_8(df7)
    movies = question_9(df8)
    df10 = question_10(df8)
    question_11(df10)
    question_12(df10)
    question_13(df10)
