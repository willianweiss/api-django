from rest_framework.generics import ListAPIView, RetrieveAPIView

from .models import Quizz
from .serializers import QuizzSerializer


class QuizzList(ListAPIView):
    queryset = Quizz.objects.all()
    serializer_class = QuizzSerializer


class QuizzDetail(RetrieveAPIView):
    queryset = Quizz.objects.all()
    serializer_class = QuizzSerializer
