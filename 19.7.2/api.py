import json
import requests

from requests_toolbelt.multipart.encoder import MultipartEncoder


class PetFriends:
    def __init__(self):
        self.base_url = "https://petfriends1.herokuapp.com/"

    def get_api_key(self, email, password):
        """ Метод делает запрос к API сервера и возвращает статус запроса и результат в формате JSON с уникальным
        ключем пользователя, найденного по указаному email и password"""
        headers = {
            'email': email,
            'password': password
        }
        res = requests.get(self.base_url + 'api/key', headers=headers)
        status = res.status_code

        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def get_list_of_pets(self, auth_key, filter):
        """Метод делает запрос к API сервера и возвращает статус запроса и результат со списком
        найденных питомцев, совпадающих с фильтром. На данный момент фильтр пустое значение - получить
        список всех питомцев, либо 'my_pets' - получить список моих питомцев"""
        headers = {'auth_key': auth_key['key']}
        filter = {'filter': filter}
        res = requests.get(self.base_url+'api/pets', headers=headers, params=filter)
        status = res.status_code

        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def add_new_pet(self, auth_key: json, name: str, animal_type: str, age: str, pet_photo: str):
        """Метод использует API для отправки данных о новом питемце на сервер и возвращает статус запроса в формате JSON
         с указанием данных питомца"""
        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age,
                'pet_photo': (pet_photo,  open(pet_photo, 'rb'), 'image/jpeg')
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}
        res = requests.post(self.base_url+'api/pets', headers=headers, data=data)
        status = res.status_code

        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        print(result)
        return status, result

    def delete_pet(self, auth_key: json, pet_id: str):
        """Метод делает запрос на сервер на удаление питомца по его ID и возвращает статус запроса в формате JSON
         с подтверждением удаления питомца"""
        headers = {'auth_key': auth_key['key']}
        res = requests.delete(self.base_url+'api/pets/' + pet_id, headers=headers)
        status = res.status_code

        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        print(result)
        return status, result

    def put_info_pet(self, auth_key: json, pet_id: str, name: str, animal_type: str, age: str, pet_photo: str):
        """Метод делает запрос к серверу на изменение информации о питомце по ID и возвращает статус запроса в формате
         JSON с измененой информацией о питомце или выдает текстовое сообщение об ошибке при пусто списке питомцев"""
        headers = {'auth_key': auth_key['key']}
        data = {'name': name, 'animal_type': animal_type, 'age': age, 'pet_photo': pet_photo}
        res = requests.put(self.base_url + 'api/pets/' + pet_id, headers=headers, data=data)
        status = res.status_code

        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        print(result)
        return status, result

    def add_new_pet_not_photo(self, auth_key: json, name: str, animal_type: str, age: str):
        """Метод использует API для отправки данных о новом питемце на сервер без фото и возвращает статус запроса
         в формате JSON с указанием данных питомца"""
        headers = {'auth_key': auth_key['key']}
        data = {'name': name, 'animal_type': animal_type, 'age': age}
        res = requests.post(self.base_url+'api/create_pet_simple', headers=headers, data=data)
        status = res.status_code

        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        print(result)
        return status, result

    def add_pet_photo(self, auth_key: json, pet_id: str, name: str, animal_type: str, age: str, pet_photo: str):
        """Метод использует API для отправки данных к серверу на изменение фото питомца и возвращает статус запроса
         в формате JSON с новым фото питомца или выдает текстовое сообщение об ошибке при пусто списке питомцев"""
        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age,
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}
        res = requests.post(self.base_url+'api/pets/set_photo/' + pet_id, headers=headers, data=data)
        print(res.request.body)
        status = res.status_code

        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        print(result)
        return status, result

    def get_list_of_pets_false_key(self, auth_key, filter):
        """Делает запрос к API сервера и возвращает статус запроса в формате JSON"""
        headers = {'auth_key': auth_key}
        filter = {'filter': filter}
        res = requests.get(self.base_url+'api/pets', headers=headers, params=filter)
        status = res.status_code

        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result
