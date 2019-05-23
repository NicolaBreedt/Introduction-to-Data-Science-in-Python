#Load the energy data from the file Energy Indicators.xls, which is a list of 
#indicators of energy supply and renewable electricity production from the United 
#Nations for the year 2013, and should be put into a DataFrame with the variable name of energy.
#Keep in mind that this is an Excel file, and not a comma separated values file. 
#Also, make sure to exclude the footer and header information from the datafile. 
#The first two columns are unneccessary, so you should get rid of them, and you 
#should change the column labels so that the columns are:
#['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable']
#Convert Energy Supply to gigajoules (there are 1,000,000 gigajoules in a petajoule). 
#For all countries which have missing data (e.g. data with "...") make sure this 
#is reflected as np.NaN values.
#Rename the following list of countries (for use in later questions):
#"Republic of Korea": "South Korea",
#"United States of America": "United States",
#"United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
#"China, Hong Kong Special Administrative Region": "Hong Kong"
#There are also several countries with numbers and/or parenthesis in their name. 
#Be sure to remove these,
#e.g.
#'Bolivia (Plurinational State of)' should be 'Bolivia',
#'Switzerland17' should be 'Switzerland'.
#Next, load the GDP data from the file world_bank.csv, which is a csv containing 
#countries' GDP from 1960 to 2015 from World Bank. Call this DataFrame GDP.
#Make sure to skip the header, and rename the following list of countries:
#"Korea, Rep.": "South Korea", 
#"Iran, Islamic Rep.": "Iran",
#"Hong Kong SAR, China": "Hong Kong"
#Finally, load the Sciamgo Journal and Country Rank data for Energy Engineering 
#and Power Technology from the file scimagojr-3.xlsx, which ranks countries based 
#on their journal contributions in the aforementioned area. Call this DataFrame ScimEn.
#Join the three datasets: GDP, Energy, and ScimEn into a new dataset (using the 
#intersection of country names). Use only the last 10 years (2006-2015) of GDP 
#data and only the top 15 countries by Scimagojr 'Rank' (Rank 1 through 15).
#The index of this DataFrame should be the name of the country, and the columns 
#should be ['Rank', 'Documents', 'Citable documents', 'Citations', 'Self-citations', 
#'Citations per document', 'H index', 'Energy Supply', 'Energy Supply per Capita', 
#'% Renewable', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', 
#'2014', '2015'].
#This function should return a DataFrame with 20 columns and 15 entries.
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

#The previous question joined three datasets then reduced this to just the top 
#15 entries. When you joined the datasets, but before you reduced this to the 
#top 15 items, how many entries did you lose?
#This function should return a single number.
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

#Answer the following questions in the context of only the top 15 countries by 
#Scimagojr Rank (aka the DataFrame returned by answer_one())

#What is the average GDP over the last 10 years for each country? 
#(exclude missing values from this calculation.)
#This function should return a Series named avgGDP with 15 countries and their 
#average GDP sorted in descending order.
def answer_three():
    import pandas as pd
    import numpy as np
    DF = answer_one()
    DF["Mean"] = DF.iloc[:, 10:20].mean(axis = 1, skipna = True)
    avgGDP = pd.Series(DF["Mean"])
    pd.Series.sort_values(avgGDP, ascending = False)
    return avgGDP
answer_three()

#By how much had the GDP changed over the 10 year span for the country with the 
#6th largest average GDP?
#This function should return a single number.
def answer_four():
    import pandas as pd
    import numpy as np
    DF = answer_one()
    DF["Mean"] = DF.iloc[:, 10:20].mean(axis = 1, skipna = True)
    DF.sort_values("Mean", ascending = False, inplace = True)
    Answer = abs(DF.iloc[5, 10] - DF.iloc[5, 19])
    return Answer
answer_four()

#What is the mean Energy Supply per Capita?
#This function should return a single number.
def answer_five():
    import pandas as pd
    import numpy as np
    DF = answer_one()
    Answer = pd.Series(DF["Energy Supply per Capita"]).mean()
    return Answer
answer_five()

#What country has the maximum % Renewable and what is the percentage?
#This function should return a tuple with the name of the country and the percentage.
def answer_six():
    import pandas as pd
    import numpy as np
    DF = answer_one()
    Country = pd.Series(DF["% Renewable"]).idxmax(axis = 1)
    Value = pd.Series(DF["% Renewable"]).max()
    Answer = (Country, Value)
    return Answer
answer_six()

#Create a new column that is the ratio of Self-Citations to Total Citations. 
#What is the maximum value for this new column, and what country has the highest ratio?
#This function should return a tuple with the name of the country and the ratio.
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

#Create a column that estimates the population using Energy Supply and Energy 
#Supply per capita. What is the third most populous country according to this estimate?
#This function should return a single string value.
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

#Create a column that estimates the number of citable documents per person. 
#What is the correlation between the number of citable documents per capita and 
#the energy supply per capita? Use the .corr() method, (Pearson's correlation).
#This function should return a single number.
def answer_nine():
    import pandas as pd
    import numpy as np
    DF = answer_one()
    DF["PopEst"] = DF["Energy Supply"] / DF["Energy Supply per Capita"]
    DF["Doc per person"] = DF["Citable documents"] / DF["PopEst"]
    Answer = DF["Doc per person"].corr(DF["Energy Supply per Capita"], method = "pearson")
    return Answer
answer_nine()

#Create a new column with a 1 if the country's % Renewable value is at or above 
#the median for all countries in the top 15, and a 0 if the country's % Renewable 
#value is below the median.
#This function should return a series named HighRenew whose index is the country 
#name sorted in ascending order of rank.
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

#Use the following dictionary to group the Countries by Continent, then create 
#a dateframe that displays the sample size (the number of countries in each 
#continent bin), and the sum, mean, and std deviation for the estimated population 
#of each country.
#This function should return a DataFrame with index named Continent 
#['Asia', 'Australia', 'Europe', 'North America', 'South America'] and columns 
#['size', 'sum', 'mean', 'std']
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

#Cut % Renewable into 5 bins. Group Top15 by the Continent, as well as these 
#new % Renewable bins. How many countries are in each of these groups?
#This function should return a Series with a MultiIndex of Continent, then the 
#bins for % Renewable. Do not include groups with no countries.
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

