import pytest
from author.models import Author


@pytest.mark.django_db
class TestRegistration:
    url = 'http://127.0.0.1:8000/api/register'
    data = {
        "first_name": "Somebody",
        "last_name": "JustToldMe",
        "birth_date": "11.11.2011",
        "email": "thiswrld@isgonna.rollme",
        "password": "!QAZ@WSX"
    }

    def test_user_registration(self, client):
        assert Author.objects.filter(email=self.data['email']).exists() is False
        response = client.post(self.url, self.data)
        assert response.status_code == 201
        assert response.data['first_name'] == self.data['first_name']
        assert response.data['last_name'] == self.data['last_name']
        assert response.data['birth_date'] == self.data['birth_date']
        assert response.data['email'] == self.data['email']
        assert Author.objects.filter(email=self.data['email']).exists() is True

    def test_user_reg_common_pass(self, client):
        data = self.data
        data.update({'password': '1a'})
        response = client.post(self.url, data)
        assert response.status_code == 400
        assert response.data[0] == 'This password is too short. It must contain at least 8 characters.'

    def test_user_reg_wrong_date(self, client):
        data = self.data
        data.update({'birth_date': '11.11.11'})
        response = client.post(self.url, data)
        assert response.status_code == 400
        assert response.data['non_field_errors'][0] == 'Unsupported date format. Use dd.mm.yyyy'

    def test_user_reg_without_email(self, client):
        data = self.data
        data.pop('email')
        response = client.post(self.url, data)
        assert response.status_code == 400
        assert response.data['email'][0] == 'This field is required.'
