import pandas as pd

# import dataframes

famous_places_df = pd.read_csv("Cleaned Data/clean_famous_places") # famous places with locations and best travel times
euro_destinations_df = pd.read_csv("Cleaned Data/clean_euro_destinations") #euro destinations with descriptions, and best travel times
travel_destinations_df = pd.read_csv("Cleaned Data/clean_travel_destinations") # categorized cities and countries with best travel times
travel_details_df = pd.read_csv("Cleaned Data/clean_travel_details") # city and country, with costs and travel types
worldwide_travel_cities_df = pd.read_csv("Cleaned Data/clean_worldwide_travel_cities") # city country with category ratings, descriptions, avg monthly temp, and budget level


#drop unnamed columns
worldwide_travel_cities_df = worldwide_travel_cities_df.loc[:, ~worldwide_travel_cities_df.columns.str.contains('Unnamed')]
travel_details_df = travel_details_df.loc[:, ~travel_details_df.columns.str.contains('Unnamed')]
travel_destinations_df = travel_destinations_df.loc[:, ~travel_destinations_df.columns.str.contains('Unnamed')]
euro_destinations_df = euro_destinations_df.loc[:, ~euro_destinations_df.columns.str.contains('Unnamed')]
famous_places_df = famous_places_df.loc[:, ~famous_places_df.columns.str.contains('Unnamed')]

# drop lat and lng from all datasets except one 
#europe_hotel_reviews_df = europe_hotel_reviews_df.drop(columns=["lat", "lng"])
travel_details_df = travel_details_df.drop(columns=["lat", "lng"])
travel_destinations_df = travel_destinations_df.drop(columns=["lat", "lng"])
euro_destinations_df = euro_destinations_df.drop(columns=["Latitude", "Longitude"])
famous_places_df = famous_places_df.drop(columns=["lat", "lng"])

# aggregate datasets
agg_famousplaces_df = famous_places_df.groupby(['City', 'Country']).agg({'Entry_Fee_USD' : 'mean', 'Place_Name' : 'count'}).reset_index()
agg_famousplaces_df.rename(columns={'Entry_Fee_USD' : 'avg_attraction_fee', 'Place_Name' : 'num_attractions'}, inplace=True)

agg_traveldetails_df = travel_details_df.groupby(['City', 'Country']).agg({'Duration (days)': 'mean', 'Accommodation cost': 'mean', 'Transportation cost': 'mean'}).reset_index()
agg_traveldetails_df.rename(columns={'Duration (days)': 'avg_trip_duration', 'Accommodation cost': 'avg_accommodation_cost', 'Transportation cost': 'avg_transport_cost'}, inplace=True)

agg_traveldest_df = travel_destinations_df.drop_duplicates(subset=['City', 'Country'], keep='first')

################# merge all datasets together

# add worldwide travel cities df 
merged_df = worldwide_travel_cities_df.copy()

# add travel details df 
merged_df = merged_df.merge(agg_traveldetails_df, on=["City", "Country"], how = "left")

# add travel destinations df 
merged_df = merged_df.merge(agg_traveldest_df, on=["City", "Country"], how = "left")

# add famous places df
merged_df = merged_df.merge(agg_famousplaces_df, on=["City", "Country"], how="left")

# add euro destinations
merged_df = merged_df.merge(euro_destinations_df, on=["City", "Country"], how="left")


# drop columns
merged_df = merged_df.drop(columns=['Category_y', 'Best_Month'])

# drop duplicates in merged_df
merged_df = merged_df.drop_duplicates(subset={'City', 'Country'}, keep='first')

print(merged_df.head())

merged_df.to_csv("Cleaned Data/merged_data.csv")


