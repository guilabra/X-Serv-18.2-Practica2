from django.shortcuts import render
from django.http import HttpResponse
from models import Urlpairs
from django.views.decorators.csrf import csrf_exempt

def showRedirect(request, num):

    numeroDic = int(num)
    try:
        newurl = Urlpairs.objects.get(id=numeroDic)
        respuesta = ("<html><head><meta http-equiv='refresh' content='0; " +
            "url=" + newurl.name +"'></head></html>")
        return HttpResponse(respuesta, status = 302)

    except Urlpairs.DoesNotExist:
        respuesta = ("Recurso no disponible")
        return HttpResponse(respuesta, status = 404)

# Create your views here.
@csrf_exempt
def showFormulario(request):

    if request.method == "GET":

        formulario = """<form action="" method="post" >
            <label for="url">Introduce una url:</label>
            <input type="text" name="value" />
            <input type="submit" value="Enviar" />
            </form></body></html>"""

        pages = Urlpairs.objects.all()
    	for newurl in pages:
    		formulario += newurl.name + " : " + str(newurl.id) + "<br>"

        return HttpResponse(formulario)

    elif request.method == "POST":

        body = request.POST["value"]
        if body == "":
            return HttpResponse("No se ha introducido una url", status = 404)

        else:

            if body.find("http") == -1:
                body = "http://" + body

            try:
                newurl = Urlpairs.objects.get(name=body)
                respuesta = "La url ya esta cogida"
                return HttpResponse(respuesta)

            except Urlpairs.DoesNotExist:

                newPage = Urlpairs(name=body)
                newPage.save()
                respuesta = ("<html><body><a href='" + newPage.name + "'>" + str(newPage.id) + "</a>" +
                        "   " + "<a href='" + newPage.name + "'>" + newPage.name + "</a></body></html>")
                return HttpResponse(respuesta)
