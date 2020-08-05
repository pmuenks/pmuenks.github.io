# -*- coding: utf-8 -*-
"""EPPS 7V81 - Final Project.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Nq1eS2JvXfY5qR1RQllFvxk-boHGvzEs

Need to import pandas and requests to get the table.
"""

import pandas as pd
import requests

"""Usually, one might prefer to use Beautiful Soup to scrape website data. However, there are two reasons for using Request and Pandas rather than Beautiful Soup. First, the settings for the Texas SOS websites have security settings that prevent scraping using the default functions in Beautiful Soup. Accordingly, to access the data, onewould need to use an additional library to mimic accessing the website through a proxy, in this case, . By contrast, the request library allows one to access the site using a proxy request by the default library. Second, while Beautiful Soup allows one to scrape all data off of a webpage, Pandas has a built-in function that allows one to pull data into Python that is formatted in a table. Additionally, Panadas allows one to clean and trasnform the data while Beautiful Soup does not offer the same functionality for data cleaning. So while both Beautiful Soup and Pandas can accomplish pulling a datatable from a website, Pandas is preferred if one is only interested in the information from the data table. Therefore, as a general rule, an effective combination for scraping data would be to use a proxy site from Requests and Beautiful Soup to scrape the data. However, because this project is pulling data from a website table, using only Pandas to scrape the data is sufficient."""

base_site = 'https://elections.sos.state.tx.us/elchist5_race62.htm' #1992 Presidential election results

r = requests.get(base_site)
r.status_code

"""Here, the len(tables) command will return the number of tables found by the pd.read_html command. In this case, because there is only one table, the cleaning process is simple. However, if scraping a site that has multiple data tables, this function is useful for identifying multiple tables."""

tables = pd.read_html(r.text)

len(tables)

df_1992 = tables[0]
for col in df_1992.columns:
  print(col)
df_1992.columns = df_1992.columns.droplevel(0)
cols = [3,4,5,6,7,8,9,10,11,14]
df_1992.drop(df_1992.columns[cols],axis=1,inplace=True)
#df.drop(columns='W-I', axis=1)
df_1992.columns = df_1992.columns.droplevel(0)
df_1992['Year'] = 1992 ##Create year column
df_1992['Prez_Election'] = 1
for col in df_1992.columns:
  print(col)
df_1992.info()
df_1992

"""Repeat this process for 1994 general election using data from the Governor's race as it had the most votes."""

base_site = 'https://elections.sos.state.tx.us/elchist11_race833.htm' #1994 Governor's election results

r = requests.get(base_site)
r.status_code

tables = pd.read_html(r.text)

len(tables)

df_1994 = tables[0]
for col in df_1994.columns:
  print(col)
df_1994.columns = df_1994.columns.droplevel(0)
cols = [3,6]
df_1994.drop(df_1994.columns[cols],axis=1,inplace=True)
df_1994.columns = df_1994.columns.droplevel(0)
df_1994['Year'] = 1994
df_1994['Prez_Election'] = 0
for col in df_1994.columns:
  print(col)
df_1994.info()
df_1994

"""Repeat this process for the 1996 general election using data from the Presidential race as it had the most votes cast."""

base_site = 'https://elections.sos.state.tx.us/elchist56_race62.htm' #1996 Presidential election results

r = requests.get(base_site)
r.status_code

tables = pd.read_html(r.text)

len(tables)

"""For the 1996 data, it appears the columns no longer appear in the same order as the previous two elections. Specifically, the vote totals for the democratic candidates in the presidential election are no longer listed first. To fix this, a simple column rearrangement is completed by creating a list with the column names in the desired order and then creating a new dataframe which refernces the old dataframe using the list of column names. The resulting dataframe presents the columns in the correct order of: County, DEM, REP, Votes, Voters, Year."""

df_1996 = tables[0]
for col in df_1996.columns:
  print(col)
