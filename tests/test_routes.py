import os
import logging
from service.common import status  # HTTP Status Codes
from service.models import db, Users, init_db
from service.routes import app
import tempfile
from service import models
import pytest
from flask import session, template_rendered


RAND_NAME = {'nm': 'John'}
RAND_EMAIL = {'email': 'John@gmail.com'}
RAND_NAME2 = {'nm': 'nhoJ'}
RAND_EMAIL2 = {'email': "nhoJ@gmail.com"}



@pytest.fixture
def client(tmp_path_factory):
    client = app.test_client()
    yield client


@pytest.fixture
def captured_templates():
    recorded = []

    def record(sender, template, context, **extra):
        recorded.append((template, context))

    template_rendered.connect(record, app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app)

# def test_view(captured_templates, client):
    
#     # create random accounts
#     user1=models.Users("John",'John@gmail.com')
#     user1.create()
#     user2=models.Users("nhoJ", 'nhoJ@gmail.com')
#     user2.create()

#     response = client.get('/view')
#     assert response.status_code == status.HTTP_200_OK

#     template, context = captured_templates[-1]

#     assert template.name == "view.html"
#     # assert context["values"][2].name == 'hi'

#     assert "values" in context
#     assert len(context["values"]) == 2
#     assert context["values"][0].name == RAND_NAME['nm']
#     assert context["values"][0].email == RAND_EMAIL['email']
#     assert context["values"][1].name == RAND_NAME2['nm']
#     assert context["values"][1].email == RAND_EMAIL2['email']

def test_user(client):
    # Test unauthorized get request to /user page
    response = client.get('/user')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    # login
    client.post('/login', data= RAND_NAME) 

    # Test post request to enter email
    response = client.post('/user', data=RAND_EMAIL)
    assert response.status_code == status.HTTP_200_OK


def test_login(client):
    # Test get request
    response = client.get('/login')
    assert response.status_code == status.HTTP_200_OK
    
    # Test post requests
    response = client.post('/login', data=RAND_NAME)
    with client.session_transaction() as session:
        if session['user'] == 'John':
            assert response.status_code == status.HTTP_302_FOUND
    
    response = client.get('/login')
    assert response.status_code == status.HTTP_302_FOUND

