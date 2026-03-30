#### stage 1 recommender ####
# Uses keyword matching to parse the user's input and convert into a preference vector to compare against all destinations using cosine similiarity

import numpy as np
import pandas as pd
#from sklearn.metrics.pairwise import cosine_similarity


# load data and convert values to 32-bit float 
X = np.load('../X_features.npy', allow_pickle=True).astype(np.float32)


# load destinations
destinations = pd.read_csv('../destinations.csv')

# load feature columns
feature_columns = np.load('../feature_columns.npy', allow_pickle=True).tolist()


# define features - only using style columns to match against user input in stage 1
style_features = ['culture', 'adventure', 'nature', 'beaches', 'nightlife', 'cuisine', 'wellness', 'urban', 'seclusion']
print(style_features)

# determine index position of style features
#style_indices = [feature_columns.index(col) for col in style_features]
#print(style_indices)