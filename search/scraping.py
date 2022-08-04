import sys
import snscrape.modules.twitter as sntwitter

SEARCH_NUM  = "100"
TIMEOUT     = 10
HEADER      = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:63.0) Gecko/20100101 Firefox/63.0'}


#グーグル検索から検索結果のリストを返す関数
# def search_google(words, start_date, end_date, search_limit):
def search_google(words, start_date, end_date):
    print(start_date)
    result_raw = []
    tweets_list = []
    try:
        result_raw = enumerate(sntwitter.TwitterSearchScraper(words).get_items())
    except Exception as e:
        print("ERROR_DOWNLOAD:{}".format(e))
    else:
        for i,tweet in result_raw:
            # if i>5000 or tweet.conversationId == 1547777987650674689:
            if i>100:
                break
            
            tweetUrl = "https://twitter.com/" + tweet.user.username + "/status/" + str(tweet.id)
            date = tweet.date.strftime('%Y/%m/%d %H:%M:%S')
            
            deleteEolContent = tweet.content.replace("\r\n", "")
            deleteEolContent = tweet.content.replace("\r", "")
            deleteEolContent = tweet.content.replace("\n", "")
            deleteEolContent = deleteEolContent
            tweets_list.append([date, '@' + tweet.user.username,tweet.user.displayname, deleteEolContent,tweetUrl])

    return tweets_list

def main():

    words   = input("検索ワードを入力してください")
    print(search_google(words))


if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        print("\nprogram was ended.\n")
        sys.exit()

