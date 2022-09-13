from django import forms
from django.urls import reverse
from django.core.paginator import Page
from django.test import Client, TestCase

from django.contrib.auth import get_user_model

from ..models import Group, Post
from yatube.settings import POST_PER_PAGE

User = get_user_model()


class PostPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='KtoTo')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Текстовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый текст',
            id=333,
        )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_pages_names = {
            reverse('posts:index'): 'posts/index.html',
            reverse('posts:group_posts', kwargs={'slug': self.group.slug}):
            'posts/group_list.html',
            reverse('posts:profile', kwargs={'username': self.user.username}):
            'posts/profile.html',
            reverse('posts:post_detail', args={self.post.id}):
            'posts/post_detail.html',
            reverse('posts:post_create'): 'posts/create_post.html',
            reverse('posts:post_edit', args={self.post.id}):
            'posts/create_post.html',
        }

        for reverse_name, template in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_index_show_correct_context(self):
        """Шаблон post_create сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('posts:post_create'))
        form_fields = {
            'group': forms.fields.ChoiceField,
            'text': forms.fields.CharField,
        }

        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_fields = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_fields, expected)


POSTS_FOR_PAGINATOR_TESTING = 13


class TestingPaginator(TestCase):
    """Проверка паджинатора и наличия класса Page в контексте шаблона"""
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='testslug',
        )

    def setUp(self):
        self.user = User.objects.create_user(username='Somebody')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.posts_for_test = []
        for i in range(1, POSTS_FOR_PAGINATOR_TESTING):
            self.posts_for_test.append(Post(
                author=self.user,
                text=f'Test{i}',
                group=TestingPaginator.group))
        Post.objects.bulk_create(self.posts_for_test)

    def test_first_page_contains_ten_records_and_class_page(self):
        """Проверка работы паджинатора и использования
        класса Page в контексте"""
        group = TestingPaginator.group
        user = self.user
        posts_on_second_page = len(self.posts_for_test) - POST_PER_PAGE
        pages = [
            reverse('posts:index'),
            reverse('posts:group_posts', kwargs={'slug': f'{group.slug}'}),
            reverse('posts:profile', kwargs={'username': f'{user.username}'}),
        ]
        for page in pages:
            with self.subTest(page=page):
                response1 = self.client.get(page)
                response2 = self.client.get(page + '?page=2')
                context = response1.context['page_obj']
                self.assertEqual(
                    len(response1.context['page_obj']),
                    POST_PER_PAGE,
                    f'На странице {page} показывается {POST_PER_PAGE} постов'
                )
                self.assertEqual(
                    len(response2.context['page_obj']),
                    posts_on_second_page,
                    f'На второй странице {page} '
                    f'должно быть {posts_on_second_page}'
                )
                self.assertIsInstance(
                    context,
                    Page,
                    f'На станице {page} нет класса Page в контексте'
                )
