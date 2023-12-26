from fastapi.testclient import TestClient
from ..AppAlch.main import app
from ..AppAlch import models
from ..AppAlch.schemas import ReturnUser, AccessToken
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from ..AppAlch.config import settings
from ..AppAlch.database import get_db, Base
from ..AppAlch.tokenAuthentication import create_access_token
from jose import jwt, JWTError
import pytest
import os 

SQLALCHEMY_DATABASE_URL = f"postgresql://{os.getenv('DBUSERNAME')}:{os.getenv('DBPASSWORD')}@{os.getenv('DBHOSTNAME')}/{os.getenv('DBNAME')}_test"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestSession = sessionmaker(autoflush=False, autocommit=False, bind=engine)

    
#Other functions
def get_user_id(username,session):
    users = session.query(models.AlchemyUsers).all()
    for user in users:
        if username == user.email:
            return user.id
        

#Database fixtures
@pytest.fixture(scope="module")
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db= TestSession()
    try:
        yield db
    finally:
        db.close()
    
@pytest.fixture(scope="module")
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db]=override_get_db
    yield TestClient(app)
    

#User creation
@pytest.fixture(scope="module")
def user(client):
    client_data = {"email":"admin@admin.com","password":"password"}
    res = client.post("/users/", json=client_data)
    assert res.status_code == 201
    return client_data

@pytest.fixture(scope="module")
def second_user(client):
    client_data = {"email":"admin2@admin.com","password":"password"}
    res = client.post("/users/", json=client_data)
    assert res.status_code == 201
    return client_data


#token creation
@pytest.fixture()
def token(user,session):
    return create_access_token({"user_id":get_user_id(user["email"],session)})


#user authorization
@pytest.fixture()
def authorized_user(client, token):
    if "Authorization" not in client.headers:
        client.headers= {
            **client.headers,
            "Authorization":f"Bearer {token}"
        }
    return client


#substances creation
@pytest.fixture()
def database_preload(session,user):
    substances = [
        {
            'name': 'Agua',
            'molecular_formula': 'H2O',
            'molar_mass': 18.01528,
            'cas': '7732-18-5',
            'sga_classified': True,
            'hazardous_reactions': 'No aplica'
        },
        {
            'name': 'Ácido Clorhídrico',
            'molecular_formula': 'HCl',
            'molar_mass': 36.461,
            'cas': '7647-01-0',
            'sga_classified': True,
            'hazardous_reactions': 'Puede reaccionar con metales, liberando gas inflamable de hidrógeno.'
        },
        {
            'name': 'Oxígeno',
            'molecular_formula': 'O2',
            'molar_mass': 32,
            'cas': '7782-44-7',
            'sga_classified': True,
            'hazardous_reactions': 'Favorece la combustión; puede aumentar la velocidad de reacciones inflamables.'
        },
        {
            'name': 'Sacarosa',
            'molecular_formula': 'C12H22O11',
            'molar_mass': 342.29648,
            'cas': '57-50-1',
            'sga_classified': False,
            'hazardous_reactions': 'No es peligrosa en condiciones normales de uso.'
        },
        {
            'name': 'Cloro',
            'molecular_formula': 'Cl2',
            'molar_mass': 70.906,
            'cas': '7782-50-5',
            'sga_classified': True,
            'hazardous_reactions': 'Puede ser tóxico y corrosivo; reacciona violentamente con sustancias inflamables.'
        }
    ]
    substanceList=[]
    for substance in substances:
        new_substance=models.AlchemySubstances(owner_id=get_user_id(user["email"],session),**substance)
        session.add(new_substance)
        session.commit()
        session.refresh(new_substance)
        substanceList.append(new_substance)
    return substanceList

@pytest.fixture
def database_preload_seconduser(session,second_user):
    substances = [
    {
        'name': 'Metano',
        'molecular_formula': 'CH4',
        'molar_mass': 16.04,
        'cas': '74-82-8',
        'sga_classified': False,
        'hazardous_reactions': 'No es inflamable en condiciones normales de uso.'
    },
    {
        'name': 'Amoníaco',
        'molecular_formula': 'NH3',
        'molar_mass': 17.03,
        'cas': '7664-41-7',
        'sga_classified': True,
        'hazardous_reactions': 'Puede ser tóxico y corrosivo para los ojos y la piel.'
    },
    {
        'name': 'Dióxido de Carbono',
        'molecular_formula': 'CO2',
        'molar_mass': 44.01,
        'cas': '124-38-9',
        'sga_classified': False,
        'hazardous_reactions': 'No es tóxico, pero altas concentraciones pueden ser peligrosas.'
    },
    {
        'name': 'Hidróxido de Sodio',
        'molecular_formula': 'NaOH',
        'molar_mass': 39.997,
        'cas': '1310-73-2',
        'sga_classified': True,
        'hazardous_reactions': 'Corrosivo; puede causar quemaduras en contacto con la piel.'
    }]
    substanceList=[]
    for substance in substances:
        new_substance=models.AlchemySubstances(owner_id=get_user_id(second_user["email"],session),**substance)
        session.add(new_substance)
        session.commit()
        session.refresh(new_substance)
        substanceList.append(new_substance)
    return substanceList



@pytest.fixture
def preload_vote(user,database_preload,session):
    new_vote= models.AlchemyVotes(user_id=get_user_id(user["email"],session), substance_id=database_preload[0].id)
    session.add(new_vote)
    session.commit()
