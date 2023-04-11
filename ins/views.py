from rest_framework.response import Response
from rest_framework import generics
from django.http import HttpResponse

from sch.scripts.BC import clientFinder

class CHECK(generics.GenericAPIView):
  def get(self, req):
    content_type = req.META.get('HTTP_CONTENT_TYPE')
    status_code = None
    response_text = ""
    if req.META['HTTP_CONEXT_KEY'] == "fiwjef-paxgox-9gydcY":
      status_code = 200
      response_text = "ms_running"
    else:
      status_code = 400
      response_text = "Bad Request to server"
    return HttpResponse(response_text, status=status_code)


class SCH(generics.GenericAPIView):
  def get(self, req):
    if req.META['HTTP_CONEXT_KEY'] == "fiwjef-paxgox-9gydcY":
      status_code = 200
      contract = req.query_params.get('contract')
      olt = req.query_params.get('olt')
      data = {"contract":contract, "olt":olt}
      res = clientFinder(data)
      response_data = {"message": "OK", "data": res}
      return Response(response_data, status=status_code)
      return Response("client_contract", status=200)
    else:
      return HttpResponse("Bad Request to server", status=400)
