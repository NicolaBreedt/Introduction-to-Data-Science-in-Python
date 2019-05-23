# -*- coding: utf-8 -*-

def answer_one():
#LOADING AND CLEANING Energy Indicators.xls
    import pandas as pd
    df = pd.read_excel("Energy Indicators.xls", header = 8, skiprows = (0,1,2,3,4,5,6,7,8), skipfooter = 38, usecols = (2,3,4,5),
                       names = ['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable'], na_values = "...")
#Converting to gigajoules
    df["Energy Supply"] = df["Energy Supply"] * 1000000
    df["Country"].replace({"Republic of Korea": "South Korea", "United States of America20": "United States", 
                           "United Kingdom of Great Britain and Northern Ireland19": "United Kingdom", 
                           "China, Hong Kong Special Administrative Region3": "Hong Kong", "Iran (Islamic Republic of)":"Iran"}, inplace = True)
#Removing () and everything inside
    df["Country"] = df["Country"].str.replace(r"\(.*\)","")
#Removing numbers from country names
    df["Country"] = df["Country"].str.replace("\d+", "")
#LOADING AND CLEANING file world_bank.csv
    GDP = pd.read_csv("world_bank.csv", header = 4)
    GDP["Country Name"].replace({"Korea, Rep.": "South Korea", "Iran, Islamic Rep.": "Iran", "Hong Kong SAR, China": "Hong Kong"}, inplace = True)
# LOADING scimagojr-3.xlsx
    ScimEn = pd.read_excel("scimagojr-3.xlsx")
