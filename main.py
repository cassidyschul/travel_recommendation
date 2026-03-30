#### entry point for the travel recommender app


# import recommend function
from recommender.stage1_recommender import recommend

# get user input
user_input = input("Where would you like to go and what do you want to do?")

# provide recommendations
recs = recommend(user_input)

# display recommendations to user, displaying city, country and match score
print("Top Recommendations:")
print(recs[['City', 'Country', 'match_score']].to_string(index=False))

