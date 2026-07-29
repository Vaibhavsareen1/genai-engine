import asyncio
from fastapi import Request, HTTPException, status
from library.constants import JWT_ALGORITHM, JWT_SECRET_KEY
from jwt import (decode, InvalidKeyError, InvalidTokenError, InvalidAudienceError,
                 ExpiredSignatureError, InvalidAlgorithmError, InvalidSignatureError, DecodeError)


async def authorize_user(request: Request) -> Request:
    """
    Async function that performs JWT authorization of a user's request as part of the request-response cycle.

    The function performs verification and helps extract user profile from the request

    :param request: Request object representing user's request.

    :returns: Updated Request with user profile if the request is valid and authorized 
    """

    try:
        auth_header = request.headers.get("Authorization", None)
        if auth_header:
            bearer, auth_header = auth_header.split(" ")
            if bearer == 'Bearer':
                authorization_config = {
                                            'jwt': auth_header,
                                            'key': JWT_SECRET_KEY,
                                            'audience': ['ADMIN', 'USER'],
                                            'algorithms': [JWT_ALGORITHM]
                                        }
                payload = await asyncio.to_thread(decode, **authorization_config)

                # Setup user profile object
                user_profile = {
                                'user_id': payload['user_id'],
                                'user_name': payload['user_name']
                                }

                # Add user profile object to request's state
                request.state.user_profile = user_profile

                return request
            else:
                raise InvalidTokenError
        else:
            raise InvalidTokenError

    except InvalidAudienceError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Permission denied")

    except (InvalidKeyError, InvalidTokenError, ExpiredSignatureError, InvalidAlgorithmError, InvalidSignatureError, DecodeError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid authorization token")


async def authorize_admin(request: Request) -> Request:
    """
    Async function that performs JWT authorization of an admin's request as part of the request-response cycle.

    The function performs verification and helps extract admin profile from the request

    :param request: Request object representing admin's request.

    :returns: Updated Request with admin's profile if the request is valid and authorized 
    """

    try:
        auth_header = request.headers.get("Authorization", None)
        if auth_header:
            bearer, auth_header = auth_header.split(' ')
            if bearer == 'Bearer':
                authorization_config = {
                                            'jwt': auth_header,
                                            'key': JWT_SECRET_KEY,
                                            'audience': ['ADMIN'],
                                            'algorithms': [JWT_ALGORITHM]
                                        }
                payload = await asyncio.to_thread(decode, **authorization_config)

                # Setup user profile object
                user_profile = {
                                'user_id': payload['user_id'],
                                'user_name': payload['user_name']
                                }

                # Add user profile object to request's state
                request.state.user_profile = user_profile

                return request
            else:
                raise InvalidTokenError
        else:
            raise InvalidTokenError

    except InvalidAudienceError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Permission denied")

    except (InvalidKeyError, InvalidTokenError, ExpiredSignatureError, InvalidAlgorithmError, InvalidSignatureError, DecodeError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid authorization token")
