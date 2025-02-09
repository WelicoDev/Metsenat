from rest_framework import viewsets
from .models import Sponsor, University, Student, AllocatedAmount
from .serializers import SponsorSerializer, UniversitySerializer, StudentSerializer, AllocatedAmountSerializer

class SponsorViewSet(viewsets.ModelViewSet):
    queryset = Sponsor.objects.all()
    serializer_class = SponsorSerializer

class UniversityViewSet(viewsets.ModelViewSet):
    queryset = University.objects.all()
    serializer_class = UniversitySerializer

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class AllocatedAmountViewSet(viewsets.ModelViewSet):
    queryset = AllocatedAmount.objects.all()
    serializer_class = AllocatedAmountSerializer
