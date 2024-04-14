from fastapi.testclient import TestClient
import pytest
from main import app
import models
from sqlalchemy.orm import Session
from httpx import AsyncClient
from sqlalchemy.orm import declarative_base

"""class TestAPI():
  def setup(self):
    self.client = TestClient(app)"""

client = TestClient(app)

@pytest.mark.anyio
async def test_listar_chefs(self):
    response = self.client.get("/chef/listar/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

    
    
    
""" 
  @pytest.fixture
  def create_test_user(db: Session):
  test_user = models.Usuario(usuario="test_user", password="secret")
  db.add(test_user)
  db.commit()
  yield test_user
  db.delete(test_user)
  db.commit()

  def test_listar_chefs(self):
    response = self.client.get("/chef/listar/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
  # TEST METODO LOGIN  
  # Prueba credenciales correctas
  async def test_login_success(client: TestClient, db_dependency):
   # Create a test user in the database (outside the test)
  user_data = {"usuario": "test_user", "password": "secret"}
  # ... (code to create the user in the database)

  # Login with correct credentials
  response = client.get("/usuario/login/token/test_user/secret", db=db_dependency)
  assert response.status_code == 200
  assert "token" in response.json()

async def test_login_incorrect_user(client: TestClient, db_dependency):
  Tests login with incorrect username.
  response = client.get("/usuario/login/token/invalid_user/secret", db=db_dependency)
  assert response.status_code == 200
  assert "error" in response.json()
  assert response.json()["error"] == "Usuario no encontrado"

async def test_login_incorrect_password(client: TestClient, db_dependency):
  Tests login with incorrect password.
  # Create a test user (as done before the test_login_success)
  response = client.get("/usuario/login/token/test_user/wrong_password", db=db_dependency)
  assert response.status_code == 200
  assert "error" in response.json()
  assert response.json()["error"] == "Contraseña incorrecta"
  """ 