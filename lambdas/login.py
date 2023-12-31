"""Log in a user in a cognito user pool and start a session"""
import os
import boto3

def lambda_handler(event, _):
    """create cognito client and try to log in the user"""
    client = boto3.client('cognito-idp')
    try:
        user = client.initiate_auth(
            ClientId= os.environ['COGNITO_CLIENT_ID'],
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': event["arguments"]["email"],
                'PASSWORD': event["arguments"]["password"]
            }
        )
    #respond to reset password challenge
    except client.exceptions.NotAuthorizedException as exc:
        print("Invalid credentials")
        raise PermissionError("Invalid credentials") from exc
    except client.exceptions.UserNotConfirmedException as exc:
        print("User not confirmed")
        raise PermissionError("User not confirmed") from exc
    except client.exceptions.UserNotFoundException as exc:
        print("User not found")
        raise LookupError("User not found") from exc

    #return the user's access and refresh tokens, as well as their cognito name and trello id
    return {
        "access_token": user["AuthenticationResult"]["AccessToken"]
    }
