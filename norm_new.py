import pandas as pd 
import sys
import numpy
import collections
import itertools
df_list_soft=pd.read_csv('list_soft.csv')
df_purchase=pd.read_csv('purchase.csv',index_col="Software")
df_table=pd.read_csv('table.csv',index_col="Software")
df_purchase_test=pd.read_csv('purchase_test.csv', index_col="Software")
df_software=pd.read_csv('software.csv')

#This updates table.csv from purchase_test.csv (This would have been recently updated)
def pivot():
    df_tes=pd.read_csv('purchase_test.csv')
    meann=df_tes.mean(axis=1)
    df_tes["Mean"]=meann
    table_n=pd.melt(df_tes, id_vars =['Mean','Software'], var_name='User') #very important
    table_n=table_n.iloc[:,0:4]
    table_n.to_csv('table.csv')
    print('table.csv has been updated')
    
#This adds the rating to purchase_test.csv
def addRating(user,software,rating):
    df_purchase_test.set_index='Software'
    df_purchase_test.loc[software,user] = rating
    df_purchase_test.drop(['Mean'],axis=1)
    del df_purchase_test['Mean']
    df_purchase_test.to_csv('purchase_test.csv')
    print("purchase_test.csv has been updated")
     
#This one prints the top 10 suggestions from the persona
def printTop10FromPersona(list_software_by_persona):
    meann=df_purchase_test.mean(axis=1)
    df_purchase_test["Mean"]=meann
    df_temp_software=pd.DataFrame()
    for i in list_software_by_persona:
        df_temp=df_purchase_test.query('Software==@i')
        df_temp_software=df_temp_software.append(df_temp)

          
    top_10_from_persona=df_temp_software.nlargest(10,'Mean')
    top_10_from_persona=top_10_from_persona.loc[:,'Mean']
    print("The top ten suggestion from your persona are: ")
    print(top_10_from_persona)

#This prints the top 10 similar and top 10 dissimilar suggestions
def printTop10FromSimAndDis():
    correlationMatrix=df_purchase_test.corr(method ='pearson')
    print(correlationMatrix)

    max_correlation=correlationMatrix.nlargest(6,name)
    print(max_correlation)
    top_five_related=max_correlation.loc[:,name]
    top_five_related=top_five_related.iloc[1:6]
    print(top_five_related)

    min_correlation=correlationMatrix.nsmallest(5,name)
    print(min_correlation)
    least_five_related=min_correlation.loc[:,name]
    print(least_five_related)


    df_top_50=top10SoftwareByTop5User(top_five_related)

    df_down_50=top10SoftwareByTop5User(least_five_related)

    dict_rec=dataFrameToDictionarySorted(df_top_50)

    dict_rec_diversity=dataFrameToDictionarySorted(df_down_50)

    print("The recommendation from similar users")
    printDictionary(dict_rec)

    print("The recommendation from dissimilar users")
    printDictionary(dict_rec_diversity)

#This prints the key and value from dictionary
def printDictionary(dict_rec):
    for key, value in dict_rec:
        print (key, value)
    print()


#This adds the column of Mean and then uses it to sort the dictionary
def dataFrameToDictionarySorted(dataFrame):
    df_mean=dataFrame['Mean']
    dict_mean=df_mean.to_dict()
    dict_mean_sorted=sortDictionary(dict_mean)
    return(dict_mean_sorted)

#This sorts the dictionary
def sortDictionary(dictDf):
    sorted_x = sorted(dictDf.items(), key=lambda kv: kv[1], reverse=True)
    sorted_dict = collections.OrderedDict(sorted_x)
    x = itertools.islice(sorted_dict.items(), 0, 10)
    return(x)

#This returns the Top 10 software of a user and user name is the input
def top10SoftwareByUserName(name):
    df_user_table=df_table.query('User==@name')
    df_10_largest=df_user_table.nlargest(10,'value')
    return df_10_largest

#This gives top 10 softwares from top 5 similar/disimilar person,ie it gives 50 suggestions in total
def top10SoftwareByTop5User(top_five_related):
    dict_top_5=top_five_related.to_dict()
    top_5_users=list(dict_top_5.keys())
    df_top_50=pd.DataFrame()
    for i in top_5_users:
        temp=top10SoftwareByUserName(i)
        df_top_50=df_top_50.append(temp)

    return(df_top_50)
    

#This provides the list of softwares with the input persona
def listSoftwareByPersona(persona):
    df_software_persona=df_software.query('Category==@persona')
    df_software_persona=df_software_persona['Software']
    dict_software_persona=df_software_persona.to_dict()
    list_software_persona=list(dict_software_persona.values())
    return(list_software_persona)


name=input("Enter your name")
persona=input("Enter from the options\n1- Marketing\n2- Sales and BD\n3- Developer\n4- DevOps and IT\n")

df_user_purchase=df_table.query('User==@name')
count_rating=df_user_purchase['value'].count()
print(count_rating)
print(df_user_purchase)
if df_user_purchase.empty==False and count_rating>=15:  #Here the threshhold count is required to find correlation
    printTop10FromSimAndDis()                     #if not NaN values will dominate the recommendation leading to error 

list_software_by_persona=listSoftwareByPersona(persona)
printTop10FromPersona(list_software_by_persona)


ch=input('Enter y if you want to add rating')
if ch=='y':
    software_add=input("Enter the name of the software you want to add the rating ")
    rating_add=input("Enter the rating you are giving this software")
    addRating(name,software_add,rating_add)
    pivot()