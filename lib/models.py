from sqlalchemy import ForeignKey, Column, Integer, String, MetaData
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.associationproxy import association_proxy

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    founding_year = Column(Integer())

    freebies = relationship("Freebie", backref="company")
    devs = association_proxy("freebies", "dev", creator=lambda dv: Freebie(dev=dv))

    def __repr__(self):
        return f"<Company {self.name}>"

    def give_freebie(self, dev, item_name, value):
        free = Freebie(
            item_name=item_name, value=value, dev_id=dev.id, company_id=self.id
        )
        print(free)
        return free


class Dev(Base):
    __tablename__ = "devs"

    id = Column(Integer(), primary_key=True)
    name = Column(String())

    freebies = relationship("Freebie", backref="dev")
    companies = association_proxy(
        "freebies", "company", creator=lambda comp: Freebie(company=comp)
    )

    def __repr__(self):
        return f"<Dev {self.name}>"


class Freebie(Base):
    __tablename__ = "freebies"

    id = Column(Integer(), primary_key=True)
    item_name = Column(String())
    value = Column(Integer())
    company_id = Column(Integer(), ForeignKey("companies.id"))
    dev_id = Column(Integer(), ForeignKey("devs.id"))

    def __repr__(self):
        return f"<Freebie {self.item_name}>"

    def print_details(self):
        return f"{self.dev.name} owns a {self.item_name} from {self.company.name}"
