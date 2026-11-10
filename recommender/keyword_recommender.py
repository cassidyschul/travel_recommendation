#### stage 1 recommender ####
# Uses keyword matching to parse the user's input and convert into a preference vector to compare against all destinations using cosine similiarity

import os
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# get file path for travel_recommendation repo
base_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# load feature columns
feature_columns = np.load(os.path.join(base_directory, 'feature_columns.npy')).tolist()

# load data and convert values to 32-bit float 
X = pd.DataFrame(np.load(os.path.join(base_directory, 'X_features.npy')).astype(np.float32), columns = feature_columns)


# load destinations
destinations = pd.read_csv(os.path.join(base_directory, 'destinations.csv'))


# define category features 
category_features = ['culture', 'adventure', 'nature', 'beaches', 'nightlife', 'cuisine', 'wellness', 'urban', 'seclusion']
X_features = X[category_features].values

# single words that signal each category
keywords = {
    'culture':   ['culture', 'history', 'historic', 'museum', 'museums', 'art', 'architecture'],
    'adventure': ['adventure', 'hiking', 'hike', 'diving', 'climbing', 'outdoor', 'outdoors'],
    'nature':    ['nature', 'mountain', 'mountains', 'forest', 'wildlife', 'scenic'],
    'beaches':   ['beach', 'beaches', 'surf', 'island', 'islands', 'swim', 'coast'],
    'nightlife': ['nightlife', 'party', 'bar', 'bars', 'club', 'clubs'],
    'cuisine':   ['food', 'cuisine', 'restaurant', 'restaurants', 'eat', 'foodie', 'wine'],
    'wellness':  ['wellness', 'spa', 'relax', 'relaxing', 'yoga', 'retreat'],
    'urban':     ['city', 'urban', 'shopping'],
    'seclusion': ['quiet', 'secluded', 'remote', 'peaceful'],
}


# count keywords in user input (9 numbers) 
def parse_inputs(text):
    text = text.lower()
    for ch in ',.!?;:':
        text = text.replace(ch, ' ')
    words = text.split()

    preferences = []
    for category in category_features:
        count = 0
        for word in words:
            if word in keywords[category]:
                count += 1
        preferences.append(count)
    return np.array(preferences, dtype=np.float32)

def recommend(user_input, top_n=5):
    preferences = parse_inputs(user_input)

    # no keywords found, return empty table
    if preferences.sum() == 0:
        print("No travel preferences found.")
        empty = destinations.head(0).copy()
        empty['match_score'] = []
        return empty

    # compare the query (1 x 9)
    scores = cosine_similarity(preferences.reshape(1,-1), X_features)[0]

    results = destinations.copy()
    results['match_score'] = scores
    return results.sort_values('match_score', ascending=False).head(top_n)
