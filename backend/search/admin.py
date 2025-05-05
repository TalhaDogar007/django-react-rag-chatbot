from django.contrib import admin
from .models import PDF

@admin.register(PDF)
class PDFAdmin(admin.ModelAdmin):
    list_display = ('file', 'uploaded_at')  # Display file name and upload time in the admin panel
