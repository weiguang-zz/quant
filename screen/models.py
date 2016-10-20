#各个model类

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username

class Price(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    open_price = db.Column(db.Float)
    high_price = db.Column(db.Float)
    low_price = db.Column(db.Float)
    close_price = db.Column(db.Float)
    volumn = db.Column(db.Float)

    def __init__(self,o,h,l,c,v):
        self.open_price = o
        self.close_price = c
        self.low_price = l
        self.high_price = h
        self.volumn = v
