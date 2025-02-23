from django.contrib import admin

from .models import Order, Transaction


class TransactionInline(admin.TabularInline):
    model = Transaction
    extra = 1
    readonly_fields = ("executed_at",)
    fields = ("executed_price", "quantity", "executed_at")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "product",
        "order_type",
        "quantity",
        "price",
        "status",
        "created_at",
    )
    list_filter = ("order_type", "status", "created_at")
    search_fields = ("id", "user__username", "product__name")
    readonly_fields = ("created_at",)
    autocomplete_fields = ("user", "product")
    inlines = [TransactionInline]


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "executed_price", "quantity", "executed_at")
    list_filter = ("executed_at",)
    search_fields = ("order__id", "order__user__username", "order__product__name")
    readonly_fields = ("executed_at",)
    autocomplete_fields = ("order",)
