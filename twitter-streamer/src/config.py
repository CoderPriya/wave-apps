class Configuration:
    """
    Configuration file for Twitter Sentiment
    """

    def __init__(self):
        self.color = "#00A8E0"
        self.total_gauge_color = "#FF0102"
        self.image_path = "static/icon.jpeg"

        self.default_model = "twitter_sentiment_model"

        self.title = "Twitter Streamer"
        self.subtitle = "Streams twitter hashtags and provide insights"
        self.icon = "UpgradeAnalysis"

        self.boxes = {
            "banner": "1 1 -1 1",
            "logo": "11 1 -1 1",
            "navbar": "4 1 -1 1",
            "search_click": "11 2 2 1",
            "search_tab": "1 2 10 1",
            "credentials": "-1 -1 -1 -1"
        }

        self.tweet_row_indexes = ['3', '9', '15', '21', '27']
        self.tweet_column_indexes = ['1', '4', '7', '10']
        self.max_tweet_count = 12
        self.default_search_text = 'AI'
        self.ask_for_access_text = "Apply for access : <a href=\"https://developer.twitter.com/en/apply-for-access\" " \
                                   "target='_blank'\">Visit developer.twitter.com!</a>"
        self.popularity_terms = {'neg': 'Negative', 'neu': 'Neutral', 'pos': 'Positive', 'compound': 'Compound'}
