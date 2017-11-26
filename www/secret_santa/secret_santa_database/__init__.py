from .. import app
from sqlalchemy import Column, Integer, String, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_sqlalchemy_session import flask_scoped_session

_base = declarative_base()
_engine = create_engine(app.config['SQLALCHEMY_DB_URI'])
_session_factory = sessionmaker(bind=_engine)
session = flask_scoped_session(_session_factory, app)

dude_participate_group = Table('dude_participate_group', _base.metadata,
                               Column('dude_id', Integer, ForeignKey('dudes.id')),
                               Column('group_id', Integer, ForeignKey('groups.id')),
                               )


class Dude(_base):
    __tablename__ = 'dudes'
    id = Column(Integer, primary_key=True)
    login = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    mail = Column(String, nullable=False, unique=True)

    groups = relationship('Group', secondary=dude_participate_group, back_populates="dudes")
    letters = relationship("Letter", back_populates="dude")
    gifts = relationship("Gift", back_populates="dude")

    def __repr__(self):
        return "<Dude(id='%s', login='%s', mail='%s')>" % (self.id, self.login, self.mail)


class Group(_base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    date = Column(Integer, nullable=False)

    dudes = relationship("Dude", secondary=dude_participate_group, back_populates="groups")
    letters = relationship('Letter', back_populates="group")

    def __repr__(self):
        return "<Group(id='%s', name='%s', date='%s')>" % (self.id, self.name, self.date)


class Letter(_base):
    __tablename__ = 'letters'
    id = Column(Integer, primary_key=True)
    uri = Column(String, nullable=False)
    id_group = Column(Integer, ForeignKey('groups.id'))
    id_dude = Column(Integer, ForeignKey('dudes.id'))
    # id_dude_receiver = Column(Integer, ForeignKey('dudes.id'))

    group = relationship("Group", back_populates="letters")
    dude = relationship("Dude", back_populates="letters")
    gift = relationship("Gift", back_populates="letter")

    def __repr__(self):
        return "<Letter(id='%s', uri='%s', id_group='%s', id_dude_emitter='%s', id_dude_receiver='%s')>" % (
            self.id, self.uri, self.id_group, self.id_dude_emitter, self.id_dude_receiver)


class Gift(_base):
    __tablename__ = 'gifts'
    id = Column(Integer, primary_key=True)
    id_dude = Column(Integer, ForeignKey('dudes.id'))
    id_letter = Column(Integer, ForeignKey('letters.id'))

    dude = relationship("Dude", back_populates="gifts")
    letter = relationship("Letter", back_populates="gift")


if app.config['SQLALCHEMY_DB_DROP']:
    _base.metadata.drop_all(_engine)
    _base.metadata.create_all(_engine)
