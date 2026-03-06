from django.contrib.auth import authenticate, login, logout

# DRF APIView 사용
from rest_framework.views import APIView

# API 응답 객체
from rest_framework.response import Response

# HTTP 상태 코드
from rest_framework import status

# 모든 사용자 접근 허용
from rest_framework.permissions import AllowAny, IsAuthenticated

# 회원가입 데이터 검증 Serializer
from .serializers import SignupSerializer

from django.shortcuts import redirect


# 회원가입 API
class SignupAPIView(APIView):

    # 로그인하지 않은 사용자도 접근 가능
    permission_classes = [AllowAny]

    # POST 요청 처리
    def post(self, request):

        # 요청 데이터(request.data)를 Serializer에 전달
        serializer = SignupSerializer(data=request.data)

        # raise_exception=True → 검증 실패 시 자동으로 에러 응답 반환
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response({"detail": "회원가입 완료"}, status=status.HTTP_201_CREATED)


class SessionLoginAPIView(APIView):

    # 로그인하지 않은 사용자도 접근 가능
    permission_classes = [AllowAny]

    # POST 요청 처리
    def post(self, request):

        username = request.data.get("username", "")
        password = request.data.get("password", "")

        user = authenticate(request, username=username, password=password)

        if not user:
            return Response(
                {"detail": "아이디/비밀번호가 올바르지 않습니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        login(request, user)

        return Response({"detail": "로그인 성공"}, status=status.HTTP_200_OK)


class SessionLogoutAPIView(APIView):

    permission_classes = [IsAuthenticated]

    # GET 요청(주소창 입력/단순 링크) 처리
    def get(self, request):
        logout(request)
        return redirect("page-login")  # 로그인 페이지로 이동

    # POST 요청(API 호출) 처리
    def post(self, request):
        logout(request)
        return Response({"detail": "로그아웃"}, status=status.HTTP_200_OK)
