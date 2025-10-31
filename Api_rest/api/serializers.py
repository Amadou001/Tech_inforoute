from rest_framework import serializers
from harvesting.models import Dataset, Organization, Ressource, Tag


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = [
            'organization_id',
            'name',
            'title',
            'description',
            'image_url',
            'created_at',
        ]


class RessourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ressource
        fields = [
            'ressource_id',
            'name',
            'description',
            'format',
            'url',
            'url_type',
            'created_at',
            'updated_at',
        ]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = [
            'tag_id',
            'name',
        ]


class DatasetSerializer(serializers.ModelSerializer):
    organization = OrganizationSerializer(read_only=True)
    ressources = RessourceSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Dataset
        fields = [
            'id',
            'source',
            'source_id',
            'title',
            'description',
            'author_email',
            'organization',
            'ressources',
            'tags',
            'created_at',
            'updated_at',
        ]
