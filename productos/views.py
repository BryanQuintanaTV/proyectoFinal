import json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import os

PATH_PRODUCTOS = os.path.join(settings.BASE_DIR, 'db\productos.json')

# Función para cargar los contenidos de órdenes.json
def cargar_productos():
    if not os.path.exists(PATH_PRODUCTOS):
        return []

    with open(PATH_PRODUCTOS, 'r') as file:
        return json.load(file)

# Función para sobreescribir el archivo de usuarios.json
def guardar_productos(productos):
    with open(PATH_PRODUCTOS, 'w') as file:
        json.dump(productos, file, indent=2)

# Create your views here.
def productos(request):

    productos = cargar_productos()

    # Verificar si hay usuarios
    if len(productos) == 0:
        return JsonResponse({"mensaje" : "No hay productos"}, safe=False, status=404)

    if request.method == 'GET':
        respuesta = JsonResponse(productos, safe=False, status=200)
        return respuesta

    elif request.method == 'POST':
        try:
            nuevo_producto = json.loads(request.body.decode('utf-8'))
            productos.append(nuevo_producto)
            guardar_productos(nuevo_producto)
            return JsonResponse({"mensaje": "Usuario Creado Correctamente"}, status=200)
        except:
            return JsonResponse({"mensaje" : "Hubo un error al agregar el producto"}, safe=False, status=400)
