import sys
import snscrape.modules.twitter as sntwitter

SEARCH_NUM  = "100"
TIMEOUT     = 10
HEADER      = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:63.0) Gecko/20100101 Firefox/63.0'}

#グーグル検索から検索結果のリストを返す関数
def search_twitter(words, since_date, until_date, search_limit):
    print("since: " + since_date + " until: " + until_date)
    if(search_limit == ""):
        search_limit = 10
    result_raw = []
    tweets_list = []
    query = " since:" + since_date + " until:" + until_date + " lang:ja -filter:links -filter:replies"
    print(query)
    try:
        result_raw = enumerate(sntwitter.TwitterSearchScraper(words + query).get_items())
    except Exception as e:
        print("ERROR_DOWNLOAD:{}".format(e))
    else:
        for i, tweet in result_raw:
            if len(tweets_list)>int(search_limit)-1:
                break
            if len(tweets_list)>5000:
                break
            
            tweetUrl = "https://twitter.com/" + tweet.user.username + "/status/" + str(tweet.id)
            date = tweet.date.strftime('%Y/%m/%d %H:%M:%S')
            tweet_date = tweet.date.strftime('%Y%m%d')
            
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

