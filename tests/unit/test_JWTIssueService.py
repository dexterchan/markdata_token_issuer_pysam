import unittest
import logging
import os
from service.JWTIssueService import JwtIssueService
from Exception.JsonIssueException import ParameterNotFound
from crypto.jwt_crypto import JWT_Crypto
from datetime import datetime, timedelta

FORMAT = '%(asctime)-15s %(levelname)s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)

crypto = JWT_Crypto()

class TestJWTIssueService(unittest.TestCase):


    def testAWSParameterStoreOK(self):
        os.environ["JWTKEYID"] = "/mktsvc/dev/JWT_SECRET"
        jwtIssueService = JwtIssueService()
        response = jwtIssueService.getEncryptedParameter()
        self.assertEqual("abcd", response)

    def testAWSParameterFail(self):
        os.environ["JWTKEYID"] = "/mktsvc/dev/JWT_SECRET2"
        with self.assertRaises(ParameterNotFound):
            jwtIssueService = JwtIssueService()
            jwtIssueService.getEncryptedParameter()

    def testJsonIssue(self):
        os.environ["JWTKEYID"] = "/mktsvc/dev/JWT_SECRET"
        hours = 720
        try:
            expTime = datetime.utcnow() +  timedelta(hours=hours)
            jwtIssueService = JwtIssueService()
            encodedToken = jwtIssueService.issueJWTToken(hours)
            print(encodedToken)
            secret = jwtIssueService.getEncryptedParameter();
            decodedJson = crypto.decodeJWT(encodedToken,secret )
            logging.debug((decodedJson))
            self.assertGreaterEqual(decodedJson["exp"], expTime.timestamp() )
        except ParameterNotFound as p:
            logging.error(p)
            raise p

