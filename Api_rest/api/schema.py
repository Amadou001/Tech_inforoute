import graphene
from graphene_django import DjangoObjectType
from django.db.models import Q
from harvesting.models import Dataset, Organization, Ressource, Tag




class OrganizationType(DjangoObjectType):
    class Meta:
        model = Organization
        fields = "__all__"


class RessourceType(DjangoObjectType):
    class Meta:
        model = Ressource
        fields = "__all__"


class TagType(DjangoObjectType):
    class Meta:
        model = Tag
        fields = "__all__"


class DatasetType(DjangoObjectType):
    class Meta:
        model = Dataset
        fields = "__all__"



class Query(graphene.ObjectType):
    # List of all datasets, with search and ordering
    all_datasets = graphene.List(
        DatasetType,
        search=graphene.String(),
        ordering=graphene.String()
    )

    # Retrieve a single dataset by ID
    dataset = graphene.Field(DatasetType, id=graphene.Int(required=True))

    # ---- Resolver for all datasets ----
    def resolve_all_datasets(root, info, search=None, ordering=None):
        qs = Dataset.objects.select_related('organization').prefetch_related('ressources', 'tags')

        # Apply search filter if provided
        if search is not None and search.strip() != "":
            qs = qs.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(organization__name__icontains=search) |
                Q(organization__title__icontains=search)
            )

        # Apply ordering only if valid
        if ordering:
            qs = qs.order_by(ordering)
        else:
            qs = qs.order_by('-updated_at')

        return qs

    # ---- Resolver for single dataset ----
    def resolve_dataset(root, info, id):
        try:
            return Dataset.objects.select_related('organization').get(pk=id)
        except Dataset.DoesNotExist:
            return None



schema = graphene.Schema(query=Query)

