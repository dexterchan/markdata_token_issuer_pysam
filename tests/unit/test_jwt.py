import unittest
import logging
from crypto.jwt_crypto import JWT_Crypto
from datetime import timedelta, datetime


FORMAT = '%(asctime)-15s %(levelname)s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)



class MarketDataServiceSuite(unittest.TestCase):
    def testshouldencodeanddecodeproperly(self):
        crypto = JWT_Crypto()

        message = {}
        message["issuer"] = "abc"
        message["role"] = "user"
        key = "abcd"
        refExpDate = (datetime.utcnow() + timedelta(seconds=10)).timestamp()
        encodedJWT, expDate = crypto.generateJWT(key, message, timedelta(seconds=10))
        self.assertGreaterEqual(expDate, refExpDate)

        self.assertIsNotNone(encodedJWT)
        logging.info(encodedJWT)
        decodedJWT = crypto.decodeJWT(encodedJWT, key)
        logging.info(decodedJWT)

        expDateTime = datetime.fromtimestamp(decodedJWT["exp"])


        logging.debug ( expDateTime.strftime("%m/%d/%Y, %H:%M:%S"))

        self.assertEqual(decodedJWT["issuer"], message["issuer"])

    def testExceptionExpired(self):
        crypto = JWT_Crypto()

        message = {}
        message["issuer"] = "abc"
        message["role"] = "user"
        key = "abcd"
        refExpDate = (datetime.utcnow() + timedelta(seconds=10)).timestamp()
        encodedJWT, expDate = crypto.generateJWT(key, message, timedelta(seconds=-1))
        self.assertGreaterEqual(expDate, refExpDate)
        self.assertIsNotNone(encodedJWT)


        with self.assertRaises(Exception):
            crypto.decodeJWT(encodedJWT, key)

    def testExceptionInvalid(self):
        crypto = JWT_Crypto()

        message = {}
        message["issuer"] = "abc"
        message["role"] = "user"
        key = "abcd"
        refExpDate = (datetime.utcnow() + timedelta(seconds=10)).timestamp()
        encodedJWT, expDate = crypto.generateJWT(key, message, timedelta(seconds=10))
        self.assertGreaterEqual(expDate, refExpDate)
        self.assertIsNotNone(encodedJWT)
        key = "abcd2"

        with self.assertRaises(Exception):
            crypto.decodeJWT(encodedJWT, key)
