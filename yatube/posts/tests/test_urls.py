from django.urls import reverse
from django.test import TestCase, Client
from django.contrib.auth import get_user_model

from ..models import Post, Group

User = get_user_model()


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.post = Post.objects.create(
            text='Тестовый текст',
            author=cls.user,
        )
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание',
        )

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username='HasNoName')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_response_code(self):
        slug = PostURLTests.group.slug
        user = PostURLTests.user
        post_id = PostURLTests.post.id
        url_names = {
            'index': '/',
            'group_posts': f'/group/{slug}/',
            'profile': f'/profile/{user}/',
            'post_by_id': f'/posts/{post_id}/',
        }
        for adress in url_names.values():
            with self.subTest(adress=adress):
                response = self.guest_client.get(adress)
                self.assertEqual(response.status_code, 200)

    def test_response_code_authorized(self):
        post_id = PostURLTests.post.id
        url_names = {
            'create': '/create/',
            'post_edit': f'/posts/{post_id}/edit/',
        }
        for adress in url_names.values():
            with self.subTest(adress=adress):
                response = self.authorized_client.get(adress)
                self.assertEqual(response.status_code, 200)

    def test_redirect_response_code(self):
        post_id = PostURLTests.post.id
        url_names = {
            'create': '/create/',
            'post_edit': f'/posts/{post_id}/edit/',
        }
        for adress in url_names.values():
            with self.subTest(adress=adress):
                response = self.guest_client.get(adress)
                self.assertEqual(response.status_code, 302)

    def test_unexisting_page(self):
        response = self.guest_client.get('/unexisting_page/')
        self.assertEqual(response.status_code, 404)

    def test_create_url_redirect_anonymous_on_admin_login(self):
        login_url = reverse('users:login')
        post_create_url = reverse('posts:post_create')
        target_url = f'{login_url}?next={post_create_url}'
        response = self.guest_client.get('/create/', follow=True)
        self.assertRedirects(response, target_url)

    def test_post_edit_url_redirect_anonymous_on_admin_login(self):
        post_id = PostURLTests.post.id
        login_url = reverse('posts:post_edit', args=(post_id,))
        post_create_url = reverse('users:login')
        target_url = f'{post_create_url}?next={login_url}'
        response = self.guest_client.get(
            f'/posts/{post_id}/edit/',
            follow=True
        )
        self.assertRedirects(response, target_url)

    def test_urls_uses_correct_template(self):
        slug = PostURLTests.group.slug
        post_id = PostURLTests.post.id
        user = PostURLTests.user
        templates_url_names = {
            '/': 'posts/index.html',
            f'/group/{slug}/': 'posts/group_list.html',
            f'/profile/{user}/': 'posts/profile.html',
            f'/posts/{post_id}/': 'posts/post_detail.html',
            f'/posts/{post_id}/edit/': 'posts/create_post.html',
            '/create/': 'posts/create_post.html',
        }
        for adress, template in templates_url_names.items():
            with self.subTest(address=adress):
                response = self.authorized_client.get(adress)
                self.assertTemplateUsed(response, template)
