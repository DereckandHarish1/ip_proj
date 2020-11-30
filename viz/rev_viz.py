import json
import numpy as np
import plotly
import plotly.graph_objects as go
from google_play_scraper import reviews, Sort
from pymongo import MongoClient
from pymongo.errors import CollectionInvalid
from textblob import TextBlob


def get_review(app_name):
    app_id = app_name.split("/")[-1].split("=")[1]

    result = reviews(
        app_id,
        sort=Sort.MOST_RELEVANT,  # defaults to Sort.MOST_RELEVANT
        count=75
    )

    di = result
    li = []
    for i in di[0]:
        li.append(i['content'])
    lis = []

    for i in li:
        lis.append(TextBlob(i).sentiment.polarity)

    lis = ["Positive" if i > 0 else "Neutral" if i == 0 else "Negative" for i in lis]

    data = list(zip(li, lis))

    return data, app_id


# save data to mongodb
def create_db(data, app_id):
    data_list = []

    for i in data:
        data_list.append(
            {
                "text": i[0],
                "sentiment": i[1]
            }
        )
    key = app_id.split('.')

    app_key = ' '.join(key[1:])

    client = MongoClient(
        "mongodb+srv://Harish:harishdereck@cluster0.5mz9d.mongodb.net/<dbname>?retryWrites=true&w=majority")

    db = client.get_database('PlayStoreReview')

    try:
        ref = db.create_collection(app_key)

    except (Exception, CollectionInvalid):
        ref = db.get_collection(app_key)
        ref.delete_many({})
    # Using seperate cluster

    ref.insert_many(data_list)

    tot = ref.count_documents({})
    count_sentiment_dict = {
        'positive': ref.count_documents({'sentiment': 'Positive'}),
        'negative': ref.count_documents({'sentiment': 'Negative'}),
        'neutral': ref.count_documents({'sentiment': 'Neutral'})
    }

    pie_percent = {
        'percentage_positive': np.round(float(ref.count_documents({'sentiment': 'Positive'}) / tot) * 100, decimals=2),
        'percentage_negative': np.round(float(ref.count_documents({'sentiment': 'Negative'}) / tot) * 100, decimals=2),
        'percentage_neutral': np.round(float(ref.count_documents({'sentiment': 'Neutral'}) / tot) * 100, decimals=2)
    }

    return count_sentiment_dict, pie_percent


def bar_pie(count_sentiment_dict, pie_percent):
    # data1 = [
    #     go.Bar(x=list(count_sentiment_dict.keys()), y=list(count_sentiment_dict.values()))
    # ]

    fig = go.Figure([go.Bar(x=list(count_sentiment_dict.keys()), y=list(count_sentiment_dict.values()))])
    fig.update_traces(marker_color='#C8A2C8', marker_line_color='rgb(8,48,107)', marker_line_width=2.5, opacity=0.6)
    # fig.show()

    # data2 = [
    #     go.Pie(labels=list(pie_percent.keys()), values=list(pie_percent.values()))
    # ]
    colors = ['gold', 'mediumturquoise', 'lightgreen']

    fig1 = go.Figure(data=[go.Pie(labels=list(pie_percent.keys()), values=list(pie_percent.values()))])
    fig1.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20,
                       marker=dict(colors=colors, line=dict(color='#000000', width=2)))
    # fig1.show()
    # print(fig.to_dict())
    graphBar = json.dumps(fig.to_dict(), cls=plotly.utils.PlotlyJSONEncoder)
    graphPie = json.dumps(fig1.to_dict(), cls=plotly.utils.PlotlyJSONEncoder)
    return graphBar, graphPie
