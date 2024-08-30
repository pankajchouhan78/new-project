from rest_framework import serializers
from django.core.exceptions import ValidationError
from user_services.models import Role, Organization, Address

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

# class SearchTaskSerializer(serializers.Serializer):
#     search = serializers.CharField(max_length=50)

#     def validate_search(self, value):
#         # Check if the Role exists
#         if not Role.objects.filter(role_name=value).exists():
#             raise serializers.ValidationError("Search task not found")
        
#         # Check if any UserProfile is associated with the Role
#         if not UserProfile.objects.filter(user_role=value).exists():
#             raise serializers.ValidationError("No user registered with the search task")
        
#         # Return the filtered queryset or value if needed
#         return value
