from ImmovableVault import db, UserMixin


class UserProfile(UserMixin, db.Model):
    __tablename__ = "UserProfile"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    user_name = db.Column(db.Text, unique=True, nullable=False)
    user_unique_id = db.Column(db.Text, unique=True)
    user_email = db.Column(db.Text, nullable=False, server_default="")
    user_password = db.Column(db.Text, nullable=False, server_default="")
    documents = db.relationship(
        "Document",
        backref="UserProfile",
        primaryjoin="Document.user_id==UserProfile.user_unique_id",
    )

    def __init__(
        self,
        user_name,
        user_unique_id,
        user_email,
        user_password,
    ):
        self.user_name = user_name
        self.user_unique_id = user_unique_id
        self.user_email = user_email
        self.user_password = user_password


class Document(UserMixin, db.Model):
    __tablename__ = "Document"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    document_name = db.Column(db.Text, nullable=False)
    documet_unique_id = db.Column(db.Text, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey("UserProfile.user_unique_id"))
    document_type = db.Column(db.Text)
    document_path = db.Column(db.Text, nullable=False)
    Accesses = db.relationship(
        "DocumentAccess",
        backref="Document",
        primaryjoin="Document.id==DocumentAccess.document_id",
    )

    def __init__(
        self,
        document_name,
        documet_unique_id,
        document_type,
        document_path,
    ):
        self.document_name = document_name
        self.documet_unique_id = documet_unique_id
        self.document_type = document_type
        self.document_path = document_path


class DocumentAccess(UserMixin, db.Model):
    __tablename__ = "DocumentAccess"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    document_name = db.Column(db.Text)
    document_id = db.Column(db.Integer, db.ForeignKey("Document.id"))
    access_created = db.Column(db.Text)
    access_deadline = db.Column(db.Text)
    access_type = db.Column(db.Text)
    access_to_id = db.Column(db.Text)

    def __init__(
        self,
        document_name,
        access_created,
        access_deadline,
        access_type,
        access_to_id,
    ):
        self.document_name = document_name
        self.access_created = access_created
        self.access_deadline = access_deadline
        self.access_type = access_type
        self.access_to_id = access_to_id
