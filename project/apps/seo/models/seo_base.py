from django.db import models
from ckeditor.fields import RichTextField

class SeoBase(models.Model):
    seo_title = models.CharField(
        null=True,
        blank=True,
        max_length=200,
    )
    seo_image = models.ImageField(
        null=True,
        blank=True,
    )
    seo_description = RichTextField(
        null=True,
        blank=True,

    )
    seo_text = RichTextField(
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True