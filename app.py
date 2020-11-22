from flask import Flask, render_template, request
from afinn import Afinn
from googletrans import Translator
from gensim.summarization import summarize
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer

app = Flask(__name__, template_folder='templates')


#


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/signup")
def sign():
    return render_template('signup.html')


#
#
@app.route("/feedback")
def feedback():
    return render_template('feedback.html')

@app.route("/summary")
def summary():
    return render_template('summary.html')


@app.route('/summary_pred', methods=['POST'])
def summary_pred():
    text = [str(x) for x in request.form.values()]
    docx = "".join(text)
    parser = PlaintextParser.from_string(docx, Tokenizer("english"))
    lex_summarizer = LexRankSummarizer()
    summary = lex_summarizer(parser.document, 3)
    summary_list = [str(sentence) for sentence in summary]
    result = "".join(summary_list)
    return render_template('summary.html', prediction_text = "{}".format(result))


@app.route('/predict', methods=['POST'])
def predict():
    af = Afinn()
    translator = Translator()
    text = [str(x) for x in request.form.values()]
    text1 = "".join(text)
    trans = translator.translate(text1)
    detect_dict = {'af': 'afrikaans', 'sq': 'albanian',
                   'am': 'amharic', 'ar': 'arabic',
                   'hy': 'armenian', 'az': 'azerbaijani',
                   'eu': 'basque', 'be': 'belarusian',
                   'bn': 'bengali', 'bs': 'bosnian',
                   'bg': 'bulgarian', 'ca': 'catalan',
                   'ceb': 'cebuano', 'ny': 'chichewa',
                   'zh-cn': 'chinese (simplified)',
                   'zh-tw': 'chinese (traditional)',
                   'co': 'corsican', 'hr': 'croatian',
                   'cs': 'czech', 'da': 'danish',
                   'nl': 'dutch', 'en': 'english',
                   'eo': 'esperanto', 'et': 'estonian',
                   'tl': 'filipino', 'fi': 'finnish',
                   'fr': 'french', 'fy': 'frisian',
                   'gl': 'galician', 'ka': 'georgian',
                   'de': 'german', 'el': 'greek',
                   'gu': 'gujarati', 'ht': 'haitian creole',
                   'ha': 'hausa', 'haw': 'hawaiian',
                   'iw': 'hebrew', 'hi': 'hindi',
                   'hmn': 'hmong', 'hu': 'hungarian',
                   'is': 'icelandic', 'ig': 'igbo',
                   'id': 'indonesian', 'ga': 'irish',
                   'it': 'italian', 'ja': 'japanese',
                   'jw': 'javanese', 'kn': 'kannada',
                   'kk': 'kazakh', 'km': 'khmer',
                   'ko': 'korean', 'ku': 'kurdish (kurmanji)',
                   'ky': 'kyrgyz', 'lo': 'lao',
                   'la': 'latin', 'lv': 'latvian',
                   'lt': 'lithuanian', 'lb': 'luxembourgish',
                   'mk': 'macedonian', 'mg': 'malagasy',
                   'ms': 'malay', 'ml': 'malayalam',
                   'mt': 'maltese', 'mi': 'maori',
                   'mr': 'marathi', 'mn': 'mongolian',
                   'my': 'myanmar (burmese)', 'ne': 'nepali',
                   'no': 'norwegian', 'ps': 'pashto',
                   'fa': 'persian', 'pl': 'polish',
                   'pt': 'portuguese', 'pa': 'punjabi',
                   'ro': 'romanian', 'ru': 'russian',
                   'sm': 'samoan', 'gd': 'scots gaelic',
                   'sr': 'serbian', 'st': 'sesotho',
                   'sn': 'shona', 'sd': 'sindhi',
                   'si': 'sinhala', 'sk': 'slovak',
                   'sl': 'slovenian', 'so': 'somali',
                   'es': 'spanish', 'su': 'sundanese',
                   'sw': 'swahili', 'sv': 'swedish',
                   'tg': 'tajik', 'ta': 'tamil',
                   'te': 'telugu', 'th': 'thai',
                   'tr': 'turkish', 'uk': 'ukrainian',
                   'ur': 'urdu', 'uz': 'uzbek',
                   'vi': 'vietnamese', 'cy': 'welsh',
                   'xh': 'xhosa', 'yi': 'yiddish',
                   'yo': 'yoruba', 'zu': 'zulu',
                   'fil': 'Filipino', 'he': 'Hebrew'}

    # for key, value in detect_dict.items():
    #     if key == trans.src:
    #         lang = value
    prediction = af.score(trans.text)

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


app.run(debug=True)
