# Django 기본 User 모델 사용
from django.contrib.auth.models import User

# DRF Serializer 사용
from rest_framework import serializers


# 회원가입 요청 데이터를 처리하기 위한 Serializer
class SignupSerializer(serializers.Serializer):

    # 사용자 아이디
    username = serializers.CharField(max_length=150)

    # 비밀번호 (write_only=True → 응답 JSON에는 포함되지 않음)
    password = serializers.CharField(write_only=True, min_length=4)

    password2 = serializers.CharField(write_only=True, min_length=4)

    def validate_username(self, value):

        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("이미 사용중인 username 입니다.")

        return value

    def validate(self, attrs):

        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "비밀번호가 일치하지 않습니다."}
            )

        return attrs

    # 사용자 생성
    # serializer.save() 호출 시 실행됨
    def create(self, validated_data):

        # Django User 생성
        # create_user()는 내부적으로 비밀번호를 hash 처리함
        user = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
        )

        return user
