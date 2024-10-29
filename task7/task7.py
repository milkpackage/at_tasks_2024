#Implement OneToOne, OneToMany, and ManyToMany relations in your models from the previous task.(Task_6)
#Test it by CRUD.

from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, Table
from sqlalchemy.orm import declarative_base, relationship, sessionmaker, joinedload
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import text

Base = declarative_base()

#ManyToMany relationship table
person_hobby = Table('person_hobby', Base.metadata,
                     Column('person_id', Integer, ForeignKey('person.id')),
                     Column('hobby_id', Integer, ForeignKey('hobby.id'))
                     )

class Person(Base):
    __tablename__ = 'person'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    is_employed = Column(Boolean, nullable=False)
    #OneToOne relationship with Address
    address = relationship("Address", back_populates="person", uselist=False, cascade="all, delete-orphan")
    #OneToMany relationship with Phone
    phones = relationship("Phone", back_populates="person", cascade="all, delete-orphan")
    #ManyToMany relationship with Hobby
    hobbies = relationship("Hobby", secondary=person_hobby, back_populates="persons")


class Address(Base):
    __tablename__ = 'address'
    id = Column(Integer, primary_key=True)
    street = Column(String(255), nullable=False)
    city = Column(String(100), nullable=False)
    state = Column(String(50), nullable=False)
    person_id = Column(Integer, ForeignKey('person.id'))
    # OneToOne relationship with Person
    person = relationship("Person", back_populates="address")


class Phone(Base):
    __tablename__ = 'phone'
    id = Column(Integer, primary_key=True)
    number = Column(String(20), nullable=False)
    person_id = Column(Integer, ForeignKey('person.id'))
    #Many side of OneToMany relationship
    person = relationship("Person", back_populates="phones")


class Hobby(Base):
    __tablename__ = 'hobby'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    #ManyToMany relationship with Person
    persons = relationship("Person", secondary=person_hobby, back_populates="hobbies")


#Database connection
DATABASE_URL = 'mysql+mysqlconnector://root:rockstar44@localhost/task6_db'
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


def clear_database():
    session = Session()
    try:
        session.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
        session.execute(person_hobby.delete())
        session.query(Phone).delete()
        session.query(Hobby).delete()
        session.query(Address).delete()
        session.query(Person).delete()
        session.execute(text("SET FOREIGN_KEY_CHECKS = 1"))
        session.commit()

        for table in ['person', 'address', 'phone', 'hobby']:
            session.execute(text(f"ALTER TABLE {table} AUTO_INCREMENT = 1"))
        session.commit()
        print("Database cleared")
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error clearing database: {e}")
    finally:
        session.close()


def test_relationships():
    session = Session()
    try:
        #Creating test data
        hobby1 = Hobby(name="Reading")
        hobby2 = Hobby(name="Gaming")
        session.add_all([hobby1, hobby2])

        #Creating person with all relationships
        person = Person(
            name="Kate",
            is_employed=True,
            address=Address(street="123 Main St", city="Boston", state="MA"),
            phones=[
                Phone(number="555-0101"),
                Phone(number="555-0102")
            ],
            hobbies=[hobby1, hobby2]
        )
        session.add(person)
        session.commit()

        #Read and verify relationships
        person = session.query(Person).options(
            joinedload(Person.address),
            joinedload(Person.phones),
            joinedload(Person.hobbies)
        ).first()

        print("\nCreated Person with relationships:")
        print(f"Person: {person.name}")
        print(f"Address: {person.address.street}")
        print("Phones:", [phone.number for phone in person.phones])
        print("Hobbies:", [hobby.name for hobby in person.hobbies])

        #Update relationships
        person.phones.append(Phone(number="555-0103"))
        hobby3 = Hobby(name="Running")
        session.add(hobby3)
        person.hobbies.append(hobby3)
        session.commit()

        print("\nAfter updates:")
        print("Phones:", [phone.number for phone in person.phones])
        print("Hobbies:", [hobby.name for hobby in person.hobbies])

        #Delete
        session.delete(person)
        session.commit()

        print("\nAfter deletion:")
        print(f"Persons in database: {session.query(Person).count()}")
        print(f"Addresses in database: {session.query(Address).count()}")
        print(f"Phones in database: {session.query(Phone).count()}")
        print(f"Hobbies in database: {session.query(Hobby).count()}")

    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error during testing: {e}")
    finally:
        session.close()


if __name__ == "__main__":
    clear_database()
    test_relationships()