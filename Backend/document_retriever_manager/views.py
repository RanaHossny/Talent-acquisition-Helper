# import os
# import zipfile
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.parsers import MultiPartParser
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.decorators import permission_classes
# from django.views.decorators.csrf import csrf_exempt
# from rest_framework import status

# class UploadPDFsView(APIView):
#     parser_classes = [MultiPartParser]

#     @csrf_exempt  # Apply csrf_exempt only to the post method
#     @permission_classes([IsAuthenticated])  # Apply permission_classes only to the post method
#     def post(self, request, *args, **kwargs):
#         uploaded_zip_file = request.FILES.get('file')  # Retrieve the uploaded zip file
        
#         # Ensure the directory exists
#         upload_dir = os.path.join(os.getcwd(), "uploaded_pdfs")
#         if not os.path.exists(upload_dir):
#             os.makedirs(upload_dir)

#         # Extract the zip file
#         try:
#             with zipfile.ZipFile(uploaded_zip_file, 'r') as zip_ref:
#                 zip_ref.extractall(upload_dir)
#                 extracted_files = zip_ref.namelist()  # List of extracted files
#         except zipfile.BadZipFile:
#             return Response({"success": False, "error": "Invalid zip file"}, status=status.HTTP_400_BAD_REQUEST)

#         # Return the list of extracted files
#         return Response(
#             {"success": True, "extracted_files": extracted_files},
#             status=status.HTTP_201_CREATED
#         )

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

    @csrf_exempt  # Apply csrf_exempt only to the post method
    @permission_classes([IsAuthenticated])  # Apply permission_classes only to the post method
    def post(self, request, *args, **kwargs):
        # Retrieve the uploaded file (ZIP file containing PDFs)
        file = request.FILES.get('file')
        
        if not file:
            return Response(
                {"success": False, "error": "No file uploaded."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Prepare the file to send it to the Flask API
        flask_api_url = "https://8001-01jhd73nrtd9bf4m8n8d9ctmj5.cloudspaces.litng.ai/upload_pdfs"  # Replace with your Flask API endpoint
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
