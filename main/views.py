from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import SponsorSerializer
from rest_framework.permissions import AllowAny

class SponsorApplicationAPIView(APIView):

    permission_classes = [AllowAny, ]

    def post(self, request):
        # Serializerga request ma'lumotlarini yuborish
        serializer = SponsorSerializer(data=request.data)

        # Agar serializer valid bo'lsa
        if serializer.is_valid():
            serializer.save()  # Ma'lumotlarni saqlash
            return Response({
                'success': True,
                'message': 'Application Successful.',
                'data': serializer.data  # Saqlangan ma'lumotlarni qaytarish
            }, status=status.HTTP_201_CREATED)

        # Agar serializer valid bo'lmasa
        return Response({
            'success': False,
            'message': 'Invalid data',
            'errors': serializer.errors  # Xatoliklarni qaytarish
        }, status=status.HTTP_400_BAD_REQUEST)
