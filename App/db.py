#!/usr/bin/python3.5
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy import MetaData, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import exc
import os

engine = create_engine(os.environ['db_local'])
Base = declarative_base()
metadata = MetaData(bind=engine)

class Jobs(Base):
    __tablename__ = "jobs"
 
    id = Column(String(20), primary_key=True)
    company = Column(String(100))
    title = Column(String(200))
    date_created = Column(DateTime)
    category = Column(String(100))

    def __repr__(self):
    	return("""Job(id='%s', company='%s', title='%s', date_created='%s, category='%s')
    			""" %
    			(self.id
    			,self.company
    			,self.title
    			,self.date_created
    			,self.category
    			))

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
session.commit()

