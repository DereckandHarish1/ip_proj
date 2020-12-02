from flask import Flask, render_template, request
# from afinn import Afinn
from gensim.summarization import summarize
# from sumy.parsers.plaintext import PlaintextParser
# from sumy.nlp.tokenizers import Tokenizer
# from sumy.summarizers.lex_rank import LexRankSummarizer
from textblob import TextBlob
from admin.admin import *
from visual.tweets import tweetss
from viz import *
from lang_detect import *
from flask_bcrypt import Bcrypt
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__, template_folder='templates')
# bcrypt = Bcrypt(app)


# from flask_ngrok import run_with_ngrok
# run_with_ngrok(app)


@app.route("/")
def home():
    return render_template('login.html')


@app.route("/index")
def index():
    return render_template('index.html')


@app.route("/signup")
def signup():
    return render_template('signup.html')


#
#
@app.route("/feedback")
def feedback():
    return render_template('feedback.html')


@app.route("/summary")
def summary():
    return render_template('summary.html')


@app.route("/trending")
def trending():
    return render_template('trending.html')


@app.route("/login_up", methods=['POST'])
def login_up():
    email = request.form["email"]
    password = request.form["pw"]
    a = ret()
    ch = check2(email, password, a)
    if ch:
        return render_template("index.html")
    else:
        return render_template("login.html", prediction_text="Invalid Username or Password")


@app.route('/summary_pred', methods=['POST'])
def summary_pred():
    text = [str(x) for x in request.form.values()]
    docx = "".join(text)
    # parser = PlaintextParser.from_string(docx, Tokenizer("english"))
    # lex_summarizer = LexRankSummarizer()
    # summary = lex_summarizer(parser.document, 3)
    # summary_list = [str(sentence) for sentence in summary]
    # result = "".join(summary_list)
    result = summarize(docx, word_count=100)
    return render_template('summary.html', prediction_text="{}".format(result))


@app.route('/sign_up', methods=['POST'])
def sign_up():
    r = ret()
    email = request.form["email"]
    password = request.form["psw"]
    pass2 = request.form["psw-repeat"]
    if email_valid(email):
        if pass_check(password, pass2):
            # hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            hp = generate_password_hash(password)
            if email_check(email, r):
                dicts = {"email": email, "password": hp}
                store(dicts)
                print("yes")
                return render_template('login.html')
            else:
                return render_template("signup.html", predicted="Username already taken")

        else:
            return render_template("signup.html", pass_re="Password is not matching")

    else:
        return render_template("signup.html", email="Invalid Email")


@app.route('/predict', methods=['POST'])
def predict():
    try:
        text = [str(x) for x in request.form.values()]
        text1 = "".join(text)
        text = lan_det(text1)
        texts = TextBlob(text)

        prediction = texts.sentiment.polarity

        if prediction > 0:
            return render_template('index.html', prediction_text1='The Given Sentiment Is Positive',
                                   prediction_text="The Polarity Score For Given Sentiment Is {}".format(prediction))
        elif prediction < 0:
            return render_template('index.html', prediction_text1='The Given Sentiment Is Negative',
                                   prediction_text="The Polarity Score For Given Sentiment Is {}".format(prediction))

        else:
            return render_template('index.html',
                                   prediction_text='The Given Sentiment Is Neutral With Polarity Score {}'.format(
                                       prediction))
    except:
        return render_template("index.html", prediction_text="Language Not Supported")


@app.route('/tweet_pred', methods=['POST'])
def tweet_pred():
    text = [int(x) for x in request.form.values()]
    tw = tweetss(text[0])
    return render_template("trending.html", prediction_text=tw)


@app.route('/visualizer/')
def visualizer():
    return render_template('visualizer.html')


@app.route('/visual_predict', methods=['POST'])
def visual_predict():
    app_name = "".join([str(x) for x in request.form.values()])
    rev, app_id = get_review(app_name)
    senti_dict, pie = create_db(rev, app_id)
    bar, pie = bar_pie(senti_dict, pie)

    return render_template('charts.html', bar=bar, pie=pie)


@app.route('/feed_back', methods=['POST'])
def feed_back():
    email = request.form["email"]
    message = request.form["message"]

    dicts = {"email": email, "message": message}
    store_feedback(dicts)
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
