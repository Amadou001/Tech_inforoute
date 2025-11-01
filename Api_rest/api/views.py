from django.db.models import Q
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from harvesting.models import Dataset
from .serializers import DatasetSerializer
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi



search_param = openapi.Parameter(
    'search', openapi.IN_QUERY, description="Search term (title, author, organization)", type=openapi.TYPE_STRING, required=False
)
ordering_param = openapi.Parameter(
    'ordering', openapi.IN_QUERY, description="Field to order by, e.g., '-updated_at' or 'title'", type=openapi.TYPE_STRING, required=False
)

@swagger_auto_schema(
    method='get',
    manual_parameters=[search_param, ordering_param],
    responses={200: DatasetSerializer(many=True), 401: 'Unauthorized'}
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dataset_list(request):
    """
    Return all datasets with optional search and ordering.
    """
    query = request.GET.get('search', '')
    ordering = request.GET.get('ordering', '-updated_at')

    datasets = Dataset.objects.all()

    # 🔍 Search filter (title, author, organization name/title)
    # example: ?search=water
    if query:
        datasets = datasets.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(author_email__icontains=query) |
            Q(organization__name__icontains=query) |
            Q(organization__title__icontains=query)
        )

    # ↕️ Safe ordering
    try:
        datasets = datasets.order_by(ordering)
    except Exception:
        datasets = datasets.order_by('-updated_at')

    serializer = DatasetSerializer(datasets, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)




@swagger_auto_schema(
    method='get',
    responses={200: DatasetSerializer, 404: 'Dataset not found', 401: 'Unauthorized'}
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dataset_detail(request, pk):
    """
    Return the details of one dataset by ID.
    """
    try:
        dataset = Dataset.objects.get(pk=pk)
    except Dataset.DoesNotExist:
        return Response({"error": "Dataset not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = DatasetSerializer(dataset)
    return Response(serializer.data, status=status.HTTP_200_OK)
