from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase
from rest_framework.response import Response
from rest_framework.test import APIClient, APIRequestFactory, force_authenticate
from rest_framework.views import APIView

from .permissions import IsAdminRole
from .roles import ADMIN, EMPLOYEE, get_role
from .views import INVALID_LOGIN_MESSAGE

PASSWORD = 'test-wachtwoord-123'

LOGIN_URL = '/api/auth/login/'
LOGOUT_URL = '/api/auth/logout/'
ME_URL = '/api/auth/me/'
CSRF_URL = '/api/auth/csrf/'


def create_user(username, role=None, **extra):
    user = get_user_model().objects.create_user(username, password=PASSWORD, **extra)
    if role:
        user.groups.add(Group.objects.get(name=role))
    return user


class AuthEndpointTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.employee = create_user('medewerker', EMPLOYEE)
        self.admin = create_user('admin', ADMIN)

    def login(self, username, password=PASSWORD):
        return self.client.post(LOGIN_URL, {'username': username, 'password': password}, format='json')

    def test_login_returns_user_with_role(self):
        response = self.login('medewerker')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['username'], 'medewerker')
        self.assertEqual(response.data['role'], 'employee')

    def test_login_with_wrong_password_gives_generic_message(self):
        response = self.login('medewerker', 'fout')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['detail'], INVALID_LOGIN_MESSAGE)

    def test_login_with_unknown_user_gives_same_message(self):
        response = self.login('bestaat-niet')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['detail'], INVALID_LOGIN_MESSAGE)

    def test_inactive_user_cannot_login(self):
        create_user('oud-account', EMPLOYEE, is_active=False)

        response = self.login('oud-account')

        self.assertEqual(response.status_code, 400)

    def test_me_requires_login(self):
        response = self.client.get(ME_URL)

        self.assertEqual(response.status_code, 403)

    def test_me_returns_admin_role(self):
        self.login('admin')

        response = self.client.get(ME_URL)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['role'], 'admin')

    def test_logout_ends_session(self):
        self.login('medewerker')

        logout_response = self.client.post(LOGOUT_URL)
        me_response = self.client.get(ME_URL)

        self.assertEqual(logout_response.status_code, 204)
        self.assertEqual(me_response.status_code, 403)


class CsrfTests(TestCase):

    def setUp(self):
        self.client = APIClient(enforce_csrf_checks=True)
        create_user('medewerker', EMPLOYEE)

    def test_login_without_csrf_token_is_refused(self):
        response = self.client.post(LOGIN_URL, {'username': 'medewerker', 'password': PASSWORD}, format='json')

        self.assertEqual(response.status_code, 403)

    def test_login_with_csrf_token_succeeds(self):
        self.client.get(CSRF_URL)
        token = self.client.cookies['csrftoken'].value

        response = self.client.post(
            LOGIN_URL,
            {'username': 'medewerker', 'password': PASSWORD},
            format='json',
            HTTP_X_CSRFTOKEN=token,
        )

        self.assertEqual(response.status_code, 200)


class AdminOnlyView(APIView):
    permission_classes = [IsAdminRole]

    def get(self, request):
        return Response({'ok': True})


class RoleTests(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()

    def call_admin_view(self, user):
        request = self.factory.get('/admin-only/')
        force_authenticate(request, user=user)
        return AdminOnlyView.as_view()(request)

    def test_employee_is_refused_on_admin_action(self):
        response = self.call_admin_view(create_user('medewerker', EMPLOYEE))

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data['detail'], IsAdminRole.message)

    def test_admin_is_allowed_on_admin_action(self):
        response = self.call_admin_view(create_user('admin', ADMIN))

        self.assertEqual(response.status_code, 200)

    def test_user_without_group_has_no_role(self):
        self.assertIsNone(get_role(create_user('zonder-rol')))

    def test_admin_wins_when_user_has_both_roles(self):
        user = create_user('beide', EMPLOYEE)
        user.groups.add(Group.objects.get(name=ADMIN))

        self.assertEqual(get_role(user), 'admin')
