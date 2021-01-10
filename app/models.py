from . import db


class SportItem(db.Model):
    __tablename__ = 'DD_PE_item_test'
    __table_args__ = {'mysql_engine': 'InnoDB'}
    id = db.Column(db.Integer, doc="商品ID", primary_key=True)
    Name = db.Column(db.String, doc="商品名", primary_key=False)
    image_url = db.Column(db.String, doc="商品图片链接", nullable=False)
    url = db.Column(db.String, doc='商品链接', nullable=False)
    category = db.Column(db.String, doc='商品类别', nullable=False)
    brand = db.Column(db.String, doc='商品品牌名字', nullable=False)
    brand_id = db.Column(db.Integer, doc='商品品牌id', nullable=False)
    score = db.Column(db.Float, doc='商品评分', nullable=False)
    price = db.Column(db.Float, doc='商品价格', nullable=False)
    comment = db.Column(db.String, doc='商品评论', nullable=False)
    comment_tag = db.Column(db.String, doc='商品评论标签', nullable=False)
    hotword = db.Column(db.String, doc='商品热词', nullable=False)
