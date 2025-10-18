import tweepy
import pandas as pd


BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAHh74wEAAAAAFM5yx1HJ%2Fa%2F%2Bdt%2BDJjs5onVpNR4%3DylNhaU8KXuUdpCiZA8ksciqxaRWVI82l6e89VaEx3FdSTrjTay"

client = tweepy.Client(bearer_token=BEARER_TOKEN)

username = "GAUTTER_"  
user = client.get_user(username=username)
user_id = user.data.id

tweets = client.get_users_tweets(
    id=user_id,
    max_results=50,  
    tweet_fields=["created_at", "public_metrics", "text"]
)

data = []
for t in tweets.data:
    metrics = t.data["public_metrics"]
    data.append({
        "date": t.data["created_at"],
        "text": t.data["text"],
        "likes": metrics["like_count"],
        "retweets": metrics["retweet_count"]
    })

df = pd.DataFrame(data)
df.to_csv("D:/Project/Python/streamlit/data_tweet/data.csv", index=False)
print("✅ Збережено у data.csv")
