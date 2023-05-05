import requests


class UserLogin:
    def __init__(self, email, password, remember):
        self.email = email
        self.password = password
        self.remember = remember


class UserRegister:
    def __init__(self, name, last_name, email, password, repeat_password):
        self.name = name
        self.lastName = last_name
        self.email = email
        self.password = password
        # self.repeatPassword = repeat_password
        # {
        #     "name": "John",
        #     "lastName": "Dou",
        #     "email": "test@test.com",
        #     "password": "Qwerty12345",
        #     "repeatPassword": "Qwerty12345"
        # }
# {
#   "photo": "user-1621352948859.jpg",
#   "name": "John",
#   "lastName": "Dou",
#   "dateBirth": "2021-03-17T15:21:05.000Z",
#   "country": "Ukraine"
# }

class DataUserProfileGet:
    def __init__(self, user_id, photo_file_name, name, last_name):
        self.userId = user_id
        self.photoFilename = photo_file_name
        self.name = name
        self.lastName = last_name

    def __str__(self):
        return self.__dict__


class UserProfileGet:
    def __init__(self, status: str, data: DataUserProfileGet):
        self.status = status
        self.data = data.__dict__

    def __str__(self):
        return self.__dict__


class UpdateUserProfilePut:
    def __init__(self, photo, name, last_name, date_birth, country):
        self.photo = photo
        self.name = name
        self.lastName = last_name
        self.dateBirth = date_birth
        self.country = country

class TestAuth:
    def setup_class(self):
        self.session = requests.session()
        user_register = UserRegister(name="Name", last_name="LastName", email="testForAQASecond@test.com", password="Qwerty12345", repeat_password="Qwerty12345")
        self.session.post(url="https://qauto2.forstudy.space/api/auth/signup", json=user_register.__dict__)

    def setup_method(self):
        self.user_to_login = UserLogin("testForAQASecond@test.com", "Qwerty12345", False)
        self.session.post(url="https://qauto2.forstudy.space/api/auth/signin",
                          json=self.user_to_login.__dict__)

    def test_user_update_photo(self):
        user_to_update = UpdateUserProfilePut(photo="default-user.png", name="John", last_name="Dou", country="Czech",
                                              date_birth="2021-03-17T15:21:05.000Z")

        result = self.session.put("https://qauto2.forstudy.space/api/users/profile", json=user_to_update.__dict__)
        assert result.json()["status"] == "ok"
        assert result.json()["data"]["country"] == "Czech"

    def test_user_login(self):
        self.session.get("https://qauto2.forstudy.space/api/auth/logout")
        result = self.session.post(url="https://qauto2.forstudy.space/api/auth/signin",
                                   json=self.user_to_login.__dict__)
        assert result.json()["status"] == "ok"

    def test_delete_user(self):
        result = self.session.delete("https://qauto2.forstudy.space/api/users")
        assert result.json()["status"] == "ok"

    def test_check_user_profile(self):
        result = self.session.get(url="https://qauto2.forstudy.space/api/users/profile")
        data = DataUserProfileGet(20560, 'default-user.png', 'John', 'Dou')
        profile = UserProfileGet('ok', data)
        assert result.json()["data"] == data.__dict__
        assert result.json()["status"] == 'ok'

    def teardown_method(self):
        self.session.get("https://qauto2.forstudy.space/api/auth/logout")

    def teardown_class(self):
        self.session.post(url="https://qauto2.forstudy.space/api/auth/signin",
                          json=self.user_to_login.__dict__)
        self.session.delete("https://qauto2.forstudy.space/api/users")
