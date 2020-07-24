import tweepy
import csv
import re
import os

CONSUMER_KEY = os.environ.get('TWITTER_CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('TWITTER_CONSUMER_SECRET')
OAUTH_TOKEN = os.environ.get('TWITTER_OAUTH_TOKEN')
OAUTH_TOKEN_SECRET = os.environ.get('TWTTIER_OAUTH_TOKEN_SECRET')

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
api = tweepy.API(auth)

def get_tweet_text_from_id(id):
    tweet = api.get_status(id)
    return tweet.text

if __name__ == "__main__":
    with open('tweet-ids.csv') as csv_file:
        with open('output.csv', mode='w', newline='', encoding='utf-8') as output_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            output_writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    output_writer.writerow(['tweet id', 'tweet text'])
                    pass
                else:
                    try:
                        # parse tweet id from the url
                        tweet_id = re.search(r'http://twitter.com/1/statuses/([0-9]+)', row[0]).group(1)

                        # grab tweet text from tweet id
                        tweet_text = ' '.join(get_tweet_text_from_id(tweet_id).splitlines())

                        # save the result to the output file
                        output_writer.writerow([row[0], tweet_text])
                    except:
                        pass
                line_count += 1
            
            output_file.close()
        csv_file.close()
