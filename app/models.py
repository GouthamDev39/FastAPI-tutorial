from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.expression import null, text
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key = True, nullable = False)
    title = Column(String, nullable = False)
    content = Column(String, nullable = False)
    published = Column(Boolean, server_default= "true", nullable= False)
    created_at = Column(TIMESTAMP(timezone = True), nullable = False, server_default = text('now()'))
    user_id = Column(Integer, ForeignKey("user.id", ondelete= "CASCADE"), nullable = False)
    phone_no = Column(Integer, nullable= False)

    user = relationship("User")

class User(Base):
    __tablename__ = "user"

    email = Column(String, nullable= False, unique= True)
    password = Column(String, nullable= False)
    id = Column(Integer, primary_key = True, nullable = False)
    created_at = Column(TIMESTAMP(timezone = True), nullable = False, server_default = text('now()'))


class Votes(Base):
    __tablename__ = "votes"

    post_id = Column(Integer, ForeignKey("posts.id", ondelete= "CASCADE"), primary_key = True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete= "CASCADE"), primary_key = True)
    
