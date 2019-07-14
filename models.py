import datetime

from flask_bcrypt import generate_password_hash
from flask_login import UserMixin

from peewee import *


db = SqliteDatabase('learning.db')


class User(UserMixin, Model):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField(max_length=100)
    is_admin = BooleanField(default=False)

    class Meta:
        database = db

    @classmethod
    def create_user(cls, username, email, password, is_admin=False):
        try:
            with db.transaction():
                user = cls.create(
                    username=username,
                    email=email,
                    password=generate_password_hash(password),
                    is_admin=is_admin
                )
        except IntegrityError:
            raise ValueError("User already exists.")
        else:
            return user


class Entry(Model):
    title = CharField(unique=True)
    date = DateField(default=datetime.date.today)
    time = IntegerField()
    learned = TextField()
    resources = TextField()
    slug = CharField(unique=True)
    user = ForeignKeyField(User)

    class Meta:
        database = db

    def get_tags(self):
        tags = (Tag
                .select()
                .join(EntryTags)
                .join(Entry)
                .where(Entry.id == self.id))
        return sorted([tag.tag_name for tag in tags])

    def get_tags_string(self):
        tags = self.get_tags()
        return ' '.join(tags)

    def get_tag_link(self, tag):
        tag_id = Tag.get(Tag.tag_name == tag).id
        return "/{}".format(tag_id)


class Tag(Model):
    tag_name = CharField(unique=True)

    class Meta:
        database = db

    def get_entries(self):
        return (Entry
                .select()
                .join(EntryTags)
                .join(Tag)
                .where(Tag.id == self.id)
                .order_by(Entry.date.desc()))


class EntryTags(Model):
    entry = ForeignKeyField(Entry)
    tag = ForeignKeyField(Tag)

    class Meta:
        database = db
        indexes = (
            (('entry', 'tag'), True),
        )


def initialize():
    db.connect()
    db.create_tables([User, Entry, Tag, EntryTags], safe=True)
    db.close()
