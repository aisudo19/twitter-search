import sys
import snscrape.modules.twitter as sntwitter

SEARCH_NUM  = "100"
TIMEOUT     = 10
HEADER      = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:63.0) Gecko/20100101 Firefox/63.0'}


#グーグル検索から検索結果のリストを返す関数
def search_twitter(words, start_date, end_date, search_limit):
    if start_date == "":
        start_date = 0

    if end_date == "":
        end_date = 99999999

    if(search_limit == ""):
        search_limit = 9
    result_raw = []
    tweets_list = []
    try:
        result_raw = enumerate(sntwitter.TwitterSearchScraper(words).get_items())
    except Exception as e:
        print("ERROR_DOWNLOAD:{}".format(e))
    else:
        for i,tweet in result_raw:
            # if i>5000 or tweet.conversationId == 1547777987650674689:
            if i>int(search_limit):
                break
            
            tweetUrl = "https://twitter.com/" + tweet.user.username + "/status/" + str(tweet.id)
            date = tweet.date.strftime('%Y/%m/%d %H:%M:%S')
            tweet_date = tweet.date.strftime('%Y%m%d')
            
            start_date_ = start_date.replace('-','')
            end_date_ = end_date.replace('-','')

            # もしツイート日付が20220803　で　指定の日付が20220801までだったら、コンティニュー
            if int(tweet_date) < int(start_date_):
                continue
            # もしツイート日付が20220803　で　指定の日付が20220801までだったら、コンティニュー
            if int(tweet_date) > int(end_date_):
                continue

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

