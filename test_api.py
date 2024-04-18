import requests
import random
import json


class TestClass:
    api_url = "https://choose-chef.vercel.app/"

    # Entra en la documentación de la API para comprobar que el servidor está activo (Status code 200)
    def test_servidor_activo(self):
        response = requests.get(self.api_url + "docs")

        assert response.status_code == 200

    # Hace login con las credenciales correctas y comprueba que la respuesta no es error
    def test_login(self):
        response = requests.get(self.api_url + "usuario/login/token/PruebaRepetido/123456")
        print(response.text)

        assert response.text != '{"error":"Usuario no encontrado"}' and "token" in response.text

    # Hace login con las credenciales erroneas y comprueba que responde con el mensaje de error correspondiente
    def test_error_login(self):
        response = requests.get(self.api_url + "usuario/login/token/Usuarioquenoexiste/1234")
        print(response.text)

        assert response.text == '{"error":"Usuario no encontrado"}'

    # POST Crear usuario nuevo
    def test_crear_usuario(self):
        # Con un número aleatorio nos aseguramos de que siempre se cree un usuario nuevo
        random_num = str(random.randint(1, 10000))

        # Datos de usuario para la prueba
        usuario_data = {
            "id": 0,
            "usuario": "Prueba" + random_num,
            "nombre": "Probando" + random_num,
            "password": random_num,
            "descripcion": "Usuario de prueba número " + random_num,
            "ubicacion": "Calle " + random_num,
            "email": random_num + "@prueba.prueba",
            "telefono": random_num,
            "tipo": "cliente",
            "comida": "",
            "servicio": "",
            "valoracion": 0
        }

        # Realiza una solicitud POST para crear un usuario
        response = requests.post(self.api_url + "usuario/crear/", json=usuario_data)

        print(response.text)

        # Verifica que la respuesta sea exitosa (código 200)
        assert response.status_code == 200
        assert response.text == '"El usuario se ha registrado correctamente"'

    # POST Error al crear usuario existente
    def test_crear_usuario_existente(self):
        # Datos de usuario ya existente (valor de usuario repetido)
        usuario_data = {
            "id": 0,
            "usuario": "PruebaRepetido",
            "nombre": "Probando",
            "password": "123456",
            "descripcion": "Error",
            "ubicacion": "Calle",
            "email": "prueba@prueba.prueba",
            "telefono": "0123456",
            "tipo": "cliente",
            "comida": "",
            "servicio": "",
            "valoracion": 0
        }

        # Realiza una solicitud POST para crear un usuario existente
        response = requests.post(self.api_url + "usuario/crear/", json=usuario_data)

        print(response.text)

        # Verifica que la respuesta sea un error (código 404)
        assert response.status_code == 404
        assert '"El usuario ya existe"' in response.text

    # TODO
    # GET Obtener Perfil
    def test_obtener_perfil(self):
        # Login para obtener el token
        loginok = requests.get(self.api_url + "usuario/login/token/PruebaRepetido/123456")

        # parsea el JSON de la respuesta
        consulta_token = json.loads(loginok.text)

        # Obtiene el valor del token
        token = consulta_token.get("token", "")

        response = requests.get(self.api_url + "usuario/perfil/", params={"token": token})
        print(response.text)

        # Verifica que la respuesta sea exitosa (código 200)
        assert response.status_code == 200

        # Verifica que la respuesta contenga datos válidos, en este caso el nombre de usuario
        assert response.json().get("usuario") == "PruebaRepetido"


    # TODO
    # POST Modificar usuario
    def test_modificar_usuario(self):
        # Creo un numero aleatorio para generar un nuevo valor a modificar
        random_num = str(random.randint(1, 10000))
        nuevo_nombre = "Proba" + random_num

        # Login para obtener el token
        loginok = requests.get(self.api_url + "usuario/login/token/PruebaRepetido/123456")

        # parsea el JSON de la respuesta
        consulta_token = json.loads(loginok.text)

        # Obtiene el valor del token
        token = consulta_token.get("token", "")

        # Datos de usuario ya existente con modificación
        nuevo_usuario_data = {
            "id": 0,
            "usuario": "PruebaRepetido",
            "nombre": nuevo_nombre,
            "password": "123456",
            "descripcion": "Error",
            "ubicacion": "Calle",
            "email": "prueba@prueba.prueba",
            "telefono": "0123456",
            "tipo": "cliente",
            "comida": "",
            "servicio": "",
            "valoracion": 0
        }

        # Realiza una solicitud POST para crear un usuario existente
        response_modificar = requests.post(self.api_url + "usuario/modificar/", json=nuevo_usuario_data, params={"token": token})

        # Comprobamos respuesta 200 a la petición
        assert response_modificar.status_code == 200

        #Comprobamos si se han guardado los nuevos datos de usuario
        response_revisar = requests.get(self.api_url + "usuario/perfil/", params={"token": token})

        # Verifica que la respuesta contenga el nuevo nombre
        assert response_revisar.json().get("nombre") == nuevo_nombre
        
    # TODO
    # GET Listar Chefs
    def test_listar_chefs(self):
      
      response = requests.get(self.api_url + "chef/listar/")
       
      # Verifica el código de estado de la respuesta
      assert response.status_code == 200

      # Verifica que la respuesta sea una lista
      assert isinstance(response.json(), list)

      # Verifica que la lista contenga al menos un chef
      assert len(response.json()) > 0

    # TODO
    # GET Listar ubicaciones con chefs
    def test_provincias_chefs(self):
      response = requests.get(self.api_url + "provincias/conChef/")
      # Verifica el código de estado de la respuesta
      assert response.status_code == 200
      # Verifica que la respuesta sea una lista
      assert isinstance(response.json(), list)
      
      # Verifica que la lista contenga las ubicaciones esperadas
      assert 'Barcelona' and 'Tarragona' and 'Girona' in response.json()
      # Verifica que no lista provincias que no tengan chef
      assert not 'Huesca' in response.json()

    # TODO
    # GET Listar Chef Por Ubicacion Comida Servicio
    def test_especifico_chefs(self):
      response = requests.get(self.api_url + "/chef/listar/por/Madrid/Mediterranea/Domicilio")
      # Verifica el código de estado de la respuesta
      assert response.status_code == 200
      # Verifica que la respuesta sea una lista
      assert isinstance(response.json(), list)
      # Verifica la respuesta esperada
      expected_response = [
        {
          "email": "paloma@madrid.com",
          "password": "1234",
          "descripcion": "Asisoy",
          "telefono": "666666666",
          "servicio": "Domicilio",
          "usuario": "Paloma",
          "id": 168,
          "nombre": "Paloma",
          "tipo": "chef",
          "ubicacion": "Madrid",
          "comida": "Mediterranea",
          "valoracion": 5
        }
      ]
      assert response.json() == expected_response
      
    # GET Listar todos los usuarios
    def test_admin_todos_usuarios(self):
        response = requests.get(self.api_url + "admin/listar")
        # Verifica el código de estado de la respuesta
        assert response.status_code == 200

        # Verifica que la respuesta sea una lista
        assert isinstance(response.json(), list)

        # Verifica que la lista contenga al menos un usuario
        assert len(response.json()) > 0

    # TODO
    # GET Obtener perfil admin
    def test_admin_obtener_perfil(self):
        response = requests.get(self.api_url + "admin/perfil/", params= {"usuario": "Paloma"})

        # Verifica que la respuesta sea exitosa (código 200)
        assert response.status_code == 200

        # Verifica que la respuesta contenga datos válidos, en este caso el nombre de usuario
        assert response.json().get("usuario") == "Paloma"
        print(response.text)

        assert response

    # TODO
    # POST Modificar usuario Admin
    def test_admin_modifica_usuario(self):
        usuario = "PruebaRepetido"
        # Creo un numero aleatorio para generar un nuevo valor a modificar
        random_num = str(random.randint(1, 10000))
        nuevo_nombre = "Proba" + random_num

        # Datos de usuario ya existente con modificación
        nuevo_usuario_data = {
            "id": 0,
            "usuario": usuario,
            "nombre": nuevo_nombre,
            "password": "123456",
            "descripcion": "Error",
            "ubicacion": "Calle",
            "email": "prueba@prueba.prueba",
            "telefono": "0123456",
            "tipo": "cliente",
            "comida": "",
            "servicio": "",
            "valoracion": 0
        }

        # Realiza una solicitud POST para crear un usuario existente
        response_modificar = requests.post(self.api_url + "admin/modificar/" + usuario, json=nuevo_usuario_data)

        # Comprobamos respuesta 200 a la petición
        assert response_modificar.status_code == 200

        #Comprobamos si se han guardado los nuevos datos de usuario
        response_revisar = requests.get(self.api_url + "admin/perfil/", params={"usuario": usuario})

        # Verifica que la respuesta contenga el nuevo nombre
        assert response_revisar.json().get("nombre") == nuevo_nombre

    # DELETE Eliminar usuario
    def test_eliminar_usuario(self):
        
        # Datos de usuario para la prueba
        usuario_data = {
            "id": 0,
            "usuario": "PruebaEliminar",
            "nombre": "Probando",
            "password": "123456",
            "descripcion": "Usuario de prueba número ",
            "ubicacion": "Calle ",
            "email": "pr@prueba.prueba",
            "telefono": "66666666",
            "tipo": "cliente",
            "comida": "",
            "servicio": "",
            "valoracion": 0
        }
        #creamos un nuevo usuario
        response_crear = requests.post(self.api_url + "usuario/crear/", json=usuario_data)
        assert response_crear.status_code == 200  
        # Eliminar usuario creado     
        response_eliminar = requests.delete(self.api_url + "usuario/PruebaEliminar")
        assert response_eliminar.status_code == 200  
        # Buscar el usuario eliminado y no encontrarlo
        response_buscar = requests.get(self.api_url + "admin/perfil/", params= {"usuario": "PruebaEliminar"})
        assert '"Usuario no encontrado"' in response_buscar.text
        
    """
       
    PENDIENTES DE IMPLEMENTAR
    
    # POST Crear reserva
    def test_crear_reserva(self):
        response = requests.get(self.api_url + "reserva/crear")
        print(response.text)

        assert response

   
    # POST Modificar Reserva
    def test_modificar_reserva(self):
        valor_id = "0"
        response = requests.get(self.api_url + "reserva/modificar/" + valor_id)
        print(response.text)

        assert response

   
    # GET Listar reserva
    def test_listar_reservas(self):
        token = "token"
        response = requests.get(self.api_url + "reserva/listar/" + token)
        print(response.text)

        assert response
    
    """ 