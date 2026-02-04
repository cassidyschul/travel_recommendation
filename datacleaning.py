
import pandas as pd
import ast
from datetime import date
import json

################## world cities (csv of cities and country with lat and lng ##################

city_country_df = pd.read_csv("Raw Data/worldcities.csv")


################## europe hotel reviews ##################

europe_hotel_reviews_df = pd.read_csv("Raw Data/europe_hotel_reviews.csv")

# change review date to date datatype
europe_hotel_reviews_df["Review_Date"] = pd.to_datetime(europe_hotel_reviews_df["Review_Date"], format="%m/%d/%y")

# convert tags to list datatype & clean whitespaces
europe_hotel_reviews_df["Tags"] = europe_hotel_reviews_df["Tags"].apply(ast.literal_eval)
europe_hotel_reviews_df["Tags"] = europe_hotel_reviews_df["Tags"].apply(lambda tags: [t.strip().lower() for t in tags])

#drop unwanted columns
europe_hotel_reviews_df = europe_hotel_reviews_df.drop(columns=["Additional_Number_of_Scoring", "Total_Number_of_Reviews_Reviewer_Has_Given"])

#strip white space in str columns 
europe_hotel_reviews_df = europe_hotel_reviews_df.apply(lambda x: x.str.strip() if x.dtype == "string" else x)
europe_hotel_reviews_df["days_since_review"] = europe_hotel_reviews_df["days_since_review"].str.rstrip(" days").astype(int)

# break address in address, city and country
europe_hotel_reviews_df[["Hotel_Address", "Hotel_City", "Hotel_Country"]] = europe_hotel_reviews_df["Hotel_Address"].str.rsplit(" ", n=2, expand = True)



################## worldwide travel cities ##################

worldwide_travel_cities_df = pd.read_csv("Raw Data/Worldwide Travel Cities Dataset.csv")

# drop id column
worldwide_travel_cities_df = worldwide_travel_cities_df.drop(columns=['id'])

# change column names
worldwide_travel_cities_df = worldwide_travel_cities_df.rename(columns={"latitude" : "lat", "longitude": "lng"})

# replace values
worldwide_travel_cities_df["region"] = worldwide_travel_cities_df["region"].replace({"north_america": "north america", "south_america": "south america"})

# change ideal durations to list datatype
worldwide_travel_cities_df["ideal_durations"] = worldwide_travel_cities_df["ideal_durations"].apply(ast.literal_eval)

worldwide_travel_cities_df['avg_temp_monthly'] = worldwide_travel_cities_df["avg_temp_monthly"].apply(json.loads)

################## travel details ##################

travel_details_df = pd.read_csv("Raw Data/travel details.csv")

#drop any NAs
travel_details_df = travel_details_df.dropna()

# clean costs
travel_details_df[["Accommodation cost", "Transportation cost"]] = travel_details_df[["Accommodation cost", "Transportation cost"]].apply(
    lambda x: x.str.strip("$").str.strip("USD").str.strip().str.replace(",", "")
)

# split destination by city and country and clean
travel_details_df[["City", "Country"]] = travel_details_df["Destination"].str.split(",", n=1, expand = True)
travel_details_df[["City", "Country"]] = travel_details_df[["City", "Country"]].apply(
    lambda x: x.str.strip()
)
travel_details_df["Country"] = travel_details_df["Country"].replace({"UK": "United Kingdom", "USA": "United States", "SA": "South Africa", "Hawaii" : "United States"})
travel_details_df["City"] = travel_details_df["City"].replace({"New York City": "New York", "Hawaii" : "Honolulu", "Bali" : "Denpasar", "Cancun" : "Cancún"})

# handle records that only have country or city as destinated
countries = set(city_country_df["country"].str.strip().str.lower())

missing_country = travel_details_df["Country"].isna()


is_country = travel_details_df.loc[missing_country, "City"].str.lower().isin(countries)

# move countries
travel_details_df.loc[missing_country & is_country, "Country"] = travel_details_df.loc[missing_country & is_country, "City"]
travel_details_df.loc[missing_country & is_country, "City"] = None


# change datatypes 
travel_details_df[["Duration (days)", "Traveler age"]] = travel_details_df[["Duration (days)", "Traveler age"]].astype(int)
travel_details_df[["Accommodation cost", "Transportation cost"]] = travel_details_df[["Accommodation cost", "Transportation cost"]].astype(float)
travel_details_df[["Start date", "End date"]] = travel_details_df[["Start date", "End date"]].apply(
    lambda x: pd.to_datetime(x, format="%m/%d/%y")
)


# merge with city_country_df to get lat, lng and country
merged_travel_details_df = travel_details_df.merge(
    city_country_df[["city", "country", "lat", "lng"]],
    left_on = "City",
    right_on = "city",
    how = "left"
    )

# override country location for specific cities
cities_override = {
    "London" : "United Kingdom",
    "Barcelona" : "Spain",
    "Paris": "France",
    "Rome": "Italy"}

cities_to_override = merged_travel_details_df["City"].isin(cities_override.keys())

# Only update Country
merged_travel_details_df.loc[cities_to_override, "Country"] = merged_travel_details_df.loc[cities_to_override, "City"].replace(cities_override)


# map cities with multiple countries
merged_travel_details_df["Country"] = merged_travel_details_df["Country"].fillna(merged_travel_details_df["country"])


# drop trip ID and destination
merged_travel_details_df = merged_travel_details_df.drop(columns=["Trip ID", "Destination", "Traveler name", "country", "city"])

print(merged_travel_details_df.head())
