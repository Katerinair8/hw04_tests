from django.urls import reverse
from django.test import Client, TestCase
from django.contrib.auth import get_user_model

from ..forms import PostForm
from ..models import Post, Group

User = get_user_model()


class PostFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            text='Тестовый текст',
            author=cls.user,
            group=cls.group
        )
        cls.form = PostForm()

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_create_post(self):
        """Валидная форма создает новый пост."""
        post_count = Post.objects.count()
        form_data = {
            'text': 'Тестовый текст',
            'author': self.user
        }

        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )

        self.assertRedirects(
            response,
            reverse('posts:profile', args=(PostFormTests.post.author,))
        )
        self.assertEqual(Post.objects.count(), post_count + 1)
        self.assertTrue(
            Post.objects.filter(
                text='Тестовый текст',
                author=self.user,
                group=self.post.group,
            ).exists()
        )

    def test_post_edit(self):
        """Валидная форма редактирует пост."""
        post_count = Post.objects.count()
        form_data = {
            'text': 'Тестовый текст второй',
            'author': self.user,
            'group': self.group.id,
        }

        response = self.authorized_client.post(
            reverse('posts:post_edit', args=(PostFormTests.post.id,)),
            data=form_data,
            follow=True
        )
        redirect_url = reverse(
            'posts:post_detail',
            args=(PostFormTests.post.id,)
        )

        self.assertRedirects(response, redirect_url)
        self.assertEqual(Post.objects.count(), post_count)
        self.assertTrue(
            Post.objects.filter(
                author=self.user,
                text='Тестовый текст второй',
                group=self.group,
            ).exists()
        )
