from datetime import datetime
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    Float,
    Date,
    DateTime,
    ForeignKey,
    Text,
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
import os

Base = declarative_base()


class Contractor(Base):
    __tablename__ = "contractors"
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.now)
    name = Column(Text, unique=True)
    inn = Column(Text)

    invoices = relationship("Invoice", back_populates="contractor")
    acts = relationship("Act", back_populates="contractor")


class Employee(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.now)
    last_name = Column(Text)
    first_name = Column(Text)
    middle_name = Column(Text, nullable=True)
    department = Column(Text, nullable=True)
    position = Column(Text, nullable=True)


class StopWord(Base):
    __tablename__ = "stop_words"
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.now)
    word = Column(Text, unique=True)


class Invoice(Base):
    __tablename__ = "invoices"
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.now)
    number = Column(Text)
    date = Column(Date)
    amount = Column(Float)
    contractor_id = Column(Integer, ForeignKey("contractors.id"))
    organization_group = Column(Text)
    responsible_import = Column(Text)
    comment = Column(Text)
    deadline = Column(Date, nullable=True)
    deadline_days = Column(Integer, nullable=True)
    payment_date = Column(Date, nullable=True)
    motivated_person = Column(Text, nullable=True)
    status = Column(Text, default="Не оплачен")

    contractor = relationship("Contractor", back_populates="invoices")
    acts = relationship("Act", back_populates="invoice")


class Act(Base):
    __tablename__ = "acts"
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.now)
    number = Column(Text)
    filename = Column(Text)
    signing_date = Column(DateTime)
    amount = Column(Float)
    contractor_id = Column(Integer, ForeignKey("contractors.id"))
    invoice_id = Column(Integer, ForeignKey("invoices.id"), nullable=True)
    responsible_manager = Column(Text, nullable=True)

    contractor = relationship("Contractor", back_populates="acts")
    invoice = relationship("Invoice", back_populates="acts")


def get_db_path():
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), "database.db")


def get_engine():
    db_path = get_db_path()
    return create_engine(f"sqlite:///{db_path}")


def get_session():
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    return Session()


def init_db():
    engine = get_engine()
    Base.metadata.create_all(engine)


def clear_db(keep_employees: bool = False, keep_stop_words: bool = False):
    engine = get_engine()
    Base.metadata.bind = engine

    tables_to_clear = [Invoice, Act, Contractor]

    if not keep_stop_words:
        tables_to_clear.append(StopWord)

    if not keep_employees:
        tables_to_clear.append(Employee)

    with engine.begin() as conn:
        for table in tables_to_clear:
            conn.execute(table.__table__.delete())