df_1996.columns = df_1996.columns.droplevel(0)
cols = [3,4,5,6,7,8,11]
df_1996.drop(df_1996.columns[cols],axis=1,inplace=True)
df_1996.columns = df_1996.columns.droplevel(0)
df_1996['Year'] = 1996
df_1996['Prez_Election'] = 1
for col in df_1996.columns:
  print(col)
df_1996.info()
new_columns = ['County', 'DEM', 'REP', 'Votes', 'Voters', 'Year', 'Prez_Election']
df_1996 = df_1996[new_columns]
df_1996

base_site = 'https://elections.sos.state.tx.us/elchist72_race833.htm' #1998 Governor's election results

r = requests.get(base_site)
r.status_code

tables = pd.read_html(r.text)

len(tables)

df_1998 = tables[0]
for col in df_1998.columns:
  print(col)
df_1998.columns = df_1998.columns.droplevel(0)
cols = [3,4,7]
df_1998.drop(df_1998.columns[cols],axis=1,inplace=True)
df_1998.columns = df_1998.columns.droplevel(0)
df_1998['Year'] = 1998
df_1998['Prez_Election'] = 0
for col in df_1998.columns:
  print(col)
df_1998.info()
new_columns = ['County', 'DEM', 'REP', 'Votes', 'Voters', 'Year', 'Prez_Election']
df_1998 = df_1998[new_columns]
df_1998

base_site = 'https://elections.sos.state.tx.us/elchist82_race62.htm' #2000 Presidential election results

r = requests.get(base_site)
r.status_code

tables = pd.read_html(r.text)

len(tables)

df_2000 = tables[0]
for col in df_2000.columns:
  print(col)
df_2000.columns = df_2000.columns.droplevel(0)
cols = [3,4,5,6,7,8,11]
df_2000.drop(df_2000.columns[cols],axis=1,inplace=True)
df_2000.columns = df_2000.columns.droplevel(0)
df_2000['Year'] = 2000
df_2000['Prez_Election'] = 1
for col in df_2000.columns:
  print(col)
df_2000.info()
new_columns = ['County', 'DEM', 'REP', 'Votes', 'Voters', 'Year', 'Prez_Election']
df_2000 = df_2000[new_columns]
df_2000

base_site = 'https://elections.sos.state.tx.us/elchist95_race833.htm' #2002 Governor's election results

r = requests.get(base_site)
r.status_code

tables = pd.read_html(r.text)

len(tables)

df_2002 = tables[0]
for col in df_2002.columns:
  print(col)
df_2002.columns = df_2002.columns.droplevel(0)
cols = [3,4,5,6,9]
df_2002.drop(df_2002.columns[cols],axis=1,inplace=True)
df_2002.columns = df_2002.columns.droplevel(0)
df_2002['Year'] = 2002
df_2002['Prez_Election'] = 0
for col in df_2002.columns:
  print(col)
df_2002.info()
new_columns = ['County', 'DEM', 'REP', 'Votes', 'Voters', 'Year', 'Prez_Election']
df_2002 = df_2002[new_columns]
df_2002

base_site = 'https://elections.sos.state.tx.us/elchist114_race62.htm' #2004 Presidential election results

r = requests.get(base_site)
r.status_code

tables = pd.read_html(r.text)

len(tables)

df_2004 = tables[0]
for col in df_2004.columns:
  print(col)
df_2004.columns = df_2004.columns.droplevel(0)
cols = [3,4,5,6,7,8,9,10,13]
df_2004.drop(df_2004.columns[cols],axis=1,inplace=True)
df_2004.columns = df_2004.columns.droplevel(0)
df_2004['Year'] = 2004
df_2004['Prez_Election'] = 1
for col in df_2004.columns:
  print(col)
df_2004.info()
new_columns = ['County', 'DEM', 'REP', 'Votes', 'Voters', 'Year', 'Prez_Election']
df_2004 = df_2004[new_columns]
df_2004

base_site = 'https://elections.sos.state.tx.us/elchist127_race833.htm' #2006 Governor's election results

r = requests.get(base_site)
r.status_code

tables = pd.read_html(r.text)

len(tables)

df_2006 = tables[0]
for col in df_2006.columns:
  print(col)
