# The general task for all:
# 1. Serialization-Deserialization: 
# a) Make some complex models using your variant.
# b) Make it serializable.
# c) Read JSON from “input.json”
# d) and deserialize it to POJO. 
# e) Then change a few fields and save it to “output.json”.
# f) Do the same for XML.
# 1. Stream:
# a) Generate 10 random objects using a class from a previous task 
# b) Sort it using any two fields using stream.
# c) Filter it by any two fields custom filter.
# d) Collect it to List with *main field(s).

# V5
# {
#   "name": "Mary",
#   "isEmployed": true,
#   "address": {
#     "street": "123 Main St",
#     "city": "Seattle",
#     "state": "WA"
#   }
# }
# <person>
#   <name>Mary</name>
#   <isEmployed>true</isEmployed>
#   <address>
#     <street>123 Main St</street>
#     <city>Seattle</city>
#     <state>WA</state>
#   </address>
# </person>

#----------
#task code 

import json
import xml.etree.ElementTree as ET
from dataclasses import dataclass, asdict
import os
import random
from typing import List

# 1.Serialization-Deserialization
@dataclass
class Address:
    street: str
    city: str
    state: str

@dataclass
class Person:
    name: str
    isEmployed: bool
    address: Address

    def to_dict(self):
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data):
        address_data = data.pop('address')
        address = Address(**address_data)
        return cls(**data, address=address)
    
    def to_xml(self):
        root = ET.Element('person')
        ET.SubElement(root, 'name').text = self.name
        ET.SubElement(root, 'isEmployed').text = str(self.isEmployed).lower()
        address = ET.SubElement(root, 'address')
        ET.SubElement(address, 'street').text = self.address.street
        ET.SubElement(address, 'city').text = self.address.city
        ET.SubElement(address, 'state').text = self.address.state
        return ET.tostring(root, encoding='unicode')
    
    @classmethod
    def from_xml(cls, xml_string):
        root = ET.fromstring(xml_string)
        name = root.find('name').text
        isEmployed = root.find('isEmployed').text.lower() == 'true'
        address = root.find('address')
        street = address.find('street').text
        city = address.find('city').text
        state = address.find('state').text
        return cls(name, isEmployed, Address(street, city, state))

def json_serialization():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(current_dir, 'input.json')
    
    with open(input_path, 'r') as f:
        input_data = json.load(f)

    person = Person.from_dict(input_data)

    person.name = "John"
    person.address.city = "New York"

    output_path = os.path.join(current_dir, 'output.json')
    with open(output_path, 'w') as f:
        json.dump(person.to_dict(), f, indent=2)

#XML
def xml_serialization():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(current_dir, 'input.xml')
    
    with open(input_path, 'r') as f:
        input_xml = f.read()

    person = Person.from_xml(input_xml)

    person.name = "Alice"
    person.address.state = "TX"
    person.address.city = "Phoenix"

    output_path = os.path.join(current_dir, 'output.xml')
    with open(output_path, 'w') as f:
        f.write(person.to_xml())

# 2.Stream operations
def generate_random_person() -> Person:
    names = ["John", "Jane", "Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace", "Henry"]
    cities = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose"]
    states = ["NY", "CA", "IL", "TX", "AZ", "PA", "TX", "CA", "TX", "CA"]
    
    return Person(
        name=random.choice(names),
        isEmployed=random.choice([True, False]),
        address=Address(
            street=f"{random.randint(100, 999)} {random.choice(['Main', 'Oak', 'Pine', 'Maple', 'Cedar'])} St",
            city=random.choice(cities),
            state=random.choice(states)
        )
    )

def stream_operations():
    #generating
    people = [generate_random_person() for _ in range(10)]

    #sorting and filtering
    sorted_people = sorted(people, key=lambda p: (p.name, p.address.city))
    filtered_people = list(filter(lambda p: p.isEmployed and p.address.state in ["CA", "NY"], people))


    main_fields = [(p.name, p.address.city) for p in filtered_people]

    print("Sorted people:")
    for person in sorted_people:
        print(f"{person.name}, {person.address.city}")

    print("\nFiltered people:")
    for person in filtered_people:
        print(f"{person.name}, {person.address.city}, {person.address.state}")

    print("\nMain fields of filtered people:")
    for name, city in main_fields:
        print(f"{name}, {city}")

if __name__ == "__main__":
    json_serialization()
    xml_serialization()
    stream_operations()