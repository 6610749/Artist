
from datetime import date
from app import db 



class Omgevinf(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    name = db.Column(db.String(140))

    def __repr__ (self):
        return '{}'.format(self.name)


class Artist(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    name = db.Column(db.String(140))
    image = db.Column(db.String(16000))

    performances = db.relationship("Performance", secondary="association"
                                    ,lazy='dynamic')

    def __repr__ (self):
        return '{}'.format(self.name)

class Performance(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    title = db.Column(db.String(140))

    artists = db.relationship("Artist", secondary="association"   )

    description = db.Column(db.String(16000))
    price = db.Column(db.Integer) 
    link = db.Column(db.String(180)) 

    omgevinfId = db.Column(db.Integer, db.ForeignKey(Omgevinf.id))
    omgevinf = db.relationship(Omgevinf, uselist=False)

    
    date = db.Column(db.Date ,default=date.today)
    def __repr__ (self):
        return '<Performance> {}'.format(self.title)


'''
class Association(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id' ) )
    performance_id = db.Column(db.Integer, db.ForeignKey('performance.id'  ) ) 

    artist = db.relationship(Artist, backref=db.backref("association")  ) 
    performance = db.relationship(Performance, backref=db.backref("association") )
'''

Association = db.Table(
    'association' , 
    db.Column('artists_id' , db.Integer , db.ForeignKey('artist.id') ) , 
    db.Column('performance_id' , db.Integer , db.ForeignKey('performance.id') )
    
)  