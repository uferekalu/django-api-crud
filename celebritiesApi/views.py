from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status

from .models import Celebs
from .serializers import CelebsSerializer
from rest_framework.decorators import api_view

# Create your views here.


@api_view(['GET', 'POST', 'DELETE'])
def celebrities_list(request):
    if request.method == 'GET':
        celebrities = Celebs.objects.all()

        name = request.GET.get('name', None)
        if name is not None:
            celebrities = celebrities.filter(name__icontains=name)

        celebrities_serializer = CelebsSerializer(celebrities, many=True)
        # 'safe=False' for objects serialization
        return JsonResponse(celebrities_serializer.data, safe=False)

    elif request.method == 'POST':
        celebrities_data = JSONParser().parse(request)
        celebrities_serializer = CelebsSerializer(data=celebrities_data)
        if celebrities_serializer.is_valid():
            celebrities_serializer.save()
            return JsonResponse(celebrities_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(celebrities_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        count = Celebs.objects.all().delete()
        return JsonResponse({'message': '{} Celebrities were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT', 'DELETE'])
def celebrity_detail(request, id):
    # find celeb by id (celeb_id)
    try:
        celebrity = Celebs.objects.get(id=id)

        if request.method == 'GET':
            celebrity_serializer = CelebsSerializer(celebrity)
            return JsonResponse(celebrity_serializer.data)

        elif request.method == 'PUT':
            celebrity_data = JSONParser().parse(request)
            celebrity_serializer = CelebsSerializer(
                celebrity, data=celebrity_data)
            if celebrity_serializer.is_valid():
                celebrity_serializer.save()
                return JsonResponse(celebrity_serializer.data)
            return JsonResponse(celebrity_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            celebrity.delete()
            return JsonResponse({'message': 'Celebrity was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
    except Celebs.DoesNotExist:
        return JsonResponse({'message': 'The celebrity does not exist'}, status=status.HTTP_404_NOT_FOUND)
