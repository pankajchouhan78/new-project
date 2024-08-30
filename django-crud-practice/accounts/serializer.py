from rest_framework import serializers

from relationship_app.models import Cources


class CourcesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cources
        fields = "__all__"

    def validate_course_name(self, value):
        if Cources.objects.filter(course_name=value).exists():
            raise serializers.ValidationError(
                f"A course with name '{value}' already exists."
            )
        return value
