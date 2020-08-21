import jwt
import json
from datetime import datetime, timedelta

import logging
FORMAT = '%(asctime)-15s %(levelname)s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)

class JWT_Crypto:


    def generateJWT(self, key, messageDict: dict, diff:timedelta):
        messageDict["exp"] = datetime.utcnow() + diff
        encoded = jwt.encode(messageDict, key, algorithm='HS256')
        return encoded

    def decodeJWT(self, token, key):
        try:
            decoded = jwt.decode(token, key, algorithms=['HS256'])
            return decoded
        except jwt.ExpiredSignatureError as e:
            logging.error(e)
            raise e




