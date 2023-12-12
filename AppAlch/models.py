from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship
from .database import Base

class AlchemySubstances(Base):
    __tablename__ = "alchemySubstances"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    molecular_formula= Column(String, nullable=False)
    molar_mass= Column(Float, nullable=False)
    cas = Column(String, nullable=False)
    sga_classified=Column(Boolean, nullable=False, server_default='TRUE')
    hazardous_reactions=Column(String, nullable=True)
    created_at=Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    owner_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable="False")
    owner=relationship("AlchemyUsers")


class AlchemyUsers(Base):
    __tablename__ = "users"
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    id= Column(Integer, primary_key=True, nullable=False)
    created_at=Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))

class AlchemyVotes(Base):
    __tablename__="votes"
    user_id=Column(Integer,ForeignKey("users.id", ondelete="CASCADE"), nullable=False, primary_key=True )
    substance_id=Column(Integer, ForeignKey("alchemySubstances.id", ondelete="CASCADE"),nullable=False, primary_key=True )