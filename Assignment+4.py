#Definitions:
#A quarter is a specific three month period, Q1 is January through March, Q2 is 
#April through June, Q3 is July through September, Q4 is October through December.
#A recession is defined as starting with two consecutive quarters of GDP decline, 
#and ending with two consecutive quarters of GDP growth.
#A recession bottom is the quarter within a recession which had the lowest GDP.
#A university town is a city which has a high percentage of university students 
#compared to the total population of the city.

#Hypothesis: University towns have their mean housing prices less effected by 
#recessions. Run a t-test to compare the ratio of the mean price of houses in 
#university towns the quarter before the recession starts compared to the recession bottom. 
#(price_ratio=quarter_before_recession/recession_bottom)

#The following data files are available for this assignment:
#From the Zillow research data site there is housing data for the United States. 
#In particular the datafile for all homes at a city level, City_Zhvi_AllHomes.csv, 
#has median home sale prices at a fine grained level.
#From the Wikipedia page on college towns is a list of university towns in the 
#United States which has been copy and pasted into the file university_towns.txt.
#From Bureau of Economic Analysis, US Department of Commerce, the GDP over time 
#of the United States in current dollars (use the chained value in 2009 dollars), 
#in quarterly intervals, in the file gdplev.xls. For this assignment, only look at 
#GDP data from the first quarter of 2000 onward.

# Use this dictionary to map state names to two letter acronyms
states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}

#get_list_of_university_towns():
#Returns a DataFrame of towns and the states they are in from the university_towns.txt list. 
#The format of the DataFrame should be: DataFrame( [ ["Michigan", "Ann Arbor"], 
#["Michigan", "Yipsilanti"] ], columns=["State", "RegionName"] )
#The following cleaning needs to be done:
#1. For "State", removing characters from "[" to the end.
#2. For "RegionName", when applicable, removing every character from " (" to the end.
#3. Depending on how you read the data, you may need to remove newline character '\n'. '''
def get_list_of_university_towns():
    import pandas as pd
    import numpy as np
    from scipy.stats import ttest_ind

    
    towns = open("university_towns.txt", "r")

#CREATING UNIVERSITY TOWNS DATA FRAME
    Towns_List = []
    for i in towns:
        Towns_List.append(i)

    State_List = []
    for i in Towns_List:
        if "edit" in i:
            x = i
            state = i
            State_List.append(state)
        else:
            state = x
            State_List.append(state)
        
    DF_Towns_List = pd.DataFrame({"State":State_List, "RegionName":Towns_List})
    DF_Towns_List = DF_Towns_List[DF_Towns_List["State"] != DF_Towns_List["RegionName"]]
    DF_Towns_List["State"] = DF_Towns_List["State"].map(lambda x: x.rstrip('[edit]\n'))
    DF_Towns_List["RegionName"] = DF_Towns_List["RegionName"].str.split('(').str[0] 
    DF_Towns_List = DF_Towns_List[["State", "RegionName"]]
    DF_Towns_List = DF_Towns_List.sort_values(by= 1, axis=1, ascending=True)
    DF_Towns_List = DF_Towns_List.reset_index()
    DF_Towns_List =  DF_Towns_List.drop(labels = "index", axis = 1)

    return DF_Towns_List
get_list_of_university_towns()

