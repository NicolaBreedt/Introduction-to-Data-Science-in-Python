#The following code loads the olympics dataset (olympics.csv), which was derrived 
#from the Wikipedia entry on All Time Olympic Games Medals, and does some basic 
#data cleaning.
#The columns are organized as # of Summer games, Summer medals, # of Winter games, 
#Winter medals, total # number of games, total # of medals. Use this dataset to 
#answer the questions below.

import pandas as pd

df = pd.read_csv('olympics.csv', index_col=0, skiprows=1)

for col in df.columns:
    if col[:2]=='01':
        df.rename(columns={col:'Gold'+col[4:]}, inplace=True)
    if col[:2]=='02':
        df.rename(columns={col:'Silver'+col[4:]}, inplace=True)
    if col[:2]=='03':
        df.rename(columns={col:'Bronze'+col[4:]}, inplace=True)
    if col[:1]=='№':
        df.rename(columns={col:'#'+col[1:]}, inplace=True)

names_ids = df.index.str.split('\s\(') # split the index by '('

df.index = names_ids.str[0] # the [0] element is the country name (new index) 
df['ID'] = names_ids.str[1].str[:3] # the [1] element is the abbreviation or ID (take first 3 characters from that)

df = df.drop('Totals')
df.head()

#Which country has won the most gold medals in summer games?
#This function should return a single string value.
def answer_one():
    SummerGold = pd.Series(df["Gold"])
    Country = SummerGold.idxmax()
    return Country
answer_one()

#Which country had the biggest difference between their summer and winter gold medal counts?
#This function should return a single string value.
def answer_two():
    SG = pd.Series(df["Gold"])
    WG = pd.Series(df["Gold.1"])
    Difference = abs(SG - WG)
    Country = Difference.idxmax()
    return Country
answer_two()

#Which country has the biggest difference between their summer gold medal counts 
#and winter gold medal counts relative to their total gold medal count?
#Only include countries that have won at least 1 gold in both summer and winter.
#This function should return a single string value.
def answer_three():
    df1 = df.where(df["Gold"] > 0)
    df2 = df1.where(df["Gold.1"] > 0)
    df3 = df2.dropna()
    SummerG = pd.Series(df3["Gold"])
    WinterG = pd.Series(df3["Gold.1"])
    TotalG = pd.Series(df3["Gold.2"])
    Difference = abs(SummerG - WinterG)
    RelativeDiff = Difference / TotalG
    Country = RelativeDiff.idxmax()
    return Country
answer_three()

#Write a function that creates a Series called "Points" which is a weighted value 
#where each gold medal (Gold.2) counts for 3 points, silver medals (Silver.2) 
#for 2 points, and bronze medals (Bronze.2) for 1 point. The function should 
#return only the column (a Series object) which you created, with the country names as indices.
#This function should return a Series named Points of length 146
def answer_four():
    GoldTotal = pd.Series(df["Gold.2"])
    GoldPoints = []
    for i in GoldTotal:
        if i > 0:
            x = i * 3
        else:
            x = 0
        GoldPoints.append(x)
    df["GoldPoints"] = GoldPoints
    
    SilverTotal = pd.Series(df["Silver.2"])
    SilverPoints = []
    for i in SilverTotal:
        if i > 0:
            y = i * 2
        else:
            y = 0
        SilverPoints.append(y)
    df["SilverPoints"] = SilverPoints    
    
    BronzeTotal = pd.Series(df["Bronze.2"])
    BronzePoints = []
    for i in BronzeTotal:
        if i > 0:
            z = i * 1
        else:
            z = 0
        BronzePoints.append(z)
    df["BronzePoints"] = BronzePoints
    
    df["TotalPoints"] = df["GoldPoints"] + df["SilverPoints"] + df["BronzePoints"]
    
    Points = pd.Series(df["TotalPoints"])
    
    return Points
answer_four()

#For the next set of questions, we will be using census data from the United States Census Bureau.
census_df = pd.read_csv('census.csv')
census_df.head()

#Which state has the most counties in it? (hint: consider the sumlevel key 
#carefully! You'll need this for future questions too...)
#This function should return a single string value.
def answer_five():
    import numpy as np
    census_df50 = census_df[census_df['SUMLEV'] == 50]
    StateList = census_df50.STNAME.unique()
    
    State = []
    NumCounty = []
    for i in StateList:
        x = len(census_df50[(census_df50['STNAME'] == i)])
        State.append(i)
        NumCounty.append(x)
    
    New_df = pd.DataFrame({"State":State, "NumCounties":NumCounty})
    New_df = New_df.set_index('State')
    
    Statecounts = pd.Series(New_df["NumCounties"])
    MaxCount = Statecounts.idxmax()
    return MaxCount
answer_five()

#Only looking at the three most populous counties for each state, what are the 
#three most populous states (in order of highest population to lowest population)? 
#Use CENSUS2010POP.
#This function should return a list of string values.
def answer_six():
    import numpy as np
    census_df50 = census_df[census_df['SUMLEV'] == 50]
    StateList = census_df50["STNAME"].unique()
    TriCount = []
    for i in StateList:
        state_df50 = census_df50[census_df50['STNAME'] == i]
        state_df50 = state_df50.sort_values(by = "CENSUS2010POP", ascending=False)        
        x = sum(state_df50["CENSUS2010POP"][0:3])
        TriCount.append(x)
    New_df = (pd.DataFrame({"State":np.array(StateList), "Top3Cty#":np.array(TriCount)})).set_index('State')
    New_df = New_df.sort_values(by = "Top3Cty#", ascending=False)
    Answer = New_df[0:3].index.tolist()
    return Answer
answer_six()

#Which county has had the largest absolute change in population within the period 
#2010-2015? (Hint: population values are stored in columns POPESTIMATE2010 through 
#POPESTIMATE2015, you need to consider all six columns.)
#This function should return a single string value.
def answer_seven():
    
    import numpy as np
    census_df50 = census_df[census_df['SUMLEV'] == 50]
    new_df50 = census_df50[["CTYNAME", "POPESTIMATE2010", "POPESTIMATE2011", "POPESTIMATE2012", "POPESTIMATE2013", "POPESTIMATE2014", "POPESTIMATE2015"]]
    
    Difference = []
    length = new_df50["CTYNAME"].count()
    
    for i in range(0,length):
        x = max(new_df50.iloc[i, 1:7])
        y = min(new_df50.iloc[i, 1:7])
        diff = x - y
        Difference.append(diff)
    
    new_df50["Difference"] = Difference
    new_df50 = new_df50.sort_values(by = "Difference", ascending=False)
    new_df50 = new_df50.set_index("CTYNAME")
    Answer = new_df50[0:1].index.tolist()[0]
    return Answer
answer_seven()

#In this datafile, the United States is broken up into four regions using the "REGION" column.

#Create a query that finds the counties that belong to regions 1 or 2, whose name 
#starts with 'Washington', and whose POPESTIMATE2015 was greater than their POPESTIMATE 2014.
#This function should return a 5x2 DataFrame with the columns = ['STNAME', 'CTYNAME'] 
#and the same index ID as the census_df (sorted ascending by index).
def answer_eight():
    census_df50 = census_df[census_df['SUMLEV'] == 50]
    Answer = census_df50.loc[((census_df50['REGION'] != 3) & (census_df50['REGION'] != 4)) & (census_df50['POPESTIMATE2014'] < census_df50['POPESTIMATE2015']) & census_df50['CTYNAME'].str.contains("Washington"), ["STNAME", "CTYNAME"]]
    return Answer
answer_eight()