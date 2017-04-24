from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
 
from puppies import Shelter, Puppy, Base
import datetime
 
engine = create_engine('sqlite:///puppyshelter.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

def query_one():    
    """ Query all of the puppies and return the results in ascending alphabetical order """
    puppies = session.query(Puppy.name).order_by(Puppy.name.asc()).all()
    for puppy in puppies:
        print puppy[0]

def query_two():
    """ Query all of the puppies that are less than 6 months old organized by the youngest first """
    today = datetime.date.today()
    sixMonthsAgo = today - datetime.timedelta(days = 182)
    query = session.query(Puppy.name, Puppy.dateOfBirth)\
        .filter(Puppy.dateOfBirth >= sixMonthsAgo)\
        .order_by(Puppy.dateOfBirth.desc())

    for q in query:
        name = q[0]
        dob = str(q[1])
        print "Name: " + name + "\nDOB: " + dob + "\n"

def query_three():
    """ Query all puppies by ascending weight """
    query = session.query(Puppy.name, Puppy.weight).order_by(Puppy.weight.asc()).all()

    for q in query:
        name = q[0]
        weight = str(int(q[1]))

        print "Name: " + name + "\nWeight: " + weight + "\n"

def query_four():
    """ Query all puppies grouped by the shelter in which they are staying """
    query = session.query(Shelter, func.count(Puppy.id)).join(Puppy).group_by(Shelter.id).all()
    for q in query:
        id = str(q[0].id)
        name = q[0].name
        count = str(q[1])

        print "Shelter ID: " + id + "\nShelter Name: " + name + "\nPuppy Count: " + count + "\n"

query_four()