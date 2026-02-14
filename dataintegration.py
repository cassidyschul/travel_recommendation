import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import warnings
warnings.filterwarnings("ignore")


# import dataframes

famous_places_df = pd.read_csv("Cleaned Data/clean_famous_places")
euro_destinations_df = pd.read_csv("Cleaned Data/clean_euro_destinations")
europe_hotel_reviews_df = pd.read_csv("Cleaned Data/clean_europe_hotel_reviews")
travel_destinations_df = pd.read_csv("Cleaned Data/clean_travel_destinations")
travel_details_df = pd.read_csv("Cleaned Data/clean_travel_details")
worldwide_travel_cities_df = pd.read_csv("Cleaned Data/clean_worldwide_travel_cities")