from django.urls import path
from .views import AISuggestionView

urlpatterns = [
    path("summary/<int:user_id>/", AISuggestionView.as_view(), name="ai-summary"),
]
