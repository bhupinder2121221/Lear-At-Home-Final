from rest_framework.authentication import TokenAuthentication


class myTokenAuthentication(TokenAuthentication):
    keyword='SecretToken'
    