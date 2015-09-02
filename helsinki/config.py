import os

hackpad_api_key = os.getenv('HACKPAD_API_KEY')
hackpad_api_secret = os.getenv('HACKPAD_API_SECRET')
facebook_id = os.getenv('FACEBOOK_ID')


class Config:

    def __init__(self):
        pass

    def get_hackpad_api_key(self):
        return hackpad_api_key

    def get_hackpad_api_secret(self):
        return hackpad_api_secret

    def get_facebook_id(self):
        return facebook_id


envs = ['HACKPAD_API_KEY', 'HACKPAD_API_SECRET', 'FACEBOOK_ID']


def create_env_file():
    f = open('config.env', 'w')
    s = ''
    for e in envs:
        s += env_entry(e)
    f.write(s)
    f.close()


def env_entry(env):
    value = os.getenv(env)
    if not value:
        raise Exception('The environment variable %s needs to be defined' % env)
    return "%s=%s\n" % (env, value)


if __name__ == "__main__":
    create_env_file()
