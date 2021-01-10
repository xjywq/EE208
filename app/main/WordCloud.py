from collections import Counter

import jieba
import jieba.analyse
from pyecharts import options as opts
from pyecharts.charts import WordCloud
from pyecharts.globals import SymbolType
from .EE208_ES_FP_class import cut_comment_seg
from ..models import SportItem

def wordcloud_base(id) -> WordCloud:
    item = SportItem.query.filter_by(id=int(id)).first()
    words = eval(cut_comment_seg(item.comment))
    c = (
        WordCloud()
        .add("", words, word_size_range=[20, 100], shape=SymbolType.DIAMOND)
    )
    return c