#!/usr/bin/env python3

# Script goes here!
from models import Company, Dev, Freebie
from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import random

fake = Faker()

engine = create_engine("sqlite:///freebies.db")
Session = sessionmaker(bind=engine)
session = Session()

swag = [
    "toy",
    "sticker",
    "hoody",
    "cap",
    "usb-drive",
    "headset",
    "backpack",
    "mouse",
    "keyboard",
    "notepad",
    "pen",
]


def delete_records():
    session.query(Company).delete()
    session.query(Dev).delete()
    session.query(Freebie).delete()
    session.commit()


def create_records():
    companies = [Company(name=fake.company()) for i in range(50)]
    devs = [Dev(name=fake.name()) for i in range(50)]
    freebies = [Freebie(item_name=random.choice(swag)) for i in range(50)]
    session.add_all(companies + devs + freebies)
    session.commit()
    return companies, devs, freebies


def relate(companies, devs, freebies):
    for free in freebies:
        free.dev = random.choice(devs)
        free.company = random.choice(companies)

    session.add_all(freebies)
    session.commit()
    return companies, devs, freebies


delete_records()
companies, devs, freebies = create_records()
companies, devs, freebies = relate(companies, devs, freebies)
