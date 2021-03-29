from django.contrib import admin
from apps.catalog.models import Category, Product, Attribute, AttributeValue, ProductAttributeValue
from mptt.admin import DraggableMPTTAdmin


@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    fieldsets = (
        (None, {
            'fields': ('active','title','slug','image','parent')
        }),
    )
    prepopulated_fields = {"slug": ("title",)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields':('active', 'id_1c','title', 'slug', 'category', 'image', 'description')
        }),
        ('Свойства товара',{
            'fields':('price', 'old_price', 'amount')
        }),
    )
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ('id_1c',)
    list_display = ('title', 'category', 'price', 'active')
    search_fields = ('title__startswith',)
    list_filter = ('active',)

@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    search_fields = ('title__startswith',)
    readonly_fields = ('id_1c',)


@admin.register(AttributeValue)
class AttributeValueAdmin(admin.ModelAdmin):
    search_fields = ('value__startswith','id_1c__icontains')
    # readonly_fields = ('id_1c',)

@admin.register(ProductAttributeValue)
class ProductAttributeValueAdmin(admin.ModelAdmin):
    search_fields = ('attribute_value__id_1c__icontains',)