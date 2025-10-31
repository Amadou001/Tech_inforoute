from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from harvesting.models import Dataset
from .serializers import DatasetSerializer


@api_view(['GET'])
def dataset_list(request):
    """
    Return all datasets with optional search and ordering.
    """
    query = request.GET.get('search', '')
    ordering = request.GET.get('ordering', '-updated_at')

    datasets = Dataset.objects.all()

    # 🔍 Search filter (title, author, organization name/title)
    if query:
        datasets = datasets.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(Author_email__icontains=query) |
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


@api_view(['GET'])
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
