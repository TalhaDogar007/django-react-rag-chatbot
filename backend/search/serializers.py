from rest_framework import serializers
from .models import PDF

class PDFSerializer(serializers.ModelSerializer):
    class Meta:
        model = PDF
        fields = '__all__'