#get_recession_start():
#Returns the year and quarter of the recession start time as a 
#string value in a format such as 2005q3'''
def get_recession_start():
    import pandas as pd
    import numpy as np
    from scipy.stats import ttest_ind
    
    DF_Recession = pd.read_excel("gdplev.xls", skiprows = (0,1,2,3,4,5,6))
    DF_Recession.columns = ("Scrap1", "Scrap2", 
                         "Scrap3", "NaN", "Quarterly (Seasonally adjusted annual rates)", 
                         "GDP in billions of current dollars", "GDP in billions of chained 2009 dollars", "NaN2")
    DF_Recession = DF_Recession.drop(labels = ["Scrap1", "Scrap2", "Scrap3", "NaN", "NaN2"], axis = 1)
    DF_Recession = DF_Recession.iloc[212:, :]
    DF_Recession["Difference"] = DF_Recession["GDP in billions of chained 2009 dollars"].diff(periods = 1)
    Recession_Indicator = []
    for i in DF_Recession["Difference"]:
        if i < 0:
            x = "recession"
            Recession_Indicator.append(x)
        else: 
            x = "not recession"
            Recession_Indicator.append(x)
    Recession_Start = []
    x = 0
    for i in range(0, len(Recession_Indicator)-1):
        if x == 0 and Recession_Indicator[i+1] == Recession_Indicator[i] == "recession":
            x = "Recession_Start"
            Recession_Start.append("Recession_Start")
        elif x == "Recession_Start" and Recession_Indicator[i+1] == Recession_Indicator[i] == "not recession":
            x = "Recession_End"
            Recession_Start.append("Recession_End")
        elif x == "Recession_Start":
            Recession_Start.append("Recession")
        elif x == "Recession_End":
            Recession_Start.append("NA")
        else: 
            Recession_Start.append("NA")
    Recession_Start.append("NA") 
    len(Recession_Start)
    DF_Recession["Recession_Indicator"] = Recession_Start
    DF_Recession.iloc[30:60]

    Start = DF_Recession["Quarterly (Seasonally adjusted annual rates)"].where(DF_Recession["Recession_Indicator"] == "Recession_Start")
    Start = pd.Series(Start).dropna()
    Start = Start.values
    Answer = Start[0]
    
    return Answer
get_recession_start()

#get_recession_end():
#Returns the year and quarter of the recession end time as a 
#string value in a format such as 2005q3'''
def get_recession_end():
    import pandas as pd
    import numpy as np
    from scipy.stats import ttest_ind
    
    DF_Recession = pd.read_excel("gdplev.xls", skiprows = (0,1,2,3,4,5,6))
    DF_Recession.columns = ("Scrap1", "Scrap2", 
                         "Scrap3", "NaN", "Quarterly (Seasonally adjusted annual rates)", 
                         "GDP in billions of current dollars", "GDP in billions of chained 2009 dollars", "NaN2")
    DF_Recession = DF_Recession.drop(labels = ["Scrap1", "Scrap2", "Scrap3", "NaN", "NaN2"], axis = 1)
    DF_Recession = DF_Recession.iloc[212:, :]
    DF_Recession["Difference"] = DF_Recession["GDP in billions of chained 2009 dollars"].diff(periods = 1)
    Recession_Indicator = []
    for i in DF_Recession["Difference"]:
        if i < 0:
            x = "recession"
            Recession_Indicator.append(x)
        else: 
            x = "not recession"
            Recession_Indicator.append(x)
    Recession_Start = []
    x = 0
    for i in range(0, len(Recession_Indicator)-1):
        if x == 0 and Recession_Indicator[i+1] == Recession_Indicator[i] == "recession":
            x = "Recession_Start"
            Recession_Start.append("Recession_Start")
        elif x == "Recession_Start" and Recession_Indicator[i-1] == Recession_Indicator[i] == "not recession":
            x = "Recession_End"
            Recession_Start.append("Recession_End")
        elif x == "Recession_Start":
            Recession_Start.append("Recession")
        elif x == "Recession_End":
            Recession_Start.append("NA")
        else: 
            Recession_Start.append("NA")
    Recession_Start.append("NA") 
    len(Recession_Start)
    DF_Recession["Recession_Indicator"] = Recession_Start
    DF_Recession.iloc[30:60]

    End = DF_Recession["Quarterly (Seasonally adjusted annual rates)"].where(DF_Recession["Recession_Indicator"] == "Recession_End")
    End = pd.Series(End).dropna()
    End = End.values
    Answer = End[0]
    return Answer
get_recession_end()

