#!/usr/bin/env python
# coding: utf-8

# # Python for Data Analytics

# ## Independent Project Guidelines

# Data analytics project is a showcase of your skills on data processing using Python. Main stages of the project:
# 
# 1. __Selection of your research data set__
# 
# Selection can be based on your profesional activities (preferred), personal side projects, hobbies, or just pure curiosity.
# 
# 2. __Organising a Jupiter notebook that will be used for all operations and the project report__
# 
# For brevity reasons, the report is limited by 2000 words (excl. source codes)
# 
# 3. __Data collection__
# 
# This is preferable to organise data collection from the notebook - e.g., downloading of data from open sources. If the data set are not public or not available for automatic collection, then this is allowed to use local files for loading.
# 
# 4. __Business understanding__
# 
# Describe potential applications of the data set - how and for which purposes it can be used.
# 
# 5. __Loading the data set__
# 
# The data set can be heterogeneous and include numeric data, text fragments, images, etc. This is highly recommended to use NumPy, Pandas and/or pure Python data structures to highlight your skills on these libraries
# 
# 6. __Data understanding / visualisation__
# 
# This is recommended to use Matplotlib/Seaborn for visualising your data set. Note that your plots should tell the story - supplement them with interesting conclusions/insights
# 
# 7. __Data preparation__
# 
# Data clean up, transformation, indexing, aggreagation, etc. - everything you need for further stages
# 
# 8. __Data modelling (optional)__
# 
# Illustrate solution of one of the stated business problems using the loaded data set. The possible solution require modelling, which will be mainly covered by next study courses, so this is optional at the moment.
# 

# ## Project Examples
# 
# Using your own data set is the preferred option, but if you have no ideas  - use one of the recommendations below.

# ### General Transit Feed Specification (GTFS) data
# 
# GTFS defines a common format for public transportation schedules and associated geographic information. This format is used by many public transport operators to publish schedule information - e.g., Rigas Satiksme https://data.gov.lv/dati/lv/dataset/marsrutu-saraksti-rigas-satiksme-sabiedriskajam-transportam
# 
# The data format is quite complicated, but opens a wide range of applications

# ### Public Transport smart card data
# 
# Registration data of smart cards is another valuable source of information. This is publicly available in Riga (e.g., Rigas Satiksme https://data.gov.lv/dati/lv/dataset/e-talonu-validaciju-dati-rigas-satiksme-sabiedriskajos-transportlidzeklos) and has a relatively simple format.

# ### Regional statistics
# 
# Regional statistic data covers a lot of indicators - economic, social, demographic, etc. has a large potential for visualisation and trends. The data for Latvia is provided here https://data.gov.lv/eng, but for other countries are also publicly available.

# ### Regional statistics
# 
# Regional statistic data covers a lot of indicators - economic, social, demographic, etc. has a large potential for visualisation and trends. The data for Latvia is provided here https://data.gov.lv/eng, but for other countries are also publicly available.

# ### Web scrapping: Wikipedia
# 
# Wikipedia is a perfect source of textual data, available for automatic scrapping. It is primarily used for text mining, but also a great source for visualising activities, trends, or just a source for specific information (e.g., a bot for finding dates of births from famous person's Wiki articles)

# ### Web scrapping: Market
# 
# If you are interested in market analysis (e.g., real estate, cars, etc.), you can collect data from a website of private advertisements.
# 
# Please avoid scrapping personal data and intellectual property.

# ### World Statistics
# 
# There is a wide vareity of data sources on global processes in our world - population, migration, spread of deseases, etc. E.g., Our World in Data https://ourworldindata.org/ is a great collection of data sets for visualisation and analysis.

# ### Social Networks
# 
# Many social networks provide APIs for automatic data collection - e.g., Twitter or Facebook API. In addition to textual and image analysis, social networks cen be used for monitoring trends, etc.

# ### Airbnb open data
# 
# Airbnb's open API lets you extract data on Airbnb stays from the public website. Data includes all the information needed to find out more about hosts and geographical availability, both of which are necessary metrics to make predictions and draw conclusions.

# ## Final notes

# In addition to the provided report, the project require a short presentation (max. 7 minutes) to your group mates, describing data set, steps of data processing and most interesting results.
