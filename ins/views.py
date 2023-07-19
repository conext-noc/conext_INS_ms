import os
import json
from rest_framework import generics
from rest_framework.response import Response
from django.http import HttpResponse
from dotenv import load_dotenv
from ins.scripts.IC import client_install

load_dotenv()


class INS(generics.GenericAPIView):
    def get(self, req):
        status_code = 200
        response_text = "ms_running"
        return HttpResponse(response_text, status=status_code)

    def post(self, req):
        if req.META["HTTP_CONEXT_KEY"] == os.environ["CONEXT_KEY"]:
            status_code = 200
            data = json.loads(req.body)
            response = {"error": None, "message": None, "data": None}
            if data["type"].lower() == "m":
                response["data"] = data["data"]
                response["error"] = False
                response["message"] = "success, waiting for manual config"
                return Response(response, status=status_code)
            result = client_install(data["data"], False)
            return Response(result, status=status_code)
        return HttpResponse("Bad Request to server", status=400)


class INSDashboard(generics.GenericAPIView):
    def get(self, req):
        status_code = 200
        response_text = "ms_running"
        return HttpResponse(response_text, status=status_code)

    def post(self, req):
        data = req.data

        if data["API_KEY"] == os.environ["API_KEY"]:
            result = client_install(data["data"], True)
            return Response(result, status=200)
        return HttpResponse("Bad Request to server", status=400)
