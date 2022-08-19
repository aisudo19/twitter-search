from cmath import sin
import datetime
import sys
import snscrape.modules.twitter as sntwitter
import mimetypes
mimetypes.add_type("text/css", ".css", True)

SEARCH_NUM  = "100"
TIMEOUT     = 10
HEADER      = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:63.0) Gecko/20100101 Firefox/63.0'}

#グーグル検索から検索結果のリストを返す関数
def search_twitter(words, since_date, until_date, search_limit):
    if(search_limit == ""):
        search_limit = 10
    if(since_date == ""):
        since_date = datetime.date.today() - datetime.timedelta(days=31)
        # print("since_date:" + str(since_date))
    if(until_date == ""):
        until_date = datetime.date.today()
    # print("since:" + str(since_date) + "_00:00:00_JST until:" + str(until_date) + "_23:59:59_JST lang:ja -filter:links -filter:replies")
    result_raw = []
    tweets_list = []
    # query = " since:" + str(since_date) + "_00:00:00_JST until:" + str(until_date) + "_23:59:59_JST lang:ja -filter:links -filter:replies"
    query = " since:" + str(since_date) + "_00:00:00_JST until:" + str(until_date) + "_23:59:59_JST"
    # print("query: " + words + query)
    try:
        result_raw = enumerate(sntwitter.TwitterSearchScraper(words + query).get_items())
        # print(result_raw)
    except Exception as e:
        print("ERROR_DOWNLOAD:{}".format(e))
    else:
        for i, tweet in result_raw:            
            tweetUrl = "https://twitter.com/" + tweet.user.username + "/status/" + str(tweet.id)
            date = tweet.date.strftime('%Y/%m/%d %H:%M:%S')
            tweet_date = tweet.date.strftime('%Y%m%d')
            if len(tweets_list)>int(search_limit)-1:
                # print("tweets_list" + len(tweets_list) + "件. tweet_date: " + str(tweet_date) + " since_date: " + str(since_date))
                break
            since_date = str(since_date).replace("-", "")
            # print(type(since_date))
            if int(tweet_date) < int(since_date):
                # print("tweets_list" + len(tweets_list) + "件. tweet_date: " + str(tweet_date) + " since_date: " + str(since_date))
                break
            # print("tweet_date: " + tweet_date + " since_date:" + since_date.replace("-", ""))
            deleteEolContent = tweet.content.replace("\r\n", "")
            deleteEolContent = tweet.content.replace("\r", "")
            deleteEolContent = tweet.content.replace("\n", "")
            deleteEolContent = deleteEolContent
            tweets_list.append([date, '@' + tweet.user.username,tweet.user.displayname, deleteEolContent,tweetUrl])

    return tweets_list

def main():

    words   = input("検索ワードを入力してください")
    print(search_twitter(words))


if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        print("\nprogram was ended.\n")
        sys.exit()

