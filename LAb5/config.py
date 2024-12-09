class Config:
    def __init__(self):
        self.DEBUG = True
        self.SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Ramy2404@localhost:3306/ap'
        self.SQLALCHEMY_TRACK_MODIFICATIONS = False