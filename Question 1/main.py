from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def sentiment_scores(sentences):
    result = {"positive": 0, "negative": 0, "neutral": 0}
    sid_obj = SentimentIntensityAnalyzer()
    for sentence in sentences:
        sentiment_dict = sid_obj.polarity_scores(sentence)

        if sentiment_dict['compound'] >= 0.05:
            result["positive"] += 1

        elif sentiment_dict['compound'] <= - 0.05:
            result["negative"] += 1

        else:
            result["neutral"] += 1
    print(result)


sentences = []
with open("input/q1/reviews.txt") as file:
    for line in file:
        sentences.append(line)

sentiment_scores(sentences)
