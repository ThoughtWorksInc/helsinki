import os


hackpad_api_key = os.getenv('HACKPAD_API_KEY')
hackpad_api_secret = os.getenv('HACKPAD_API_SECRET')


class Config:

    def __init__(self):
        pass

    def get_hackpad_api_key(self):
        return hackpad_api_key

    def get_hackpad_api_secret(self):
        return hackpad_api_secret
