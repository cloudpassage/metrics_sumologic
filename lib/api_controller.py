import re
import cloudpassage
from config import CONFIG


class ApiController():
    @staticmethod
    def build_http_session():
        key_id = CONFIG['key_id']
        secret_key = CONFIG['secret_key']

        session = cloudpassage.HaloSession(key_id,
                                           secret_key,
                                           api_port=CONFIG["api_port"],
                                           api_host=CONFIG["api_hostname"])
        return cloudpassage.HttpHelper(session)

    def get(self, endpoint):
        return self.build_http_session().get(endpoint)
