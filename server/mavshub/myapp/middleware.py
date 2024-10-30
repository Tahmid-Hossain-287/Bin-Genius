# import re

# class DistanceLoggingMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         # Extract the distance from the query parameters
#         distance = request.GET.get('distance')
#         if distance:
#             with open('data.txt', 'a') as log_file:  # Update this path
#                 log_file.write(f"{distance}\n")
        
#         response = self.get_response(request)
#         return response

import os

class DistanceLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Extract the distance from the query parameters
        distance = request.GET.get('distance')
        if distance:
            file_path = 'data.txt'  # Update this path if needed

            # Append the new distance value to the file
            with open(file_path, 'a') as log_file:
                log_file.write(f"{distance}\n")
            
            # Trim file to keep only the latest 50 lines
            with open(file_path, 'r') as log_file:
                lines = log_file.readlines()
            
            # Keep only the last 50 lines if there are more than 50
            if len(lines) > 50:
                with open(file_path, 'w') as log_file:
                    log_file.writelines(lines[-50:])
        
        response = self.get_response(request)
        return response