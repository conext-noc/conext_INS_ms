from django.http import HttpResponse
from dotenv import load_dotenv
from ins.scripts.IX import confirm
import json
from rest_framework.response import Response
from rest_framework import generics
import os
load_dotenv()

class CHECK(generics.GenericAPIView):
  def get(self, req):
    content_type = req.META.get('HTTP_CONTENT_TYPE')
    status_code = None
    response_text = ""
    if req.META['HTTP_CONEXT_KEY'] == os.environ["CONEXT_KEY"]:
      status_code = 200
      response_text = "ms_running"
    else:
      status_code = 400
      response_text = "Bad Request to server"
    return HttpResponse(response_text, status=status_code)


class INS(generics.GenericAPIView):
  def post(self, req):
    if req.META['HTTP_CONEXT_KEY'] == os.environ["CONEXT_KEY"]:
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
      result = confirm(data["data"])
      return Response(result, status=status_code)
    else:
      return HttpResponse("Bad Request to server", status=400)
