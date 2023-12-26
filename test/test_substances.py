from typing import List
from ..AppAlch import schemas
import pytest

def deauthorize_client(client):
    if "Authorization" in client.headers:
        del client.headers["Authorization"]
    return client


def test_unauthorized_get_substances(client, database_preload):
    deauthorize_client(client)
    res= client.get("/substances/")
    assert res.status_code == 401

def test_unauthorized_get_one(client, database_preload):
    deauthorize_client(client)
    res= client.get("/substances/1")
    assert res.status_code == 401

def test_get_substances(authorized_user,database_preload):
    res= authorized_user.get("/substances/")
    list_of_substances = res.json()
    verified_substances=[schemas.ReturningSubstanceVotes(**item) for item in list_of_substances]
    assert res.status_code == 200

def test_get_one(authorized_user,database_preload):
    res= authorized_user.get("/substances/1")
    substance = res.json()
    verified_substance= schemas.ReturningSubstanceVotes(**substance)
    assert res.status_code == 200

@pytest.mark.parametrize("name, molecular_formula, molar_mass, cas, sga_classified, hazardous_reactions", [
    (('Sulfuric Acid', 'H2SO4', 98.079, '7664-93-9', True, 'Corrosive, reacts with metals')),
    ('Potassium Permanganate', 'KMnO4', 158.034, '7722-64-7', True, 'Oxidizing agent, reacts with combustible materials')])
def test_create_post(authorized_user, name, molecular_formula, molar_mass, cas, sga_classified,hazardous_reactions):
    res = authorized_user.post("/substances/", json = {"name":name, "molecular_formula":molecular_formula, "molar_mass":molar_mass, "cas":cas, "sga_classified":sga_classified,"hazardous_reactions":hazardous_reactions})
    verification_post=schemas.ReturningSubstance(**res.json())
    assert res.status_code == 201

@pytest.mark.parametrize("name, molecular_formula, molar_mass, cas, hazardous_reactions", [
    (('Sulfuric Acid', 'H2SO4', 98.079, '7664-93-9', 'Corrosive, reacts with metals')),
    ('Potassium Permanganate', 'KMnO4', 158.034, '7722-64-7', 'Oxidizing agent, reacts with combustible materials')])
def test_default_values_posts(authorized_user, name, molecular_formula, molar_mass, cas,hazardous_reactions):
    res = authorized_user.post("/substances/", json = {"name":name, "molecular_formula":molecular_formula, "molar_mass":molar_mass, "cas":cas,"hazardous_reactions":hazardous_reactions})
    verification_post=schemas.ReturningSubstance(**res.json())
    assert verification_post.sga_classified == True
    assert res.status_code == 201


@pytest.mark.parametrize("name, molecular_formula, molar_mass, cas, hazardous_reactions", [
    (('Sulfuric Acid', 'H2SO4', 98.079, '7664-93-9', 'Corrosive, reacts with metals')),
    ('Potassium Permanganate', 'KMnO4', 158.034, '7722-64-7', 'Oxidizing agent, reacts with combustible materials')])
def test_unauthorized_posts(client, name, molecular_formula, molar_mass, cas,hazardous_reactions):
    deauthorize_client(client)
    res = client.post("/substances/", json = {"name":name, "molecular_formula":molecular_formula, "molar_mass":molar_mass, "cas":cas,"hazardous_reactions":hazardous_reactions})
    assert res.status_code == 401


def test_delete_post(authorized_user):
    res=authorized_user.delete("/substances/1")
    assert res.status_code == 204

def test_delete_unauthorized(client):
    deauthorize_client(client)
    res= client.delete("/substances/1")
    assert res.status_code == 401

def test_delete_nonexistant(authorized_user):
    res=authorized_user.delete("/substances/1000")
    assert res.status_code == 404

def test_delete_non_owned_post(authorized_user,database_preload_seconduser):
    res=authorized_user.delete(f"/substances/{database_preload_seconduser[3].id}")
    assert res.status_code == 403

def test_update_post(authorized_user,database_preload):
    data={'name': 'Etanol','molecular_formula': 'C2H5OH','molar_mass': 46.07,'cas': '64-17-5','sga_classified': False,'hazardous_reactions': 'Inflamable; evite la inhalación y el contacto con los ojos.'}
    schemas.Substance(**data)
    res= authorized_user.put("/substances/2", json=data)
    print(res.text)
    assert res.status_code == 200

def test_nonauthorized_update_post(client):
    deauthorize_client(client)
    res= client.put("/substances/1", json={'name': 'Etanol',
                                                       'molecular_formula': 'C2H5OH',
                                                       'molar_mass': 46.07,
                                                       'cas': '64-17-5',
                                                       'sga_classified': False,
                                                       'hazardous_reactions': 'Inflamable; evite la inhalación y el contacto con los ojos.'}
                                )
    assert res.status_code == 401

def test_nonowned_update_post(authorized_user,database_preload_seconduser):
    res= authorized_user.put(f"/substances/{database_preload_seconduser[2].id}", json={'name': 'Etanol',
                                                       'molecular_formula': 'C2H5OH',
                                                       'molar_mass': 46.07,
                                                       'cas': '64-17-5',
                                                       'sga_classified': False,
                                                       'hazardous_reactions': 'Inflamable; evite la inhalación y el contacto con los ojos.'}
                                )
    assert res.status_code == 403