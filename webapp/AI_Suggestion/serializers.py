from rest_framework import serializers
from .models import AISummary


class AISummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = AISummary
        fields = [
            'id',
            'user',
            'summary_text',
            'raw_ai_response',
            'date_created'
        ]
        read_only_fields = ['id', 'date_created']
