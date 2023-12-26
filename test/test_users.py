from fastapi.testclient import TestClient
from AppAlch.main import app
from AppAlch import models
from AppAlch.schemas import ReturnUser, AccessToken
from AppAlch.config import settings
from jose import jwt, JWTError
from .conftest import get_user_id
import pytest


def test_default(client):
    res = client.get("/")
    assert res.status_code ==200


def test_user(client):
    res = client.post("/users/", json = {"email":"admin5@admin.com","password":"12345"})
    new_return_user = ReturnUser(**res.json())
    assert new_return_user.email == "admin5@admin.com"
    assert res.status_code == 201

def test_correct_login(client,user,session):
    res = client.post("/login", data={"username":user["email"],"password":user["password"]})
    login_return = AccessToken(**res.json())
    payload= jwt.decode(login_return.access_token, settings.skey, algorithms=[settings.algorithm])
    assert login_return.token_type == "bearer"
    assert get_user_id(user["email"],session)==payload.get("user_id")
    assert res.status_code == 200

@pytest.mark.parametrize("username,password,expectedstatus" , [("admin@admin.com","passwordIncorrect",403),("admin@adminincorrect.com","password",403),("admin@adminincorrect.com","passwordincorrect",403),(None,"password",422),("admin@admin.com",None,422),(None,None,422)])
def test_incorrect_login(client,username,password,expectedstatus):
    res = client.post("/login", data={"username":username,"password":password})
    assert res.status_code == expectedstatus
    #assert res.json().get("detail") == "Invalid credentials"
