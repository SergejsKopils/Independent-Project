#!/usr/bin/env python
# coding: utf-8

# In[1]:


pip install osmnx


# In[2]:


pip install folium


# In[3]:


from folium.plugins import HeatMap
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import osmnx as ox
import requests
import folium
import re


# This code is for a web scraping project. It gets data from a website about garages. The determine_category function decides the ad's type. It looks for words like 'Sell' or 'Buy' in the ad. The scrape_page function gets data from one webpage. It finds links to ads and gets details like price and location. The scrape_all_pages function does this for many pages. It collects data from each page on the website. The extract_numeric function gets numbers from text. It's used for turning price text into numbers. The code then puts all the data into a table using pandas. It changes dates and prices to a standard format. This makes the data easy to understand and analyze.

# In[5]:


import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

def determine_category(ad_soup):
    text = ad_soup.get_text()
    if 'Miscellaneous' in text:
        return 'Miscellaneous'
    elif 'Sell' in text:
        return 'Sell'
    elif 'Buy' in text:
        return 'Buy'
    elif 'Hand over' in text:
        return 'Hand over'
    elif 'Will remove' in text:
        return 'Will remove'
    elif 'Change' in text:
        return 'Change'
    return 'Unknown'

def scrape_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    ad_links = soup.find_all('a', class_='am')
    links = ['https://www.ss.com' + ad['href'] for ad in ad_links]

    page_data = []

    date_regex = re.compile(r'Date: (\d{2}\.\d{2}\.\d{4})')

    for link in links:
        ad_response = requests.get(link)
        ad_soup = BeautifulSoup(ad_response.text, 'html.parser')

        city_district_tag = ad_soup.find(string='City, district:')
        city_district = city_district_tag.find_next().text if city_district_tag else 'Not found'

        city_civil_parish_tag = ad_soup.find(string='City/civil parish:')
        city_civil_parish = city_civil_parish_tag.find_next().text if city_civil_parish_tag else 'Not found'

        street_tag = ad_soup.find(string='Street:')
        street = street_tag.find_next().text.replace('[Map]', '').strip() if street_tag else 'Not found'

        price_tag = ad_soup.find(string='Price:')
        price = price_tag.find_next().text if price_tag else 'Not found'

        date_match = date_regex.search(ad_soup.text)
        date = date_match.group(1) if date_match else 'Not found'

        category = determine_category(ad_soup)

        map_link = ad_soup.find('a', class_="ads_opt_link_map")
        if map_link and 'onclick' in map_link.attrs:
            onclick_text = map_link['onclick']
            coords = re.search(r'c=(\d+\.\d+),\s*(\d+\.\d+)', onclick_text)
            latitude = coords.group(1) if coords else 'Not found'
            longitude = coords.group(2) if coords else 'Not found'
        else:
            latitude = 'Not found'
            longitude = 'Not found'

        ad_data = {
            'City, district': city_district,
            'City/civil parish': city_civil_parish,
            'Street': street,
            'Price': price,
            'Category': category,
            'Date': date,
            'Latitude': latitude,
            'Longitude': longitude
        }

        page_data.append(ad_data)

    return page_data

def scrape_all_pages(base_url, num_pages):
    all_data = []
    for page in range(1, num_pages + 1):
        url = f"{base_url}page{page}.html"
        all_data.extend(scrape_page(url))
    return all_data

def extract_numeric(value):
    numbers = re.findall(r'\d+', value)
    return float(''.join(numbers)) if numbers else 0.0

# Main URL
base_url = 'https://www.ss.com/en/real-estate/premises/garages/all/'

# Scraping data from 20 page
data = scrape_all_pages(base_url, 20)

# Creating a pandas DataFrame from the scraped data
df_garages = pd.DataFrame(data)

# Converting 'Date' to Datetime Format
df_garages['Date'] = pd.to_datetime(df_garages['Date'], format='%d.%m.%Y')

# Applying 'extract_numeric' to the 'Price' Column and converting it to Numeric Type
df_garages['Price'] = df_garages['Price'].apply(extract_numeric)
df_garages['Price'] = pd.to_numeric(df_garages['Price'])


# The df_garages.dtypes command displays the data types of each column in the df_garages DataFrame.

# In[6]:


df_garages.dtypes


# Сode counts and prints the total number of collected advertisements from the scraped data.

# In[7]:


number_of_ads = len(data)
print(f"Total number of collected advertisements: {number_of_ads}")


