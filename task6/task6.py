# General:
# Install MySQL server (or any SQL like db)
# Make at least two tables (Entities from the previous task or any additional if needed)
# Make models for those Entities (from Task_5)
# Setup Hibernate for those Entities and local DB
# Check basic CRUD (create, read, update, and delete the BD records using Hibernate)
# Generate a few rows into all tables

#here i'm using sqlalchemy to manipulate with db via python

from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker, joinedload
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import text

Base = declarative_base()

#Creating models
class Person(Base):
    __tablename__ = 'person'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    is_employed = Column(Boolean, nullable=False)
    address = relationship("Address", back_populates="person", uselist=False, cascade="all, delete-orphan")


class Address(Base):
    __tablename__ = 'address'
    id = Column(Integer, primary_key=True)
    street = Column(String(255), nullable=False)
    city = Column(String(100), nullable=False)
    state = Column(String(50), nullable=False)
    person_id = Column(Integer, ForeignKey('person.id'))
    person = relationship("Person", back_populates="address")


# Connecting to MySQL DB
DATABASE_URL = 'mysql+mysqlconnector://root:rockstar44@localhost/task6_db'
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

# Writing clear function to clear db, because on first times
# I had duplicates in db after launching a code
def clear_database():
    session = Session()
    try:
        session.query(Address).delete()
        session.query(Person).delete()
        session.commit()

        session.execute(text("ALTER TABLE person AUTO_INCREMENT = 1"))
        session.execute(text("ALTER TABLE address AUTO_INCREMENT = 1"))
        session.commit()

        print("Database cleared")
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error clearing database: {e}")
    finally:
        session.close()


def person_exists(name, street):
    session = Session()
    try:
        existing_person = session.query(Person).join(Address).filter(
            Person.name == name,
            Address.street == street
        ).first()
        return existing_person is not None
    finally:
        session.close()

# CRUD Operations
def create_person(name, is_employed, street, city, state):
    if person_exists(name, street):
        print(f"Person {name} at {street} already exists. Skipping creation.")
        return None

    session = Session()
    try:
        new_person = Person(name=name, is_employed=is_employed)
        new_address = Address(street=street, city=city, state=state)
        new_person.address = new_address
        session.add(new_person)
        session.commit()
        print(f"Created: {name} with id {new_person.id}")
        return new_person.id
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error creating person: {e}")
    finally:
        session.close()


def read_person(person_id):
    session = Session()
    try:
        person = session.query(Person).options(joinedload(Person.address)).filter_by(id=person_id).first()
        if person:
            print(f"Read: {person.name}, ID: {person.id}, Employed: {person.is_employed}, "
                  f"Address: {person.address.street}, {person.address.city}, {person.address.state}")
        else:
            print(f"Person with id {person_id} not found")
    except SQLAlchemyError as e:
        print(f"Error reading person: {e}")
    finally:
        session.close()


def update_person(person_id, new_name, new_is_employed):
    session = Session()
    try:
        person = session.query(Person).filter_by(id=person_id).first()
        if person:
            person.name = new_name
            person.is_employed = new_is_employed
            session.commit()
            print(f"Updated: {new_name} with id {person_id}")
        else:
            print(f"Person with id {person_id} not found")
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error updating person: {e}")
    finally:
        session.close()


def delete_person(person_id):
    session = Session()
    try:
        person = session.query(Person).filter_by(id=person_id).first()
        if person:
            session.delete(person)
            session.commit()
            print(f"Deleted: {person.name} with id {person_id}")
        else:
            print(f"Person with id {person_id} not found")
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error deleting person: {e}")
    finally:
        session.close()

#function to show a list of persons in our db
def list_all_persons():
    session = Session()
    try:
        persons = session.query(Person).options(joinedload(Person.address)).all()
        print("\nAll persons in the database:")
        for person in persons:
            print(f"ID: {person.id}, Name: {person.name}, Employed: {person.is_employed}, "
                  f"Address: {person.address.street}, {person.address.city}, {person.address.state}")
    except SQLAlchemyError as e:
        print(f"Error listing persons: {e}")
    finally:
        session.close()


if __name__ == "__main__":
    clear_database()

    #Using all CRUD operations and showing a list of persons 2 times to see changes
    id1 = create_person("Mary", True, "123 Main St", "New York", "NY")
    id2 = create_person("Jane", False, "456 Elm St", "Los Angeles", "CA")
    id3 = create_person("Bob", True, "789 Oak St", "Chicago", "IL")

    list_all_persons()

    read_person(id1)
    read_person(id2)
    read_person(id3)

    update_person(id2, "Kate", True)
    read_person(id2)

    delete_person(id3)
    read_person(id3)

    list_all_persons()
