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
def guardar_ordenes(ordenes):
    with open(PATH_ORDENES, 'w') as file:
        json.dump(ordenes, file, indent=2)

# Function for http Requests
def ordenes(request):

    ordenes = cargar_ordenes()

    # Verificar si hay ordenes
    if len(ordenes) == 0:
        return JsonResponse({"mensaje": "No hay Ordenes"}, safe=False, status=404)

    if request.method == 'GET':
        respuesta = JsonResponse(ordenes, safe=False, status=200)
        return respuesta


    if request.method == 'POST':
        try:
            ordenes = cargar_ordenes()
            nueva_orden = json.loads(request.body.decode('utf-8'))
            if nueva_orden['id'] == 0:
                id = newIndex()
                nueva_orden['id'] = id

            ordenes.append(nueva_orden)
            guardar_ordenes(ordenes)

            return JsonResponse({"mensaje": "Orden Creada Correctamente"}, status=200)
        except:
            return JsonResponse({"mensaje" : "Hubo un error al agregar la Orden"}, safe=False, status=400)


    else:
        return JsonResponse({"mensaje":"Método No Permitido"}, status=400)

def newIndex():
    ordenes = cargar_ordenes()
    higher_index = 0

    for orden in ordenes:
        if orden['id'] > higher_index:
            higher_index = orden['id']

    return higher_index + 1

def detalles_ordenes(request, id):
    ordenes = cargar_ordenes()

    if request.method == 'GET':
        orden = next((o for o in ordenes if o['id'] == id), None)

        if orden is None:
            return JsonResponse({"mensaje" : "No se encontró la Orden"}, safe=False, status=404)

        return JsonResponse(orden, safe=False, status=200)


    elif request.method == 'PATCH':

        orden = next((o for o in ordenes if o['id'] == id), None)

        if orden is None:
            return JsonResponse({"mensaje" : "Orden No encontrada"}, safe=False, status=404)

        orden_actualizada = json.loads(request.body.decode('utf-8'))
        orden.update(orden_actualizada)
        guardar_ordenes(orden)
        return JsonResponse({"mensaje" : "Orden actualizada correctamente"}, safe=False, status=200)


    elif request.method == 'DELETE':

        orden = next((o for o in ordenes if o['id'] == id), None)

        if orden is None:
            return JsonResponse({"mensaje": "Orden no encontrada"}, safe=False, status=404)

        # If the product exists, then create a new array excluding the product of the {id}
        new_orden_list = [u for u in ordenes if u['id'] != id]
        guardar_ordenes(new_orden_list)
        return JsonResponse({"mensaje" : "Orden Eliminada Correctamente"}, safe=False, status=204)


