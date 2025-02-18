from django.http import Http404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import datetime
from django.db.models import Sum
from django.db.models import Q
from .serializers import SponsorSerializer, StudentSerializer, AllocatedAmountSerializer
from main.models import Sponsor, Student, AllocatedAmount
from shared.custom_paga import CustomPagination
from drf_yasg.utils import swagger_auto_schema
# Sponsor Views

class SponsorListAPIView(APIView):
    permission_classes = [IsAuthenticated,]

    def get(self, request):
        search = self.request.query_params.get('search', '')
        status_filter = self.request.query_params.get('status', None)
        filters = Q(full_name__icontains=search)

        if status_filter:
            filters &= Q(status=status_filter)

        sponsors = Sponsor.objects.filter(filters).order_by('created_at')  # yoki boshqa biror maydon
        paginator = CustomPagination()
        page_obj = paginator.paginate_queryset(sponsors, request)
        serializer = SponsorSerializer(page_obj, many=True)
        return paginator.get_paginated_response(serializer.data)


class SponsorDetailUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated,]

    @staticmethod
    def get_sponsor(id):
        try:
            sponsor = Sponsor.objects.get(id=id)
        except Sponsor.DoesNotExist:
            raise Http404("Sponsor with this id does not exist.")
        return sponsor

    def get(self, request, id):
        sponsor = self.get_sponsor(id)
        serializer = SponsorSerializer(sponsor, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=SponsorSerializer)
    def put(self, request, id):
        sponsor = self.get_sponsor(id)
        serializer = SponsorSerializer(instance=sponsor, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=SponsorSerializer)
    def patch(self, request, id):
        sponsor = self.get_sponsor(id)
        serializer = SponsorSerializer(instance=sponsor, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, id):
        sponsor = self.get_sponsor(id)
        sponsor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Student Views

class StudentListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated,]

    def get(self, request):
        search = self.request.query_params.get('search', '')
        degree = self.request.query_params.get('degree', None)
        university = self.request.query_params.get('university', None)
        filters = Q(full_name__icontains=search)

        if degree:
            filters &= Q(degree_type=degree)

        if university:
            filters &= Q(university__name__icontains=university)

        students = Student.objects.filter(filters)
        paginator = CustomPagination()
        page_obj = paginator.paginate_queryset(students, request)
        serializer = StudentSerializer(page_obj, many=True)
        return paginator.get_paginated_response(serializer.data)

    @swagger_auto_schema(request_body=StudentSerializer)
    def post(self, request):
        serializer = StudentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class StudentDetailUpdateDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get_student(id):
        try:
            student = Student.objects.get(id=id)
        except Student.DoesNotExist:
            raise Http404("Student with this id does not exist.")
        return student

    def get(self, request, id):
        student = self.get_student(id)
        serializer = StudentSerializer(instance=student)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=StudentSerializer)
    def put(self, request, id):
        student = self.get_student(id)
        serializer = StudentSerializer(instance=student, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=StudentSerializer)
    def patch(self, request, id):
        student = self.get_student(id)
        serializer = StudentSerializer(instance=student, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, id):
        student = self.get_student(id)
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




class AllocatedAmountListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get_student(student_id):
        try:
            return Student.objects.get(id=student_id)
        except Student.DoesNotExist:
            raise Http404('Student with this id does not exist.')

    @staticmethod
    def get_sponsor(sponsor_id):
        try:
            sponsor = Sponsor.objects.get(id=sponsor_id)
        except Sponsor.DoesNotExist:
            raise Http404('Sponsor with this id does not exist.')
        return sponsor

    def get(self, request, student_id):
        student = self.get_student(student_id)
        allocated_amounts = AllocatedAmount.objects.filter(student=student)
        serializer = AllocatedAmountSerializer(allocated_amounts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=AllocatedAmountSerializer)
    def post(self, request, student_id):
        student = self.get_student(student_id)
        serializer = AllocatedAmountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Assign the student from the URL to the serializer's data
        serializer.save(student=student)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AllocatedAmountDetailUpdateDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get_allocated_amount(student_id, sponsor_id):
        try:
            return AllocatedAmount.objects.get(student_id=student_id, sponsor_id=sponsor_id)
        except AllocatedAmount.DoesNotExist:
            raise Http404("Allocated amount with this student and sponsor id does not exist.")

    def get(self, request, student_id, sponsor_id):
        allocated_amount = self.get_allocated_amount(student_id, sponsor_id)
        serializer = AllocatedAmountSerializer(instance=allocated_amount)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=AllocatedAmountSerializer)
    def put(self, request, student_id, sponsor_id):
        allocated_amount = self.get_allocated_amount(student_id, sponsor_id)
        serializer = AllocatedAmountSerializer(instance=allocated_amount, data=request.data)
        serializer.is_valid(raise_exception=True)
        # Here you can modify or add custom validation if needed
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=AllocatedAmountSerializer)
    def patch(self, request, student_id, sponsor_id):
        allocated_amount = self.get_allocated_amount(student_id, sponsor_id)
        serializer = AllocatedAmountSerializer(instance=allocated_amount, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        # Apply changes if needed
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, student_id, sponsor_id):
        allocated_amount = self.get_allocated_amount(student_id, sponsor_id)
        allocated_amount.delete()
        return Response({"message": "Allocated amount deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


class AllocatedAmountSummaryAPIView(APIView):
    permission_classes = [IsAuthenticated,]

    def get(self, request):
        total_allocated_amount = AllocatedAmount.objects.all().aggregate(total=Sum('money'))['total'] or 0
        total_sponsor_balance = Sponsor.objects.all().aggregate(total_balance=Sum('amount'))['total_balance'] or 0
        total_students = Student.objects.count()

        remaining_balance = total_sponsor_balance - total_allocated_amount

        return Response(
            {
                'total_allocated_amount': total_allocated_amount,
                'total_sponsor_balance': total_sponsor_balance,
                'remaining_balance': remaining_balance,
                'total_students': total_students,
            }
        )