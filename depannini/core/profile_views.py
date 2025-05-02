# core/profile_views.py
from rest_framework import status, views, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model

from .serializers import UserSerializer, AssistantSerializer, UpdateLocationSerializer, AssistantProfileSerializer

User = get_user_model()


class UserProfileView(generics.RetrieveUpdateAPIView):
    """View for retrieving and updating user profile"""
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def retrieve(self, request, *args, **kwargs):
        """Override to customize response format"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'success': True,
            'user': serializer.data
        })

    def update(self, request, *args, **kwargs):
        """Override to customize response format"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response({
            'success': True,
            'message': 'Profile updated successfully',
            'user': serializer.data
        })


class AssistantProfileView(generics.RetrieveUpdateAPIView):
    """View for retrieving and updating assistant profile"""
    serializer_class = AssistantProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get_queryset(self):
        # Only allow assistants to access this view
        return User.objects.filter(user_type='assistant')

    def retrieve(self, request, *args, **kwargs):
        """Override to customize response format"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'success': True,
            'assistant': serializer.data
        })

    def update(self, request, *args, **kwargs):
        """Override to customize response format"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response({
            'success': True,
            'message': 'Profile updated successfully',
            'assistant': serializer.data
        })


class UpdateLocationView(views.APIView):
    """View for updating user's location"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = UpdateLocationSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            user.location = {
                'latitude': serializer.validated_data['latitude'],
                'longitude': serializer.validated_data['longitude']
            }
            user.save()

            return Response({
                'success': True,
                'message': 'Location updated successfully',
                'location': user.location
            }, status=status.HTTP_200_OK)

        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class AssistantStatusView(views.APIView):
    """View for toggling assistant active status"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.user_type != 'assistant':
            return Response({
                'success': False,
                'message': 'Only assistants can update status'
            }, status=status.HTTP_403_FORBIDDEN)

        status_value = request.data.get('is_active', False)
        request.user.is_active_assistant = status_value
        request.user.save()

        return Response({
            'success': True,
            'message': f"Status updated successfully to {'active' if status_value else 'inactive'}",
            'is_active': request.user.is_active_assistant
        }, status=status.HTTP_200_OK)


class AssistantListView(generics.ListAPIView):
    """View for listing all assistants"""
    serializer_class = AssistantSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filter by active assistants only
        queryset = User.objects.filter(
            user_type='assistant', is_active_assistant=True)

        # Apply filters if provided
        service_type = self.request.query_params.get('service_type', None)
        if service_type:
            queryset = queryset.filter(service_type=service_type)

        return queryset

    def list(self, request, *args, **kwargs):
        """Override to customize response format"""
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        return Response({
            'success': True,
            'assistants': serializer.data
        })
