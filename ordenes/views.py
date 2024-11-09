from django.template.context_processors import request
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.conf import settings
import os
import json

PATH_ORDENES = os.path.join(settings.BASE_DIR, 'db\ordenes.json')

# Función para cargar los contenidos de órdenes.json
def cargar_ordenes():
    if not os.path.exists(PATH_ORDENES):
        return []

    with open(PATH_ORDENES, 'r') as file:
        return json.load(file)

# Función para sobreescribir el archivo de usuarios.json
def guardar_ordenes(usuarios):
    with open(PATH_ORDENES, 'w') as file:
        json.dump(usuarios, file, indent=2)

# Function for http Requests
def ordenes(request):

    ordenes = cargar_ordenes()

    # Verificar si hay usuarios
    if len(ordenes) == 0:
        return JsonResponse({"mensaje": "No hay productos"}, safe=False, status=404)

    if request.method == 'GET':
        respuesta = JsonResponse(ordenes, safe=False, status=200)
        return respuesta


    if request.method == 'POST':
        return JsonResponse({"mensaje":"No hay ordenes"}, status=400)

    else:
        return JsonResponse({"mensaje":"Método No Permitido"}, status=400)