# Сode finds and stores the highest price from the 'Price' column in the df_garages DataFrame.

# In[8]:


max_price = df_garages['Price'].max()
max_price


# Сode filters the df_garages DataFrame to only include rows where the 'Price' is 100,000 or less.

# In[9]:


df_garages_filtered = df_garages[df_garages['Price'] <= 100000]
df_garages_filtered


# Сode counts and prints the number of advertisements in each category from the filtered df_garages_filtered DataFrame.

# In[10]:


category_counts = df_garages_filtered['Category'].value_counts()
print("Number of ads in each category:")
print(category_counts)


# Сode calculates and prints descriptive statistics, including the median, for the 'Price' column in the filtered df_garages_filtered DataFrame.

# In[11]:


price_stats = df_garages_filtered['Price'].describe()
print("Descriptive statistics of prices:")
print(price_stats)

median_price = df_garages_filtered['Price'].median()
print("\nMedian of prices:")
print(median_price)


# Сode loops through specified categories, filtering the DataFrame for each and then calculates and prints descriptive statistics and the median of prices for each category.

# In[12]:


categories = ['Miscellaneous', 'Sell', 'Buy', 'Hand over', 'Will remove', 'Change']

for category in categories:
    print(f"\n--- {category} Category ---")

    # Filter the DataFrame for the current category
    df_category = df_garages_filtered[df_garages_filtered['Category'] == category]

    # Descriptive statistics for the 'Price' column in the current category
    price_stats = df_category['Price'].describe()
    print("\nDescriptive statistics of prices:")
    print(price_stats)

    # Median of the 'Price' column in the current category
    median_price = df_category['Price'].median()
    print("\nMedian of prices:")
    print(median_price)


# Сode creates a copy of the DataFrame, formats dates, filters for 'Sell' category, and plots a line graph showing the average price trend over time in this category.

# In[13]:


# Create a copy of the DataFrame to avoid the SettingWithCopyWarning warning
df_garages_filtered_copy = df_garages_filtered.copy()

# Convert the 'Date' column to the correct date format
df_garages_filtered_copy['Date'] = pd.to_datetime(df_garages_filtered_copy['Date'])

# Filter the DataFrame for the 'Sell' category
df_sell = df_garages_filtered_copy[df_garages_filtered_copy['Category'] == 'Sell']

# Plot a graph for the price trend in the 'Sell' category
df_sell.groupby('Date')['Price'].mean().plot(kind='line', figsize=(15, 9))
plt.title('Price Trend Over Time for Sell Category')
plt.xlabel('Date')
plt.ylabel('Average Price')
plt.show()


# Сode creates a copy of the DataFrame, formats dates, filters for the 'Hand over' category, and plots a line graph illustrating the average price trend over time in this category.

# In[14]:


# Create a copy of the DataFrame to avoid the SettingWithCopyWarning warning
df_garages_filtered_copy = df_garages_filtered.copy()

# Convert the 'Date' column to the correct date format
df_garages_filtered_copy['Date'] = pd.to_datetime(df_garages_filtered_copy['Date'])

# Filter the DataFrame for the 'Hand over' category
df_hand_over = df_garages_filtered_copy[df_garages_filtered_copy['Category'] == 'Hand over']

# Plot a graph for the price trend in the 'Hand over' category
df_hand_over.groupby('Date')['Price'].mean().plot(kind='line', figsize=(15, 9))
plt.title('Price Trend Over Time for Hand over Category')
plt.xlabel('Date')
plt.ylabel('Average Price')
plt.show()


# This code calculates and prints the average price per street in the 'Street' column of the df_garages_filtered DataFrame.

# In[15]:


average_price_per_district = df_garages_filtered.groupby('Street')['Price'].mean()
print(average_price_per_district)


# Сode calculates and prints the count of advertisements per street in the 'Street' column of the df_garages_filtered DataFrame.

# In[16]:


ads_count_per_district = df_garages_filtered['Street'].value_counts()
print(ads_count_per_district)


# Сode counts and prints the number of advertisements for each value in the 'City, district' column of the df_garages_filtered DataFrame.

# In[17]:


ad_counts = df_garages_filtered['City, district'].value_counts()
print(ad_counts)


# Code creates a bar chart showing the average garage price per street in Riga using data from the average_price_per_district series.

# In[18]:


average_price_per_district.plot(kind='bar', figsize=(20, 12))
plt.title('Average Garage Price per Street in Riga')
plt.xlabel('Street')
plt.ylabel('Average Price')
plt.xticks(rotation=90, fontsize=6)
plt.show()


