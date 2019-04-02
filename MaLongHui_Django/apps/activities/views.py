from .models import Activity
from . import serializers

# Create your views here.
from rest_framework.generics import ListAPIView, RetrieveAPIView


class ActivityListView(ListAPIView):
    queryset = Activity.objects.all().order_by('-start_time')
    serializer_class = serializers.ActivityListSerializer


class ActivityDetailView(RetrieveAPIView):
    queryset = Activity.objects.all()
    serializer_class = serializers.ActivityDetailSerializer
