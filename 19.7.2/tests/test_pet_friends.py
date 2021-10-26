from api import PetFriends
from settings import valid_email, valid_password, name_pet_add, animal_type_pet_add, age_pet_add, photo_pet_add
from settings import new_name, new_animal_type, new_age, photo_pet
from settings import email_false, password_false, name_symbol, name_long, animal_type_symbol, age_symbol
import os

pf = PetFriends()


# Проверка на валидые логин и пароль, возращает статус и уникальный ключ
def test_get_api_key_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200

# Проверка, что результат есть уникальный ключ
    assert 'key' in result


# Пролучение списка моих питомцев
def test_get_my_pets_with_valid_key(filter='my_pets'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200

# Проверка, что список питомцев не пустой
    assert len(result['pets']) >= 0


# Проверяем, что можем добавить нового питомца с валидными данными
def test_add_new_pets(name=name_pet_add, animal_type=animal_type_pet_add, age=age_pet_add, pet_photo=photo_pet_add):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name


# Проверка возможности удаления питомца
def test_delete_pet():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        raise Exception("СПИСОК ПУСТОЙ")
    else:
        pet_id = my_pets['pets'][0]['id']
        status, _ = pf.delete_pet(auth_key, pet_id)
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    assert status == 200
    assert pet_id not in my_pets.values()


# Проверка возможности обновления данных питомца
def test_put_info_pet(name=new_name, animal_type=new_animal_type, age=new_age, pet_photo=photo_pet_add):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
# Проверка, что список питомцев не пустой. При пустом списке выводится соответствующие сообщение
    if len(my_pets['pets']) > 0:
        status, result = pf.put_info_pet(auth_key, my_pets['pets'][0]['id'], name, animal_type, age, pet_photo)
        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("СПИСОК ПУСТОЙ")


# Проверка добавление нового притомца без фото
def test_add_new_pets_not_photo(name=name_pet_add, animal_type=animal_type_pet_add, age=age_pet_add):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_not_photo(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name


# Проверка возможности изменения фото питомца
def test_add_pets_photo(pet_photo=photo_pet):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) > 0:
        pet_id = my_pets['pets'][0]['id']
        name = my_pets['pets'][0]['name']
        animal_type = my_pets['pets'][0]['animal_type']
        age = my_pets['pets'][0]['age']
        status, result = pf.add_pet_photo(auth_key, pet_id, name, animal_type, age, pet_photo)
        assert status == 200
        assert result
    else:
        raise Exception("СПИСОК ПУСТОЙ")


# Дополнительные тесты


# 1. Проверка авторизации при не валидных емаил и пароле.
def test_get_api_key_user(email=email_false, password=password_false):
    status, result = pf.get_api_key(email, password)
    assert status == 200, 'Код ошибки 403.Указанная неверная комбинация email и password'
    assert 'key' not in result


# 2. Получение списка питомцев при не валидном уникальном ключе.
def test_get_my_pets_with_key_false(filter='my_pets'):
    auth_key = ""
    status, result = pf.get_list_of_pets_false_key(auth_key, filter)
    assert status == 200, 'Код ошибки 403.Указан неправильный уникальный ключ auth_key '
    assert 'key' not in result


# 3. Проверка создания нового питомца при не заполненом имени.
def test_add_new_pets_false_info1(name='', animal_type='Коала', age='1', pet_photo='images/photo_3.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == ''
    print('Ошибка в имени питомца - ' + "< " + result['name'] + " >")


# 4. Проверка создания нового питомца с некорректным именем.
def test_add_new_pets_false_info2(name=name_symbol, animal_type='Коала', age='1', pet_photo='images/photo_3.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name_symbol
    print('Ошибка в имени питомца - ' + "< " + result['name'] + " >")


# 5. Проверка создания нового питомца с длинным именем.
def test_add_new_pets_false_info3(name=name_long, animal_type='Коала', age='1', pet_photo='images/photo_3.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name_long
    print('Ошибка в имени питомца. Слишком длинное имя- ' + "< " + result['name'] + " >")


# 6. Проверка создания нового питомца при не заполненой породе.
def test_add_new_pets_false_info4(name='Муся', animal_type='', age='1', pet_photo='images/photo_3.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['animal_type'] == ''
    print('Ошибка.Не указана порода питомца - ' + "< " + result['animal_type'] + " >")


# 7. Проверка создания нового питомца с некорректным указанием породы.
def test_add_new_pets_false_info5(name='Муся', animal_type=animal_type_symbol, age='1', pet_photo='images/photo_3.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['animal_type'] == animal_type_symbol
    print('Ошибка.Не правильно указана порода питомца - ' + "< " + result['animal_type'] + " >")


# 8. Проверка создания нового питомца при не заполненом возрасте.
def test_add_new_pets_false_info6(name='Муся', animal_type='Коала', age='', pet_photo='images/photo_3.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['age'] == ''
    print('Ошибка. Не указан возраст питомца - ' + "< " + result['age'] + " >")


# 9. Проверка создания нового питомца с указанием некорректного возраста
def test_add_new_pets_false_info7(name='Муся', animal_type='Коала', age=age_symbol, pet_photo='images/photo_3.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['age'] == age_symbol
    print("Ошибка. Не правильно указан возраст питомца - " + "< " + result['age'] + " >")


# 10. Проверка создания нового питомца с указанием отрицательного возраста
def test_add_new_pets_false_info8(name='Муся', animal_type='Кола', age='-5', pet_photo='images/photo_3.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    age = int(result['age'])
    assert status == 200
    assert age < 0
    print("Ошибка. Указан отрицательный возраст питомца - " + "< " + result['age'] + " >")
