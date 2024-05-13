from rest_framework import serializers
from user_app.models import Account

class AccountSerializers(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Account
        fields = ('id', 'first_name', 'last_name', 'username', 'email', 'phone_number', 'role', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = Account.objects.create_user(password=password, **validated_data)
        return user