#get_recession_bottom():
#Returns the year and quarter of the recession bottom time as a 
#string value in a format such as 2005q3
def get_recession_bottom():
    import pandas as pd
    import numpy as np
    from scipy.stats import ttest_ind
    
    DF_Recession = pd.read_excel("gdplev.xls", skiprows = (0,1,2,3,4,5,6))
    DF_Recession.columns = ("Scrap1", "Scrap2", 
                         "Scrap3", "NaN", "Quarterly (Seasonally adjusted annual rates)", 
                         "GDP in billions of current dollars", "GDP in billions of chained 2009 dollars", "NaN2")
    DF_Recession = DF_Recession.drop(labels = ["Scrap1", "Scrap2", "Scrap3", "NaN", "NaN2"], axis = 1)
    DF_Recession = DF_Recession.iloc[212:, :]
    DF_Recession["Difference"] = DF_Recession["GDP in billions of chained 2009 dollars"].diff(periods = 1)
    Recession_Indicator = []
    for i in DF_Recession["Difference"]:
        if i < 0:
            x = "recession"
            Recession_Indicator.append(x)
        else: 
            x = "not recession"
            Recession_Indicator.append(x)
    Recession_Start = []
    x = 0
    for i in range(0, len(Recession_Indicator)-1):
        if x == 0 and Recession_Indicator[i+1] == Recession_Indicator[i] == "recession":
            x = "Recession_Start"
            Recession_Start.append("Recession_Start")
        elif x == "Recession_Start" and Recession_Indicator[i+1] == Recession_Indicator[i] == "not recession":
            x = "Recession_End"
            Recession_Start.append("Recession_End")
        elif x == "Recession_Start":
            Recession_Start.append("Recession")
        elif x == "Recession_End":
            Recession_Start.append("NA")
        else: 
            Recession_Start.append("NA")
    Recession_Start.append("NA") 
    len(Recession_Start)
    DF_Recession["Recession_Indicator"] = Recession_Start

    Data = DF_Recession.loc[(DF_Recession["Recession_Indicator"] != "NA")]
    Min = Data["GDP in billions of chained 2009 dollars"].min()
    MinQ = Data["Quarterly (Seasonally adjusted annual rates)"].where(Data["GDP in billions of chained 2009 dollars"] == Min)
    MinQ = pd.Series(MinQ).dropna()
    MinQ = MinQ.values
    Answer = MinQ[0]

    return Answer
get_recession_bottom()

