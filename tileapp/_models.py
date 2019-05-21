from tileapp import db


class Pattern(db.Model):
    pat_id = db.Column(db.Integer, primary_key=True)
    pat = db.Column(db.Text(), nullable=False, unique=True)
    imgs = db.relationship('Image', backref='pat', lazy=True)

    def __repr__(self):
        return f'Pattern(pat_id={self.pat_id}, pat={self.pat})'


class Image(db.Model):
    img_id = db.Column(db.Integer, primary_key=True)
    pat_id = db.Column(db.Integer, db.ForeignKey('pattern.pat_id'), nullable=False)
    fignum = db.Column(db.Integer, nullable=False)
    colormap = db.Column(db.Text, nullable=False)
    alpha = db.Column(db.Float(), default=1.0, nullable=False)
    bytes = db.Column(db.LargeBinary(), nullable=False)

    def __repr__(self):
        return f'Image(img_id={self.img_id}, pat_id={self.pat_id}, fignum={self.fignum}, bytes={self.bytes})'
