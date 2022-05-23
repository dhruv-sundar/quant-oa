# Quant OA: Twitter Scraper - Dhruv Sundararaman

## Objectives
Scrapes the following information from Twitter using `tweepy` into `output.json`
  - PII: username, account age, follower count
  - top 5 most-retweeted posts 
  - top 5 most-retweeted posts *that the user retweets* 
  - 50 of User's followers, and 10 new followers (derivative)
  - 5 hashtags the user is most likely to use

> 50 followers subject to change, simply for testing purposes to avoid API rate limiting

## Instructions
Install `tweepy` library

Create a `.env` file inside `twitter-user-scraper/` with the following format:
```
api-token = "#########"
key = "#########"
secret-key = "#########"
access-token = "#########"
access-token-secret = "#########"
```

Run the following command to output Twitter data into `output.json`
```
python main.py <screen_name>
```

Run the following command to parse output.json into `User` object
```
python load.py
```

## Future Improvements
- Optimize algorithm to determine most likely hashtags
- Add more specific error messages
- Expand for more derivative information from Twitter API