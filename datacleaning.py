
import pandas as pd
import ast
from datetime import date
import json
import os

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

# to csv
europe_hotel_reviews_df.to_csv("Cleaned Data/clean_europe_hotel_reviews")


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

# change avg_temp_monthly to dictionary datatype
worldwide_travel_cities_df['avg_temp_monthly'] = worldwide_travel_cities_df["avg_temp_monthly"].apply(json.loads)

# to csv
worldwide_travel_cities_df.to_csv("Cleaned Data/clean_worldwide_travel_cities")

################## travel details ##################

travel_details_df = pd.read_csv("Raw Data/travel details.csv")

#drop any NAs
travel_details_df = travel_details_df.dropna()

# clean costs
travel_details_df[["Accommodation cost", "Transportation cost"]] = travel_details_df[["Accommodation cost", "Transportation cost"]].apply(
    lambda x: x.str.strip("$").str.strip("USD").str.strip().str.replace(",", "")
)

# split destination by city and country and clean
travel_details_df[["City", "Country"]] = travel_details_df["Destination"].str.split(",", expand = True)
travel_details_df[["City", "Country"]] = travel_details_df[["City", "Country"]].apply(
    lambda x: x.str.strip()
)
travel_details_df["Country"] = travel_details_df["Country"].replace({"UK": "United Kingdom", "USA": "United States", "SA": "South Africa", "Hawaii" : "United States"})
travel_details_df["City"] = travel_details_df["City"].replace({"New York City": "New York", "Hawaii" : "Honolulu", "Bali" : "Denpasar"})

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
    city_country_df[["city_ascii", "country", "lat", "lng"]],
    left_on = "City",
    right_on = "city_ascii",
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
merged_travel_details_df = merged_travel_details_df.drop(columns=["Trip ID", "Destination", "Traveler name", "country", "city_ascii"])

# to csv
merged_travel_details_df.to_csv("Cleaned Data/clean_travel_details")

################## travel destinations ##################

travel_destinations_df = pd.read_csv("Raw Data/travel_destinations.csv")

# remove parenthesis on best time to travel
travel_destinations_df["Best_Time_to_Travel"] = travel_destinations_df["Best_Time_to_Travel"].str.split("(").str[0].str.strip()

# change Category and best time to travel to lists
travel_destinations_df["Category"] = travel_destinations_df["Category"].apply(lambda x: [x])
travel_destinations_df["Best_Time_to_Travel"] = travel_destinations_df["Best_Time_to_Travel"].apply(lambda x: [x])

# rename cities and countries
travel_destinations_df["Country"] = travel_destinations_df["Country"].replace({"USA": "United States"})
travel_destinations_df["City"] = travel_destinations_df["City"].replace({"New York City": "New York", "Bali (Denpasar/Ubud)": "Denpasar", "Bogotá": "Bogota", "Medellín": "Medellin"})
travel_destinations_df.loc[travel_destinations_df["City"] == "Hong Kong", "Country"] = "Hong Kong"

# merge with city country to get lat & lng
merged_travel_destinations_df = travel_destinations_df.merge(
    city_country_df[["city_ascii", "country", "lat", "lng"]],
    left_on = ["City", "Country"],
    right_on = ["city_ascii", "country"],
    how = "left"
    )

#drop unwanted columns
merged_travel_destinations_df = merged_travel_destinations_df.drop(columns=["city_ascii", "country"])

# to csv
merged_travel_destinations_df.to_csv("Cleaned Data/clean_travel_destinations")

################## famous places ##################

famous_places_df = pd.read_csv("Raw Data/famous_places.csv")

#rename cities
famous_places_df["City"] = famous_places_df["City"].replace({"New York City": "New York", "Cusco Region": "Cusco", "Arizona": "Flagstaff", "Beijing/Multiple": "Beijing"})

#rename months to match other dataset months
famous_places_df["Best_Visit_Month"] = famous_places_df["Best_Visit_Month"].replace({"March": "Mar", "June": "Jun", "July": "Jul", "Sept": "Sep"}, regex=True) #regex = True to change portions of string

# convert months into a list
months = ["Jan","Feb","Mar","Apr","May","Jun", "Jul","Aug","Sep","Oct","Nov","Dec"]

def updated_best_time(best_time):
    months_list = []

    # convert input to a string, if currently a list (euro_destinations best month)
    if isinstance(best_time, list):
        best_time = "/".join(best_time)

    for x in best_time.split("/"): # split by / 
        first_month, last_month = x.split("-") # split by -
        first_index = months.index(first_month)
        last_index = months.index(last_month)

        # add each month the months_list based on index, handle ranges that occur in two separate years (Oct-March)
        if first_index <= last_index:
            months_list.extend(months[first_index:last_index+1])
        else:
            months_list.extend(months[first_index:] + months[:last_index+1])
    return months_list


famous_places_df["Best_Visit_Month"] = famous_places_df["Best_Visit_Month"].apply(updated_best_time)

#merge with city_country to get lat and lng of records
merged_famous_places_df = famous_places_df.merge(
    city_country_df[["city_ascii", "country", "lat", "lng"]],
    left_on = ["City", "Country"],
    right_on = ["city_ascii", "country"],
    how = "left"
)

#drop unwanted columns
merged_famous_places_df = merged_famous_places_df.drop(columns=["Annual_Visitors_Millions", "UNESCO_World_Heritage", "Year_Built", "Tourism_Revenue_Million_USD", "Average_Visit_Duration_Hours", "city_ascii", "country"])

# to csv
merged_famous_places_df.to_csv("Cleaned Data/clean_famous_places")

################## european destinations ##################

euro_destination_df = pd.read_csv("Raw Data/destinations.csv")

# replace year round with all months
euro_destination_df["Best Time to Visit"] = euro_destination_df["Best Time to Visit"].replace({"Year-round" : "(Jan-Dec)", "March" : "Mar", "April" : "Apr", "June" : "Jun", "August" : "Aug", "September" : "Sep", "Sept": "Sep", "December" : "Dec"}, regex=True)

# extract month
euro_destination_df["Best_Month"] = euro_destination_df["Best Time to Visit"].str.findall(r"\((.*?)\)")
euro_destination_df["Best_Month"] = euro_destination_df["Best_Month"].apply(updated_best_time)

#extract season
euro_destination_df["Best_Season"] = euro_destination_df["Best Time to Visit"].str.findall(r"(Winter|Spring|Summer|Fall)")

#drop unwanted columns
euro_destination_df = euro_destination_df.drop(columns=["Region", "Best Time to Visit", "Currency", "Majority Religion", "Approximate Annual Tourists", "Language", "Cost of Living", "Safety"])

# to csv
euro_destination_df.to_csv("Cleaned Data/clean_euro_destinations")




