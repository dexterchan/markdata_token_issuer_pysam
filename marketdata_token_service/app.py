import json

from datetime import datetime, timedelta
from service.JWTIssueService import JwtIssueService

jwtIssueService = JwtIssueService()
hours = 720
def lambda_handler(event, context):
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """
    expTime = datetime.utcnow() + timedelta(hours=hours)
    encodedToken = jwtIssueService.issueJWTToken(hours)

    encodedTokenStr = encodedToken.decode("utf-8")


    return {
        "statusCode": 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET',
            'Access-Control-Allow-Credentials': True
        },
        "body": json.dumps({
            "jwt": encodedTokenStr,
        }),
    }
#https://docs.aws.amazon.com/apigateway/latest/developerguide/how-to-cors.html
#https://www.serverless.com/framework/docs/providers/aws/events/apigateway/#lambda-proxy-integration
#https://alexharv074.github.io/2019/03/31/introduction-to-sam-part-iii-adding-a-proxy-endpoint-and-cors-configuration.html