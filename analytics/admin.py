from django.contrib import admin

from .models import AnalyticsReport


@admin.register(AnalyticsReport)
class AnalyticsReportAdmin(admin.ModelAdmin):
    list_display = ("report_name", "generated_at", "file_link")
    list_filter = ("generated_at",)
    search_fields = ("report_name",)
    readonly_fields = ("generated_at",)

    def file_link(self, obj):
        if obj.file:
            return f'<a href="{obj.file.url}" target="_blank">Download</a>'
        return "No file"

    file_link.allow_tags = True
    file_link.short_description = "Report File"
