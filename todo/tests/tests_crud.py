from django.test import TestCase
from rest_framework.test import APIClient

from ..models import Todo


# ---------------------------------------------------------
# ✅ Todo API CRUD 동작을 검증하는 테스트 클래스
# ---------------------------------------------------------
class TodoAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.base_url = "/todo/viewsets/view/"  # ViewSet 경로로 통일

        self.todo = Todo.objects.create(
            name="운동",
            description="스쿼트 50회",
            complete=False,
            exp=10,
        )

    # -----------------------------------------------------
    # 1️⃣ 목록 조회 테스트
    # -----------------------------------------------------
    def test_list(self):
        res = self.client.get(self.base_url)

        self.assertEqual(res.status_code, 200)

        # 페이지네이션 응답에서 실제 리스트 꺼내기
        data = res.json()["data"]
        self.assertIsInstance(data, list)

    # -----------------------------------------------------
    # 2️⃣ 생성 테스트
    # -----------------------------------------------------
    def test_create(self):
        payload = {
            "name": "공부",
            "description": "DRF",
            "complete": False,
            "exp": 5,
        }

        res = self.client.post(self.base_url, payload, format="json")

        self.assertEqual(res.status_code, 201)
        self.assertEqual(Todo.objects.count(), 2)

    # -----------------------------------------------------
    # 3️⃣ 상세 조회 테스트
    # -----------------------------------------------------
    def test_retrieve(self):
        res = self.client.get(f"{self.base_url}{self.todo.id}/")

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["name"], "운동")

    # -----------------------------------------------------
    # 4️⃣ 수정 테스트 (PATCH)
    # -----------------------------------------------------
    def test_update_patch(self):
        payload = {"name": "운동(수정)"}

        res = self.client.patch(
            f"{self.base_url}{self.todo.id}/", payload, format="json"
        )

        self.assertEqual(res.status_code, 200)

        self.todo.refresh_from_db()
        self.assertEqual(self.todo.name, "운동(수정)")

    # -----------------------------------------------------
    # 5️⃣ 삭제 테스트
    # -----------------------------------------------------
    def test_delete(self):
        res = self.client.delete(f"{self.base_url}{self.todo.id}/")

        self.assertEqual(res.status_code, 204)
        self.assertFalse(Todo.objects.filter(id=self.todo.id).exists())

    # -----------------------------------------------------
    # 6️⃣ 존재하지 않는 데이터 요청 시 404 테스트
    # -----------------------------------------------------
    def test_not_found_returns_404(self):
        res = self.client.get(f"{self.base_url}999999/")

        self.assertEqual(res.status_code, 404)
