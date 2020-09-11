from crypto.jwt_crypto import JWT_Crypto
import boto3
import os
from Exception.JsonIssueException import ParameterNotFound, ThrottlingException
from datetime import timedelta


class JwtIssueService:
    def __init__(self):
        self.JWTKEYID_VAR="JWTKEYID"
        if self.JWTKEYID_VAR in os.environ:
            self.JWTKEYID = os.environ[self.JWTKEYID_VAR]
        else:
            raise Exception("Environment JWTKEYID is empty")
        self.signKey = self.getEncryptedParameter()
        self.crypto = JWT_Crypto()



    def getEncryptedParameter(self):
        self.ssmClient = boto3.client('ssm')
        try:
            response = self.ssmClient.get_parameter(
                Name = self.JWTKEYID,
                WithDecryption=True
            )
        except self.ssmClient.exceptions.ParameterNotFound as ex:
            raise ParameterNotFound(str(ex))
        except self.ssmClient.exceptions.ThrottlingException as t:
            raise ThrottlingException(str(t))
        return response["Parameter"]["Value"]

    def issueJWTToken(self, validHours):
        message = {}
        message["issuer"] = "Market Data Streaming service Lambda"
        encodedJWT, expDate = self.crypto.generateJWT(self.signKey, message, timedelta(seconds=validHours))

        return encodedJWT, expDate


