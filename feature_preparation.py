import pandas as pd
import numpy as np


print("Starting feature preparation...")

# load cleaned merged data
print("Loading merged_data.csv...")
merged_df = pd.read_csv("Cleaned Data/merged_data.csv")
print(f"Shape: {merged_df.shape}")

# select numerical features 
numerical_features = ['culture', 'adventure', 'nature', 'beaches', 'nightlife', 'cuisine', 'wellness', 'urban', 'seclusion', 'lat', 'lng', 'avg_trip_duration', 'avg_accommodation_cost', 'avg_transport_cost', 'avg_attraction_fee', 'num_attractions']

X = merged_df[numerical_features].copy()
print(f"Selected {len(numerical_features)} features")

# convert budget level to numeric
budget_mapping = {'Budget' : 1, 'Mid-range': 2, 'Luxury': 3}
X['budget_numeric'] = merged_df['budget_level'].map(budget_mapping)

# fill in missing feature values
for col in X.columns:
    if X[col].isnull().sum()>0:
        X[col] = X[col].fillna(X[col].median())

# normalize features 
for col in X.columns:
    min_val = X[col].min()
    max_val = X[col].max()
    if max_val != min_val:
        X[col] = (X[col] - min_val) / (max_val - min_val)

# one-hot encode region features
region_dummies = pd.get_dummies(merged_df['region'], prefix = 'region', dtype=np.float32)
X = pd.concat([X, region_dummies], axis=1)
print(f" Add {len(region_dummies.columns)} region features")

print(X.head())

# save features, feature names, and destinations
np.save('X_features.npy', X.values)
np.save('feature_columns.npy', X.columns.to_list)
destinations = merged_df[['City', 'Country', 'lat', 'lng']]
destinations.to_csv('destinations.csv', index = False)