df_2006.columns = df_2006.columns.droplevel(0)
cols = [3,4,5,6,9]
df_2006.drop(df_2006.columns[cols],axis=1,inplace=True)
df_2006.columns = df_2006.columns.droplevel(0)
df_2006['Year'] = 2006
df_2006['Prez_Election'] = 0
for col in df_2006.columns:
  print(col)
df_2006.info()
new_columns = ['County', 'DEM', 'REP', 'Votes', 'Voters', 'Year', 'Prez_Election']
df_2006 = df_2006[new_columns]
df_2006

base_site = 'https://elections.sos.state.tx.us/elchist141_race62.htm' #2008 Presidential election results

r = requests.get(base_site)
r.status_code

tables = pd.read_html(r.text)

len(tables)

df_2008 = tables[0]
for col in df_2008.columns:
  print(col)
df_2008.columns = df_2008.columns.droplevel(0)
cols = [3,4,5,6,7,8,9,10,13]
df_2008.drop(df_2008.columns[cols],axis=1,inplace=True)
df_2008.columns = df_2008.columns.droplevel(0)
df_2008['Year'] = 2008
df_2008['Prez_Election'] = 1
for col in df_2008.columns:
  print(col)
df_2008.info()
new_columns = ['County', 'DEM', 'REP', 'Votes', 'Voters', 'Year', 'Prez_Election']
df_2008 = df_2008[new_columns]
df_2008

base_site = 'https://elections.sos.state.tx.us/elchist154_race833.htm' #2010 Governor's election results

r = requests.get(base_site)
r.status_code

tables = pd.read_html(r.text)

len(tables)

df_2010 = tables[0]
for col in df_2010.columns:
  print(col)
df_2010.columns = df_2010.columns.droplevel(0)
cols = [3,4,5,8]
df_2010.drop(df_2010.columns[cols],axis=1,inplace=True)
df_2010.columns = df_2010.columns.droplevel(0)
df_2010['Year'] = 2010
df_2010['Prez_Election'] = 0
for col in df_2010.columns:
  print(col)
df_2010.info()
new_columns = ['County', 'DEM', 'REP', 'Votes', 'Voters', 'Year', 'Prez_Election']
df_2010 = df_2010[new_columns]
df_2010

base_site = 'https://elections.sos.state.tx.us/elchist164_race62.htm' #2012 Presidential election results

r = requests.get(base_site)
r.status_code

tables = pd.read_html(r.text)

len(tables)

df_2012 = tables[0]
for col in df_2012.columns:
  print(col)
df_2012.columns = df_2012.columns.droplevel(0)
cols = [3,4,5,6,7,8,9,10,11,14]
df_2012.drop(df_2012.columns[cols],axis=1,inplace=True)
df_2012.columns = df_2012.columns.droplevel(0)
df_2012['Year'] = 2012
df_2012['Prez_Election'] = 1
for col in df_2012.columns:
  print(col)
df_2012.info()
new_columns = ['County', 'DEM', 'REP', 'Votes', 'Voters', 'Year', 'Prez_Election']
df_2012 = df_2012[new_columns]
df_2012

base_site = 'https://elections.sos.state.tx.us/elchist175_race833.htm' #2014 Governor's election results

r = requests.get(base_site)
r.status_code

tables = pd.read_html(r.text)

len(tables)

df_2014 = tables[0]
for col in df_2014.columns:
  print(col)
df_2014.columns = df_2014.columns.droplevel(0)
cols = [3,4,5,8]
df_2014.drop(df_2014.columns[cols],axis=1,inplace=True)
df_2014.columns = df_2014.columns.droplevel(0)
df_2014['Year'] = 2014
df_2014['Prez_Election'] = 0
for col in df_2014.columns:
  print(col)
df_2014.info()
new_columns = ['County', 'DEM', 'REP', 'Votes', 'Voters', 'Year', 'Prez_Election']
df_2014 = df_2014[new_columns]
df_2014

base_site = 'https://elections.sos.state.tx.us/elchist319_race62.htm' #2016 Presidential election results

