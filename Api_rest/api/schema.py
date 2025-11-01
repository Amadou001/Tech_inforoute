import graphene
from graphene_django import DjangoObjectType
from django.db.models import Q
from harvesting.models import Dataset, Organization, Ressource, Tag
from graphql_jwt.decorators import login_required


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
    all_datasets = graphene.List(DatasetType, search=graphene.String(), ordering=graphene.String())
    dataset = graphene.Field(DatasetType, id=graphene.Int(required=True))

    # Require login for this resolver
    @login_required
    def resolve_all_datasets(root, info, search=None, ordering=None):
        qs = Dataset.objects.select_related('organization').prefetch_related('ressources', 'tags')
        if search:
            qs = qs.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(organization__name__icontains=search) |
                Q(organization__title__icontains=search)
            )
        if ordering:
            qs = qs.order_by(ordering)
        else:
            qs = qs.order_by('-updated_at')
        return qs

    @login_required
    def resolve_dataset(root, info, id):
        try:
            return Dataset.objects.select_related('organization').get(pk=id)
        except Dataset.DoesNotExist:
            return None


# Add authentication mutations
import graphql_jwt

class Mutation(graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
