from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import serializers
from .models import Author
import re


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['first_name', 'last_name', 'birth_date', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        instance = self.Meta.model(**validated_data)
        try:
            validate_password(password)
        except ValidationError as error:
            raise serializers.ValidationError(error.messages)
        instance.set_password(password)
        instance.save()
        return instance

    def validate(self, data):
        birth_date = re.match(r'(0[1-9]|[1-2][0-9]|31)(\D{1})(0[1-9]|1[0-2])(\D{1})'
                              r'(19[0-9][0-9]|20[0-1][0-9]|202[0-2])', data['birth_date'])
        if birth_date is None:
            raise serializers.ValidationError('Unsupported date format. Use dd.mm.yyyy')
        return data