r = requests.get(base_site)
r.status_code

tables = pd.read_html(r.text)

len(tables)

df_2016 = tables[0]
for col in df_2016.columns:
  print(col)
df_2016.columns = df_2016.columns.droplevel(0)
cols = [3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,20]
df_2016.drop(df_2016.columns[cols],axis=1,inplace=True)
df_2016.columns = df_2016.columns.droplevel(0)
df_2016['Year'] = 2016
df_2016['Prez_Election'] = 1
for col in df_2016.columns:
  print(col)
df_2016.info()
new_columns = ['County', 'DEM', 'REP', 'Votes', 'Voters', 'Year', 'Prez_Election']
df_2016 = df_2016[new_columns]
df_2016

base_site = 'https://elections.sos.state.tx.us/elchist331_race833.htm' #2018 Governor's election results

r = requests.get(base_site)
r.status_code

tables = pd.read_html(r.text)

len(tables)

df_2018 = tables[0]
for col in df_2018.columns:
  print(col)
df_2018.columns = df_2018.columns.droplevel(0)
cols = [3,6]
df_2018.drop(df_2018.columns[cols],axis=1,inplace=True)
df_2018.columns = df_2018.columns.droplevel(0)
df_2018['Year'] = 2018
df_2018['Prez_Election'] = 0
for col in df_2018.columns:
  print(col)
df_2018.info()
new_columns = ['County', 'DEM', 'REP', 'Votes', 'Voters', 'Year', 'Prez_Election']
df_2018 = df_2018[new_columns]
df_2018

df_full = df_1992.append(df_1994, ignore_index= True)
df_full = df_full.append(df_1996, ignore_index=True)
df_full = df_full.append(df_1998, ignore_index=True)
df_full = df_full.append(df_2000, ignore_index=True)
df_full = df_full.append(df_2002, ignore_index=True)
df_full = df_full.append(df_2004, ignore_index=True)
df_full = df_full.append(df_2006, ignore_index=True)
df_full = df_full.append(df_2008, ignore_index=True)
df_full = df_full.append(df_2010, ignore_index=True)
df_full = df_full.append(df_2012, ignore_index=True)
df_full = df_full.append(df_2014, ignore_index=True)
df_full = df_full.append(df_2016, ignore_index=True)
df_full = df_full.append(df_2018, ignore_index=True)

df_full = df_full[df_full.County != 'ALL COUNTIES'] #Drop totals by year
df_full['State'] = 'TX'
df_full['Voter_ID'] = [1 if x > 2013 else 0 for x in df_full['Year']]
df_full['Senate_2018'] = [1 if x == 2018 else 0 for x in df_full['Year']]
df_full['Dem_Percent'] = df_full['DEM']/df_full['Votes']
df_full['Rep_Percent'] = df_full['REP']/df_full['Votes']
df_full['Rep_Lean'] = df_full['Rep_Percent']-df_full['Dem_Percent']
df_full['Turnout'] = df_full['Votes']/df_full['Voters']

df_full

base_site = 'https://www.nrcs.usda.gov/wps/portal/nrcs/detail/national/home/?cid=nrcs143_013697'

r = requests.get(base_site)
r.status_code

tables = pd.read_html(r.text)

len(tables)

county_codes = tables[0]

for col in county_codes.columns:
  print(col)
print(county_codes)

county_codes = county_codes[:-1] #Need to drop artifact form webscraping
county_cols = ['FIPS', 'County', 'State']
county_codes.columns = county_cols
county_codes['County'] = county_codes['County'].str.upper()

county_codes

merged = pd.merge(df_full, county_codes, on=['County', 'State'], how='left')

null_test = pd.isnull(merged["FIPS"])
merged[null_test]

merged.loc[merged['County']== 'DEWITT', 'FIPS']= 48123
merged.loc[merged['County']== 'LASALLE', 'FIPS']= 48283

print(merged)

merged.to_csv(r'C:\Users\patri\Desktop\df_full.csv', index=False, header=True)
