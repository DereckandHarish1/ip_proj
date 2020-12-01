# import the module
import tweepy

# assign the values accordingly
def tweetss(wo):
    consumer_key = "Yt141NXbf9rYI9LaeswlCJQRt"#api key
    consumer_secret = "dhOYfIrepbtfLDMmsK7kZXhzPxoMuyXQGVJV2BqxuqQJapwj2q"#api
    access_token = "1258795430751715329-jSAFU04dev3MknVWpa1ZgxYdSkcsmI"
    access_token_secret = "ltyfTJTFWDv7ZeNronVLHpbcvQEx2yHOWTaKHcXsodAaM"

    # calling API
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    li = []

    # # authorization of consumer key and consumer secret
    # auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    #
    # # set access to user's access key and access secret
    # auth.set_access_token(access_token, access_token_secret)
    #
    # # calling the api
    # api = tweepy.API(auth)

    # WOEID of London
    # woeid = 44418
    woeid = wo

    # fetching the trends
    trends = api.trends_place(id = woeid)

    # printing the information
    #print("The top trends for the location are :")

    for value in trends:
        for trend in value['trends']:
                 li.append(trend['name'])

    return li[:10]

