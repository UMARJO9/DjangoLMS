from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Allow login using email instead of username."""

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom fields to token payload
        token['email'] = user.email
        token['is_admin'] = user.is_admin
        token['is_student'] = user.is_student
        return token

    def validate(self, attrs):
        # Authenticate using email
        credentials = {
            'email': attrs.get('email'),
            'password': attrs.get('password')
        }

        from django.contrib.auth import authenticate
        user = authenticate(**credentials)
        if user and user.is_active:
            data = super().validate(attrs)
            data['user'] = {
                'id': user.id,
                'email': user.email,
                'username': user.username,
                'is_admin': user.is_admin,
                'is_student': user.is_student,
            }
            return data
        else:
            raise self.fail('no_active_account')

