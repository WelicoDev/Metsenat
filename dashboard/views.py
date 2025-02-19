from django.db.models import Sum, Q
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, ListCreateAPIView, GenericAPIView, \
    get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import SponsorSerializer, StudentSerializer, AllocatedAmountSerializer, AllocatedAmountSummarySerializer
from main.models import Sponsor, Student, AllocatedAmount
from shared.custom_paga import CustomPagination


# Sponsor Views
class SponsorListAPIView(ListAPIView):
    queryset = Sponsor.objects.all().order_by('created_at')
    serializer_class = SponsorSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        search = self.request.query_params.get('search', '')
        status_filter = self.request.query_params.get('status', None)
        filters = Q(full_name__icontains=search)
        if status_filter:
            filters &= Q(status=status_filter)
        return Sponsor.objects.filter(filters)


class SponsorDetailUpdateAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Sponsor.objects.all()
    serializer_class = SponsorSerializer
    permission_classes = [IsAuthenticated]


# Student Views
class StudentListCreateAPIView(ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        search = self.request.query_params.get('search', '')
        degree = self.request.query_params.get('degree', None)
        university = self.request.query_params.get('university', None)
        filters = Q(full_name__icontains=search)
        if degree:
            filters &= Q(degree_type=degree)
        if university:
            filters &= Q(university__name__icontains=university)
        return Student.objects.filter(filters)


class StudentDetailUpdateDeleteAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]


# Allocated Amount Views
class AllocatedAmountListCreateAPIView(ListCreateAPIView):
    serializer_class = AllocatedAmountSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        student_id = self.kwargs.get('student_id')
        return AllocatedAmount.objects.filter(student_id=student_id)

    def perform_create(self, serializer):
        student_id = self.kwargs.get('student_id')
        student = get_object_or_404(Student, id=student_id)

        sponsor_id = self.request.data.get('sponsor_id')
        sponsor = get_object_or_404(Sponsor, id=sponsor_id)


        if sponsor.payment_status != 'Tasdiqlangan':
            raise ValidationError("The money sent by the sponsor has not been confirmed. Money cannot be allocated.")

        serializer.save(student=student, sponsor=sponsor)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return response


class AllocatedAmountDetailUpdateDeleteAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = AllocatedAmountSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        student_id = self.kwargs.get('student_id')
        sponsor_id = self.kwargs.get('sponsor_id')
        return get_object_or_404(AllocatedAmount, student_id=student_id, sponsor_id=sponsor_id)


class AllocatedAmountSummaryAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AllocatedAmountSummarySerializer

    def get(self, request):
        total_allocated_amount = AllocatedAmount.objects.aggregate(total=Sum('money'))['total'] or 0
        total_sponsor_balance = Sponsor.objects.aggregate(total_balance=Sum('amount'))['total_balance'] or 0
        total_students = Student.objects.count()
        remaining_balance = total_sponsor_balance - total_allocated_amount

        # View Statistic
        data = {
            'total_allocated_amount': total_allocated_amount,
            'total_sponsor_balance': total_sponsor_balance,
            'remaining_balance': remaining_balance,
            'total_students': total_students,
        }

        return Response(data)