# This code calculates the overall average garage price for the 'Riga' district in the df_garages_filtered DataFrame and adds a horizontal red line at that average price on the existing bar chart depicting the average price per street in Riga.

# In[19]:


# Calculate the overall average price for the 'Riga' district
overall_average_price = df_garages_filtered['Price'].mean()

# Your existing code to plot the bar chart
average_price_per_district.plot(kind='bar', figsize=(20, 12))
plt.title('Average Garage Price per Street in Riga')
plt.xlabel('Street')
plt.ylabel('Average Price')
plt.xticks(rotation=90, fontsize=6)

# Add a horizontal red line at the overall average price
plt.axhline(y=overall_average_price, color='r', linestyle='-', linewidth=2)

plt.show()


# This code, assuming df_garages_filtered is filtered for Riga, first filters data for the 'Sell' and 'Hand over' categories, calculates the overall average price for the 'Riga' district, and the average price for the 'Hand over' category. It then creates subplots for both categories, plotting the average garage prices per street, and adds horizontal red lines at the overall average price and the average price for 'Hand over' to both subplots for comparison.

# In[20]:


# Filter data for 'Sell' category
sell_data = df_garages_filtered[df_garages_filtered['Category'] == 'Sell']

# Filter data for 'Hand over' category
hand_over_data = df_garages_filtered[df_garages_filtered['Category'] == 'Hand over']

# Calculate the overall average price for the 'Riga' district
overall_average_price = df_garages_filtered['Price'].mean()

# Calculate the average 'Price' for the 'Hand over' category
average_price_hand_over = hand_over_data['Price'].mean()

# Create subplots for 'Sell' and 'Hand over' categories
fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(20, 12))

# Plot for 'Sell' category
sell_data.groupby('Street')['Price'].mean().plot(kind='bar', ax=axes[0])
axes[0].set_title('Average Garage Price for "Sell" in Riga')
axes[0].set_xlabel('Street')
axes[0].set_ylabel('Average Price')
axes[0].tick_params(axis='x', rotation=90)

# Plot for 'Hand over' category
hand_over_data.groupby('Street')['Price'].mean().plot(kind='bar', ax=axes[1])
axes[1].set_title('Average Garage Price for "Hand over" in Riga')
axes[1].set_xlabel('Street')
axes[1].set_ylabel('Average Price')
axes[1].tick_params(axis='x', rotation=90)

# Add a horizontal red line at the overall average price to both subplots
axes[0].axhline(y=overall_average_price, color='r', linestyle='-', linewidth=2)
axes[1].axhline(y=average_price_hand_over, color='r', linestyle='-', linewidth=2)  # Use average price for 'Hand over'

plt.tight_layout()
plt.show()


# This code filters data for the 'Sell' and 'Hand over' categories, then creates two histograms to visualize the price distributions for each category, with the first histogram showing the distribution for 'Sell' in green and the second for 'Hand over' in red.

# In[21]:


# Filter data for 'Sell' category
sell_data = df_garages_filtered[df_garages_filtered['Category'] == 'Sell']

# Filter data for 'Hand over' category
hand_over_data = df_garages_filtered[df_garages_filtered['Category'] == 'Hand over']

# Create histograms
plt.figure(figsize=(12, 6))

# Histogram for 'Sell' category
plt.subplot(1, 2, 1)  # 1 row, 2 columns, 1st subplot
sns.histplot(sell_data['Price'], kde=True, color='green', bins=30)
plt.title('Distribution of Prices for Sell')
plt.xlabel('Price')
plt.ylabel('Frequency')

# Histogram for 'Hand over' category
plt.subplot(1, 2, 2)  # 1 row, 2 columns, 2nd subplot
sns.histplot(hand_over_data['Price'], kde=True, color='red', bins=30)
plt.title('Distribution of Prices for Hand over')
plt.xlabel('Price')
plt.ylabel('Frequency')

plt.tight_layout()
plt.show()


# Assuming df_garages_filtered contains 'Price', 'Category', and 'City, district' columns, filters data for 'City, district' as 'Riga', then further narrows it down to 'Sell' and 'Hand over' categories within Riga, and finally creates histograms to visualize the price distributions for both categories within Riga, with the first histogram showing the distribution for 'Sell' in green and the second for 'Hand over' in red.

# In[22]:


