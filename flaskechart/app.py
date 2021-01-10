from random import randrange

from flask import Flask, render_template

from pyecharts import options as opts
from pyecharts.charts import WordCloud
from pyecharts.globals import SymbolType


app = Flask(__name__, static_folder="templates")



def wordcloud_base() -> WordCloud:
    ## words database?
    words = [
    ("Sam S Club", 10000),
    ("Macys", 6181),
    ("Amy Schumer", 4386),
    ("Jurassic World", 4055),
    ("Charter Communications", 2467),
    ("Chick Fil A", 2244),
    ("Planet Fitness", 1868),
    ("Pitch Perfect", 1484),
    ("Express", 1112),
    ("Home", 865),
    ("Johnny Depp", 847),
    ("Lena Dunham", 582),
    ("Lewis Hamilton", 555),
    ("KXAN", 550),
    ("Mary Ellen Mark", 462),
    ("Farrah Abraham", 366),
    ("Rita Ora", 360),
    ("Serena Williams", 282),
    ("NCAA baseball tournament", 273),
    ("中文", 265),
    ]
    c = (
        WordCloud()
        .add("", words, word_size_range=[20, 100], shape=SymbolType.DIAMOND)
    )
    return c


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/wordcloudChart")
def get_wordcloud_chart():
    c = wordcloud_base()
    return c.dump_options_with_quotes()


if __name__ == "__main__":
    app.run(debug=True, port=8080)