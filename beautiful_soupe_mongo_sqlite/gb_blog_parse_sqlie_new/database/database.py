from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from . import models


class Database:

    def __init__(self, db_url):
        engine = create_engine(db_url)
        models.Base.metadata.create_all(bind=engine)
        self.maker = sessionmaker(bind=engine)

    def get_or_create(self, session, model, filter_field, data):
        instance = session.query(model).filter(
            getattr(model, filter_field) == data[filter_field]).first()
        if not instance:
            instance = model(**data)
        return instance

    def create_comments(self, post_id, data):
        session = self.maker()
        while True:
            try:
                comment = data.pop(0)
            except IndexError:
                break
            author = self.get_or_create(
                session,
                models.Author,
                "url",
                dict(
                    name=comment["comment"]["user"]["full_name"],
                    url=comment["comment"]["user"]["url"],
                    gb_id=comment["comment"]["user"]["id"]),
            )
            if not author.gb_id:
                author.gb_id = comment["comment"]["user"]["id"]
            comment_db = self.get_or_create(
                session, models.Comment, "id", comment["comment"],
            )
            comment_db.author = author
            comment_db.post_id = post_id
            session.add(comment_db)
            try:
                session.commit()
            except Exception:
                session.rollback()
            if comment["comment"]["children"]:
                data.extend(comment["comment"]["children"])
        session.close()

    def add_post(self, data):
        session = self.maker()
        post = self.get_or_create(session, models.Post, "id", data["post_data"])
        post.author = self.get_or_create(session, models.Author, "url", data['author_data'])
        post.tags.extend(map(
            lambda tag_data: self.get_or_create(session, models.Tag, "url", tag_data),
            data["tags_data"],
        ))
        session.add(post)
        try:
            session.commit()
        except Exception:
            session.rollback()
        finally:
            session.close()
        self.create_comments(data["post_data"]["id"], data['comments_data'])