# Filtering data for 'City, district' as 'Riga'
riga_data = df_garages_filtered[df_garages_filtered['City, district'] == 'Riga']

# Further filtering for 'Sell' and 'Hand over' categories within Riga
sell_data_riga = riga_data[riga_data['Category'] == 'Sell']
hand_over_data_riga = riga_data[riga_data['Category'] == 'Hand over']

# Creating histograms for 'Sell' and 'Hand over' in Riga
plt.figure(figsize=(12, 6))

# Histogram for 'Sell' category in Riga
plt.subplot(1, 2, 1)
sns.histplot(sell_data_riga['Price'], kde=True, color='green', bins=30)
plt.title('Distribution of Prices for Sell in Riga')
plt.xlabel('Price')
plt.ylabel('Frequency')

# Histogram for 'Hand over' category in Riga
plt.subplot(1, 2, 2)
sns.histplot(hand_over_data_riga['Price'], kde=True, color='red', bins=30)
plt.title('Distribution of Prices for Hand over in Riga')
plt.xlabel('Price')
plt.ylabel('Frequency')

plt.tight_layout()
plt.show()


# The DataFrame is filtered to include only advertisements from Riga, and then a predefined list of categories is looped through to analyze each category's price statistics and median in Riga, with a check to ensure data availability for each category before printing the insights.

# In[23]:


# Filtering the DataFrame for advertisements from Riga
df_riga = df_garages_filtered[df_garages_filtered['City, district'] == 'Riga']

# Predefined list of categories
categories = ['Miscellaneous', 'Sell', 'Buy', 'Hand over', 'Will remove', 'Change']

for category in categories:
    print(f"\n--- {category} Category in Riga ---")

    # Filtering the DataFrame for the current category
    df_category = df_riga[df_riga['Category'] == category]

    # Checking if there is data in the category
    if not df_category.empty:
        # Descriptive statistics for the 'Price' column in the current category
        price_stats = df_category['Price'].describe()
        print("\nDescriptive statistics of prices:")
        print(price_stats)

        # Median of the 'Price' column in the current category
        median_price = df_category['Price'].median()
        print("\nMedian of prices:")
        print(median_price)
    else:
        print("No data in this category.")


# Data is filtered to include only advertisements from 'Riga' and belonging to the 'Sell' and 'Hand over' categories. The data is then grouped by 'City/civil parish' and 'Category' to calculate the mean 'Price,' which is visualized as a bar chart showing the average price by city/civil parish and category in Riga.

# In[24]:


# Filter data for 'City, district' as 'Riga' and for 'Category' as 'Sell' and 'Hand over'
riga_data = df_garages_filtered[(df_garages_filtered['City, district'] == 'Riga') & 
                                (df_garages_filtered['Category'].isin(['Sell', 'Hand over']))]

# Group data by 'City/civil parish' and 'Category', then calculate the mean 'Price'
grouped_data = riga_data.groupby(['City/civil parish', 'Category'])['Price'].mean().unstack()

# If there's no data for some combinations, fill with 0
grouped_data = grouped_data.fillna(0)

# Setup for bar chart
parishes = grouped_data.index
x = np.arange(len(parishes))  # the label locations
width = 0.35  # the width of the bars

# Create a larger figure
fig, ax = plt.subplots(figsize=(19.2, 14.4))

# Creating bars for each category
rects1 = ax.bar(x - width/2, grouped_data['Sell'], width, label='Sell')
rects2 = ax.bar(x + width/2, grouped_data['Hand over'], width, label='Hand over')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Average Price', fontsize=20)
ax.set_title('Average Price by City/Civil Parish and Category in Riga', fontsize=20)
ax.set_xticks(x)
ax.set_xticklabels(parishes, rotation=90, fontsize=16)
ax.legend()

# Add bar labels
ax.bar_label(rects1, padding=3, fontsize=12)
ax.bar_label(rects2, padding=3, fontsize=12)

fig.tight_layout()
plt.show()


# In this code, data from the df_garages_filtered DataFrame is assigned to the variable adv_data_Latvia. Color codes for different categories are defined, and the road network for 'Latvia' is retrieved using OSMnx. The code then plots a map displaying road networks and garage locations, color-coded by category, and includes a legend to distinguish between different categories.

# In[28]:


adv_data_Latvia = df_garages_filtered

# Define colors for each category
category_colors = {
    'Miscellaneous': 'blue',
    'Sell': 'green',
    'Buy': 'red',
    'Hand over': 'purple',
    'Will remove': 'orange',
    'Change': 'cyan',
}

