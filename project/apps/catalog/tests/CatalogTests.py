from django.test import TestCase


class CatalogTest(TestCase):
    def test_catalog_page_status(self):
        catalog_response = self.client.get('/catalog/')
        self.assertEqual(catalog_response.status_code, 200)
