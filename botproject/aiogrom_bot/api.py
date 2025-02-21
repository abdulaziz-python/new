import requests
import json

BASE_URL = 'http://localhost:8000/api/v1'

def create_user(username, name, user_id):
    url = f"{BASE_URL}/bot-users"
    response = requests.get(url=url)

    if response.status_code == 200:
        data = response.json()  # JSON formatni o'qish
        user_exist = any(i["user_id"] == str(user_id) for i in data)
        if not user_exist:
            requests.post(url=url, data={'username': username, "name": name, "user_id": user_id})
            return "Foydalanuvchi yaratildi."
        else:
            return "Foydalanuvchi mavjud."
    else:
        return f"Xatolik: {response.status_code}, {response.text}"

    



def create_feedback(user_id, body):
    url = f"{BASE_URL}/feedbacks"
    if body and user_id :
        post = requests.post(url=url, data = {
            "user_id":user_id,
            "body":body
        })
        return "Adminga jo'natildi. Fikringiz uchun tashakkur."
    else:
        return "Amal oxiriga yetmadi."    

print(create_feedback("455652665", "zur"))