from rest_framework.response import Response
from rest_framework import generics
from django.http import HttpResponse
from ins.scripts.IX import confirm
import json

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


class INS(generics.GenericAPIView):
  def post(self, req):
    if req.META['HTTP_CONEXT_KEY'] == "fiwjef-paxgox-9gydcY":
      status_code = 200
      data = json.loads(req.body)
      response = {
        "error":None,
        "message":None,
        "data":None
        }
      if data["type"].lower() == "m":
        response["data"] = data["data"]
        response["data"]["temperature"] = "-"
        response["data"]["power"] = "-"
        response["data"]["admin_status"] = "-"
        response["data"]["onu_id"] = "-"
        response["error"] = False
        response["message"] = "success, waiting for manual config"
        return Response(response, status=status_code)
      confirm(data["data"])
      return Response({"message":"response_data"}, status=status_code)
    else:
      return HttpResponse("Bad Request to server", status=400)