#convert_housing_data_to_quarters():
#Converts the housing data to quarters and returns it as mean 
#values in a dataframe. This dataframe should be a dataframe with
#columns for 2000q1 through 2016q3, and should have a multi-index
#in the shape of ["State","RegionName"].
#Note: Quarters are defined in the assignment description, they are
#not arbitrary three month periods.
#The resulting dataframe should have 67 columns, and 10,730 rows.
def convert_housing_data_to_quarters():
    import numpy as np
    import pandas as pd
    DF_City_Sales_Prices = pd.read_csv("City_Zhvi_AllHomes.csv")
    list(DF_City_Sales_Prices.columns)
    DF_City_Sales_Prices = DF_City_Sales_Prices.drop(labels = DF_City_Sales_Prices.iloc[:, 6:-200], axis = 1)
    DF_City_Sales_Prices = DF_City_Sales_Prices.drop(labels = ["RegionID", "Metro", "CountyName", "SizeRank"], axis = 1)
    DF_City_Sales_Prices.head()
    i = "2001q1"
    QList = ('2000q1','2000q2','2000q3','2000q4','2001q1','2001q2','2001q3','2001q4','2002q1','2002q2','2002q3','2002q4','2003q1',
         '2003q2','2003q3','2003q4','2004q1','2004q2','2004q3','2004q4','2005q1','2005q2','2005q3','2005q4','2006q1','2006q2',
         '2006q3','2006q4','2007q1','2007q2','2007q3','2007q4','2008q1','2008q2','2008q3','2008q4','2009q1','2009q2','2009q3',
         '2009q4','2010q1','2010q2','2010q3','2010q4','2011q1','2011q2','2011q3','2011q4','2012q1','2012q2','2012q3','2012q4',
         '2013q1','2013q2','2013q3','2013q4','2014q1','2014q2','2014q3','2014q4','2015q1','2015q2','2015q3','2015q4','2016q1',
         '2016q2')
    MonthList = list(DF_City_Sales_Prices.columns)[2:]
    MonthList
    Month1 = MonthList[0::3]
    Month1 = Month1[:-1]
    Month2 = MonthList[1::3]
    Month2 = Month2[:-1]
    Month3 = MonthList[2::3]

    for i,j,k,l in zip(QList, Month1, Month2, Month3):
        DF_City_Sales_Prices[i] = (DF_City_Sales_Prices[j] + DF_City_Sales_Prices[k] + DF_City_Sales_Prices[l]) / 3
    DF_City_Sales_Prices["2016q3"] = (DF_City_Sales_Prices['2016-07'] + DF_City_Sales_Prices['2016-08']) / 2
    DF_City_Sales_Prices = DF_City_Sales_Prices[["RegionName", "State", '2000q1','2000q2','2000q3','2000q4','2001q1','2001q2','2001q3','2001q4','2002q1','2002q2','2002q3','2002q4','2003q1',
         '2003q2','2003q3','2003q4','2004q1','2004q2','2004q3','2004q4','2005q1','2005q2','2005q3','2005q4','2006q1','2006q2',
         '2006q3','2006q4','2007q1','2007q2','2007q3','2007q4','2008q1','2008q2','2008q3','2008q4','2009q1','2009q2','2009q3',
         '2009q4','2010q1','2010q2','2010q3','2010q4','2011q1','2011q2','2011q3','2011q4','2012q1','2012q2','2012q3','2012q4',
         '2013q1','2013q2','2013q3','2013q4','2014q1','2014q2','2014q3','2014q4','2015q1','2015q2','2015q3','2015q4','2016q1',
         '2016q2', "2016q3"]]
    #Use this dictionary to map state names to two letter acronyms
    states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}
    DF_City_Sales_Prices.replace({"State": states}, inplace = True)
    DF_City_Sales_Prices = DF_City_Sales_Prices.set_index(keys = ["State", "RegionName"])
    DF_City_Sales_Prices
    return DF_City_Sales_Prices
convert_housing_data_to_quarters()

#run_ttest():
#First creates new data showing the decline or growth of housing prices
#between the recession start and the recession bottom. Then runs a ttest
#comparing the university town values to the non-university towns values, 
#return whether the alternative hypothesis (that the two groups are the same)
#is true or not as well as the p-value of the confidence. 
#Return the tuple (different, p, better) where different=True if the t-test is
#True at a p<0.01 (we reject the null hypothesis), or different=False if 
#otherwise (we cannot reject the null hypothesis). The variable p should
#be equal to the exact p value returned from scipy.stats.ttest_ind(). The
#value for better should be either "university town" or "non-university town"
#depending on which has a lower mean price ratio (which is equivilent to a
#reduced market loss).
def run_ttest():
    import pandas as pd
    import numpy as np
    from scipy.stats import ttest_ind
    
    Recession_Start = get_recession_start()
    Recession_Bottom = get_recession_bottom()
    Uni_Towns = get_list_of_university_towns()

    House_Prices = convert_housing_data_to_quarters().dropna()

    Change = pd.DataFrame({'Change': House_Prices[Recession_Start].div(House_Prices[Recession_Bottom])})

    House_Prices.columns = House_Prices.columns.to_series().astype(str)
    House_Prices = pd.concat([House_Prices, Change], axis=1)

    House_Prices = pd.DataFrame(House_Prices)
    House_Prices.reset_index(['State','RegionName'], inplace = True)

    UniTown_PriceChange = House_Prices.loc[list(Uni_Towns.index)]['Change'].dropna()
    NonUniTown_PriceChange_index = set(House_Prices.index) - set(UniTown_PriceChange)
    NonUniTown_PriceChange = House_Prices.loc[list(NonUniTown_PriceChange_index),:]["Change"].dropna()
    
    tstat, p = tuple(ttest_ind(UniTown_PriceChange, NonUniTown_PriceChange))
    
    different = p < 0.05
    result = tstat < 0
    better = ["university town", "non-university town"]
    
    return (different, p, better[result])
run_ttest()