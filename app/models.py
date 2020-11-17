from . import db


class SportItem(db.Model):
    __tablename__ = 'dangdang_sport_item'
    __table_args__ = {'mysql_engine': 'InnoDB'}
    title = db.Column(db.String(100), doc="商品标题", primary_key=True)
    id = db.Column(db.Integer, doc='商品品牌id', primary_key=False)
    url = db.Column(db.String(50), doc='商品链接', nullable=False)
    price = db.Column(db.String(10), doc='商品价格', nullable=False)
    hot_word = db.Column(db.String(50), doc='商品热词', nullable=False)
