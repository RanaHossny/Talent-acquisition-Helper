import os
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status

class UploadPDFsView(APIView):
    parser_classes = [MultiPartParser]

    @csrf_exempt  
    @permission_classes([IsAuthenticated])  
    def post(self, request, *args, **kwargs):
        # Retrieve the uploaded file (ZIP file containing PDFs)
        file = request.FILES.get('file')
        
        if not file:
            return Response(
                {"success": False, "error": "No file uploaded."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Prepare the file to send it to the Flask API
        flask_api_url = "https://8001-01jhhtwya97h5wp60v4q27p9xy.cloudspaces.litng.ai/upload_pdfs" 
        files = {'file': (file.name, file, 'application/zip')}
        
        try:
            # Send the ZIP file to the Flask API
            response = requests.post(flask_api_url, files=files)

            if response.status_code == 200:
                return Response(
                    {"success": True, "message": "Files forwarded to Flask API successfully."},
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    {"success": False, "error": "Failed to forward files to Flask API."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        
        except requests.exceptions.RequestException as e:
            return Response(
                {"success": False, "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
