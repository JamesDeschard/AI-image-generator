import ast
import base64
import json
from io import BytesIO

import environ
import replicate
import requests
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from PIL import Image

env = environ.Env()
REPLICATE_API_TOKEN = env("REPLICATE_API_TOKEN")

class Home(View):
    template_name = 'home.html'
    
    def get(self, request, prompt_params=None):
        if prompt_params:
            return render(request, self.template_name, {'prompt_params': True})
        return render(request, self.template_name)
    
    def post(self, request):
        if request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest":
            # Retrieve the user request
            prompt_params = ast.literal_eval(request.body.decode('utf-8'))
            prompt_params = prompt_params.get('prompt_params')
            
            # Retrieve the image from Replicate
            rep = replicate.Client(api_token=REPLICATE_API_TOKEN)
            rep = rep.models.get("stability-ai/stable-diffusion")
            output = rep.predict(prompt=prompt_params)[0]
            image = Image.open(requests.get(output, stream=True).raw)
            
            buffered = BytesIO()
            image.save(buffered, format="JPEG")
            image = base64.b64encode(buffered.getvalue())
            image = json.dumps(image.decode('utf-8'))
            return JsonResponse({'image': image}, status=200)
        
        return JsonResponse({'error': 'Invalid request'}, status=400)