# Specify the place name
place_name = "Latvia"

# Retrieve the road network for the specified place
G = ox.graph_from_place(place_name, network_type='drive')

# Plot the map with roads and garage locations
fig, ax = ox.plot_graph(G, figsize=(40, 40), show=False, close=False, node_size=0, edge_linewidth=0.5)

# Add garage locations to the map with color coding for categories
for _, row in adv_data_Latvia.iterrows():
    if pd.notna(row['Longitude']) and pd.notna(row['Latitude']) and pd.notna(row['Category']):
        category = row['Category']
        if category in category_colors:
            color = category_colors[category]
            ax.scatter(row['Longitude'], row['Latitude'], c=color, s=50, label=category)
            
# Set global font size
plt.rcParams.update({'font.size': 22})                  
            
# Create a legend with unique labels
handles, labels = plt.gca().get_legend_handles_labels()
by_label = dict(zip(labels, handles))
ax.legend(by_label.values(), by_label.keys(), loc='best')

plt.show()


# Data from the df_garages_filtered DataFrame is assigned to the variable adv_data_Riga. Color codes for different categories are defined, and the road network for 'Riga, Latvia' is retrieved using OSMnx, along with building data for the same location. The code then plots a map displaying road networks, garage locations (color-coded by category), and buildings in Riga, with a legend to distinguish between different categories.

# In[29]:


adv_data_Riga = df_garages_filtered

# Define colors for each category
category_colors = {
    'Miscellaneous': 'blue',
    'Sell': 'green',
    'Buy': 'red',
    'Hand over': 'purple',
    'Will remove': 'orange',
    'Change': 'cyan',
}

# Specify the place name
place_name = "Riga, Latvia"

# Retrieve the road network for the specified place
G = ox.graph_from_place(place_name, network_type='drive')

# Retrieve buildings in the specified place
buildings = ox.geometries_from_place(place_name, tags={'building': True})

# Plot the map with roads, garage locations, and buildings
fig, ax = ox.plot_graph(G, figsize=(40, 40), show=False, close=False, node_size=0, edge_linewidth=0.5)

# Add garage locations to the map with color coding for categories
for _, row in adv_data_Riga.iterrows():
    if pd.notna(row['Longitude']) and pd.notna(row['Latitude']) and pd.notna(row['Category']):
        category = row['Category']
        if category in category_colors:
            color = category_colors[category]
            ax.scatter(row['Longitude'], row['Latitude'], c=color, s=50, label=category)

# Set global font size
plt.rcParams.update({'font.size': 22})      
            
# Plot buildings on the map
buildings.plot(ax=ax, facecolor='khaki', alpha=0.7)

# Create a legend with unique labels
handles, labels = plt.gca().get_legend_handles_labels()
by_label = dict(zip(labels, handles))
ax.legend(by_label.values(), by_label.keys(), loc='best')

plt.show()


# In this code, rows in the df_garages_filtered DataFrame where 'Latitude' or 'Longitude' is not a valid number are filtered out, and then 'Latitude' and 'Longitude' columns are converted to numeric values. The code prepares the data for a heatmap and generates a Folium map centered around the central point of the garage locations, with a heatmap layer representing the geographic distribution of the garages.

# In[27]:


# Filter out rows where 'Latitude' or 'Longitude' is not a valid number
df_garages_filtered = df_garages_filtered[pd.to_numeric(df_garages_filtered['Latitude'], errors='coerce').notnull()]
df_garages_filtered = df_garages_filtered[pd.to_numeric(df_garages_filtered['Longitude'], errors='coerce').notnull()]

# Convert 'Latitude' and 'Longitude' to numeric values
df_garages_filtered['Latitude'] = pd.to_numeric(df_garages_filtered['Latitude'])
df_garages_filtered['Longitude'] = pd.to_numeric(df_garages_filtered['Longitude'])

# Prepare the data for the heatmap
heatmap_data = df_garages_filtered[['Latitude', 'Longitude']].values.tolist()

# Calculate the central point
central_latitude = df_garages_filtered['Latitude'].mean()
central_longitude = df_garages_filtered['Longitude'].mean()
central_point = {'Latitude': central_latitude, 'Longitude': central_longitude}

# Create a map centered around the central point
folium_map = folium.Map(location=[central_point['Latitude'], central_point['Longitude']], zoom_start=12)

# Add a heatmap layer
HeatMap(heatmap_data).add_to(folium_map)

folium_map

