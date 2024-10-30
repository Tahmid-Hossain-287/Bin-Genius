from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from myapp.models import Snippet, TrashBinLevel
from myapp.serializers import SnippetSerializer
# Create your views here.

@api_view(['GET', 'POST'])
def snippet_list(request, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def snippet_detail(request, pk, format=None):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# @api_view(['GET', 'POST'])
# def distance_view(request, format=None):
#     distance = request.GET.get('distance')

#     if distance is not None:
#         distance_value = int(distance)

#         latest_reading = TrashBinLevel.objects.order_by('-timestamp').first()
            
#         trash_level = TrashBinLevel(distance=distance_value)
#         trash_level.save()

#         if distance_value < 20:
#             print("Alert: Trash bin is nearly full!")
#             return JsonResponse({"status": "success", "distance": distance_value})

#         excess_readings = TrashBinLevel.objects.order_by('-timestamp')[10:]  # Get all but the 10 latest
#         excess_readings.delete()

#     else:
#         return JsonResponse({"status": "error", "message": "No distance provided"})

def distance_view(request, format=None):
    # Path to the text file where distance readings will be stored
    file_path = "distance_readings.txt"
    
    # Check if the 'distance' parameter is present
    distance = request.GET.get('distance')

    if distance is not None:
        distance_value = int(distance)

        # Write the new reading to the file
        with open(file_path, "a") as file:
            file.write(f"{distance_value}\n")

        # Limit the file to the latest 50 readings
        with open(file_path, "r") as file:
            lines = file.readlines()
        
        # Keep only the last 50 lines
        if len(lines) > 50:
            with open(file_path, "w") as file:
                file.writelines(lines[-50:])

        # Optional alert if the distance is below a threshold
        if distance_value < 20:
            print("Alert: Trash bin is nearly full!")

        return JsonResponse({"status": "success", "distance": distance_value})
    
    else:
        return JsonResponse({"status": "error", "message": "No distance provided"})