#CREATING COMBINED DATA FRAME
    DF1 = pd.DataFrame.merge(ScimEn, df, how = "left", left_on = "Country", right_on = "Country")
    DF2 = pd.DataFrame.merge(DF1, GDP, how = "left", left_on = "Country", right_on = "Country Name")
    DF3 = DF2[["Country", "Rank", "Documents", "Citable documents", "Citations", "Self-citations", "Citations per document", 'H index', 'Energy Supply', 'Energy Supply per Capita', '% Renewable', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015']]
    DF3 = DF3.sort_values("Rank")
    DF3 = DF3.set_index("Country")
    DF = DF3.iloc[0:15, :]
    return DF
answer_one()

def answer_two():
   #LOADING AND CLEANING Energy Indicators.xls
    import pandas as pd
    df = pd.read_excel("Energy Indicators.xls", header = 8, skiprows = (0,1,2,3,4,5,6,7,8), skipfooter = 38, usecols = (2,3,4,5),
                       names = ['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable'], na_values = "...")
#Converting to gigajoules
    df["Energy Supply"] = df["Energy Supply"] * 1000000
    df["Country"].replace({"Republic of Korea": "South Korea", "United States of America20": "United States", 
                           "United Kingdom of Great Britain and Northern Ireland19": "United Kingdom", 
                           "China, Hong Kong Special Administrative Region3": "Hong Kong", "Iran (Islamic Republic of)":"Iran"}, inplace = True)
#Removing () and everything inside
    df["Country"] = df["Country"].str.replace(r"\(.*\)","")
#Removing numbers from country names
    df["Country"] = df["Country"].str.replace("\d+", "")
#LOADING AND CLEANING file world_bank.csv
    GDP = pd.read_csv("world_bank.csv", header = 4)
    GDP["Country Name"].replace({"Korea, Rep.": "South Korea", "Iran, Islamic Rep.": "Iran", "Hong Kong SAR, China": "Hong Kong"}, inplace = True)
# LOADING scimagojr-3.xlsx
    ScimEn = pd.read_excel("scimagojr-3.xlsx")
#CREATING COMBINED DATA FRAME
    DF1 = pd.DataFrame.merge(ScimEn, df, how = "left", left_on = "Country", right_on = "Country")
    DF2 = pd.DataFrame.merge(DF1, GDP, how = "left", left_on = "Country", right_on = "Country Name")
    DF3 = DF2[['Country', 'Rank', 'Documents', 'Citable documents', 'Citations', 'Self-citations', 'Citations per document', 'H index', 'Energy Supply', 'Energy Supply per Capita', '% Renewable', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015']]
    DF3 = DF3.sort_values("Rank")
    DF3 = DF3.set_index("Country")
    DF = DF3.iloc[0:15, :]
    Lost1 = len(df["Country"]) - len(ScimEn["Country"])
    Lost2 = len(GDP["Country Name"]) - len(ScimEn["Country"])
    Lost3 = Lost1 + Lost2
    return Lost3
answer_two()

def answer_three():
    import pandas as pd
    import numpy as np
    DF = answer_one()
    DF["Mean"] = DF.iloc[:, 10:20].mean(axis = 1, skipna = True)
    avgGDP = pd.Series(DF["Mean"])
    pd.Series.sort_values(avgGDP, ascending = False)
    return avgGDP
answer_three()

def answer_four():
    import pandas as pd
    import numpy as np
    DF = answer_one()
    DF["Mean"] = DF.iloc[:, 10:20].mean(axis = 1, skipna = True)
    DF.sort_values("Mean", ascending = False, inplace = True)
    Answer = abs(DF.iloc[5, 10] - DF.iloc[5, 19])
    return Answer
answer_four()

def answer_five():
    import pandas as pd
    import numpy as np
    DF = answer_one()
    Answer = pd.Series(DF["Energy Supply per Capita"]).mean()
    return Answer
answer_five()

def answer_six():
    import pandas as pd
    import numpy as np
    DF = answer_one()
    Country = pd.Series(DF["% Renewable"]).idxmax(axis = 1)
    Value = pd.Series(DF["% Renewable"]).max()
    Answer = (Country, Value)
    return Answer
answer_six()

def answer_seven():
    import pandas as pd
    import numpy as np
    DF = answer_one()
    DF["Ratio"] = DF["Self-citations"] / DF["Citations"]
    Country = pd.Series(DF["Ratio"]).idxmax(axis = 1)
    Value = pd.Series(DF["Ratio"]).max()
    Answer = (Country, Value)
    return Answer
answer_seven()

def answer_eight():
    import pandas as pd
    import numpy as np
    DF = answer_one()
    DF["PopEst"] = DF["Energy Supply"] / DF["Energy Supply per Capita"]
    PopSeries = pd.Series(DF["PopEst"])
    PopSeries.sort_values(ascending = False)
    Answer = PopSeries.index[2]
    return Answer
answer_eight()

def answer_nine():
    import pandas as pd
    import numpy as np
    DF = answer_one()
    DF["PopEst"] = DF["Energy Supply"] / DF["Energy Supply per Capita"]
    DF["Doc per person"] = DF["Citable documents"] / DF["PopEst"]
    Answer = DF["Doc per person"].corr(DF["Energy Supply per Capita"], method = "pearson")
    return Answer
answer_nine()

def answer_ten():
    import pandas as pd
    import numpy as np
    DF = answer_one()
    Mean = DF["% Renewable"].median()
    def Cat(x):
        if x >= Mean:
            return 1
        else:
            return 0
    DF["Type"] = DF["% Renewable"].apply(Cat)
    DF.sort_values(by = "Rank", ascending = True, inplace = True)
    HighRenew = pd.Series(DF["Type"])
    return HighRenew
answer_ten()

def answer_eleven():
    import pandas as pd
    import numpy as np
    DF = answer_one()
    DF["Country"] = DF.index
    ContinentDict  = {'China':'Asia', 
                      'United States':'North America', 
                      'Japan':'Asia', 
                      'United Kingdom':'Europe', 
                      'Russian Federation':'Europe', 
                      'Canada':'North America', 
                      'Germany':'Europe', 
                      'India':'Asia',
                      'France':'Europe', 
                      'South Korea':'Asia', 
                      'Italy':'Europe', 
                      'Spain':'Europe', 
                      'Iran':'Asia',
                      'Australia':'Australia', 
                      'Brazil':'South America'}
    DF["Continent"] = DF["Country"].map(ContinentDict)
    DF["PopEst"] = DF["Energy Supply"] / DF["Energy Supply per Capita"]
    DF2 = DF.set_index('Continent').groupby(level=0)['PopEst'].agg({"size":"count", "sum":"sum", "mean":"mean", "std":"std"})
    DF2["size"].apply(float)
    return DF2
answer_eleven()

def answer_twelve():
    DF = answer_one()
    import pandas as pd
    import numpy as np
    DF["Country"] = DF.index
    ContinentDict  = {'China':'Asia', 
                      'United States':'North America', 
                      'Japan':'Asia', 
                      'United Kingdom':'Europe', 
                      'Russian Federation':'Europe', 
                      'Canada':'North America', 
                      'Germany':'Europe', 
                      'India':'Asia',
                      'France':'Europe', 
                      'South Korea':'Asia', 
                      'Italy':'Europe', 
                      'Spain':'Europe', 
                      'Iran':'Asia',
                      'Australia':'Australia', 
                      'Brazil':'South America'}
    DF["Bins"] = pd.cut(DF["% Renewable"], bins = 5, right=True)
    DF["Continent"] = DF["Country"].map(ContinentDict)
    DF2 = DF.set_index(['Continent', "Bins"]).groupby(level = (0,1))["% Renewable"].agg({"size":"count"})
    DF2 = DF2.T.squeeze()
    return DF2
answer_twelve()

