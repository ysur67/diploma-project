from django.test import TestCase
from apps.catalog.models import Category
from django.db import IntegrityError


class CategoryTest(TestCase):
    def setUp(self):
        # id was set as charfield, so it doesn't matter which string is given
        self.parent_category = Category.objects.create(id_1c='s')
        self.parent_category.title = 'Инструменты'
        self.parent_category.active = True
        self.parent_category.set_slug()
        self.parent_category.save()

        self.child_category = Category.objects.create(id_1c='a')
        self.child_category.title = 'Ножницы'
        self.child_category.active = True
        self.child_category.set_slug()
        self.child_category.parent = self.parent_category
        self.child_category.save()

    def test_parent_category_is_parent(self):
        self.assertEqual(self.child_category.parent, self.parent_category)

    def test_category_empty_name(self):
        category = Category.objects.create(id_1c='b')
        category.title = ''
        category.save()
        self.assertEqual(category, Category.objects.get(slug=''))

    def test_not_empty_title(self):
        with self.assertRaises(IntegrityError):
            Category.objects.create(id_1c='d')
            Category.objects.create(id_1c='e')

    def test_category_page_status(self):
        parent_category_response = self.client.get(
            f'/catalog/{self.parent_category.slug}/')

        child_category_response = self.client.get(
            f'/catalog/{self.child_category.slug}/')

        self.assertEqual(parent_category_response.status_code, 200)
        self.assertEqual(child_category_response.status_code, 200)

    def test_not_unique_slug_raises_error(self):
        with self.assertRaises(IntegrityError):
            Category.objects.create(id_1c='f', title='slug', slug='тайтл')
            Category.objects.create(id_1c='g', title='slug', slug='тайтл')

    def test_set_unique_slug_generates_unique_slug(self):
        category1 = Category.objects.create(
            id_1c='h', title='slug', slug='slug1')

        category2 = Category.objects.create(
            id_1c='g', title='slug', slug='slug2')

        category1.set_unique_slug()
        self.assertNotEqual(category1, category2)
