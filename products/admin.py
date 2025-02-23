from django.contrib import admin

from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "product_count", "description")
    search_fields = ("name",)

    def product_count(self, obj):
        return obj.products.count()

    product_count.short_description = "Number of Products"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "created_at", "image_preview")
    list_filter = ("category", "created_at")
    search_fields = ("name", "category__name")
    readonly_fields = ("created_at", "image_preview")
    autocomplete_fields = ("category",)

    def image_preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" width="50" height="50" style="object-fit: cover;" />'
        return "No Image"

    image_preview.allow_tags = True
    image_preview.short_description = "Image Preview"
