from redis import Redis
from random import randint
import requests
import orjson
from django.conf import settings

class OtpService:
    def __init__(self):
        self.redis_client = Redis.from_url(settings.REDIS_URL)

    def _otp_key(self, phone: str) -> str:
        return f"otp:{phone}"

    def generate_code(self) -> int:
        return randint(100000, 999999)

    def send_otp(self, phone: str, code: int, expire_time: int = 300):
        """Store OTP in Redis and send SMS."""
        self.redis_client.set(self._otp_key(phone), code, ex=expire_time)
        print(f"[DEBUG] OTP for {phone}: {code}")  # Just print it in console
        return True  # Always success

        # Example using Eskiz (replace with your SMS API)
        # sms_text = f"Your verification code is {code}"
        # response = requests.post(
        #     "https://notify.eskiz.uz/api/message/sms/send",
        #     headers={"Authorization": f"Bearer {settings.ESKIZ_TOKEN}"},
        #     data={
        #         "mobile_phone": phone,
        #         "message": sms_text,
        #         "from": "4546"
        #     },
        # )
        # return response.status_code == 200

    def verify_otp(self, phone: str, code: str) -> bool:
        saved_code = self.redis_client.get(self._otp_key(phone))
        if not saved_code:
            return False
        return saved_code.decode() == code
