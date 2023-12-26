import pytest

def deauthorize_client(client):
    if "Authorization" in client.headers:
        del client.headers["Authorization"]

def test_vote(authorized_user,database_preload):
    data={"substance_id":database_preload[3].id,"direction":True}
    res = authorized_user.post("/vote", json=data)
    assert res.status_code == 201

def test_vote_non_authorized(client,database_preload):
    deauthorize_client(client)
    data={"substance_id":database_preload[3].id,"direction":True}
    res= client.post("/vote", json=data)
    assert res.status_code == 401

def test_vote_not_existing_substance(authorized_user,database_preload):
    data={"substance_id":10000,"direction":True}
    res = authorized_user.post("/vote", json=data)
    assert res.status_code == 404

def test_double_votes(authorized_user,database_preload,preload_vote):
    data={"substance_id":database_preload[0].id,"direction":True}
    res = authorized_user.post("/vote", json=data)
    assert res.status_code == 403

