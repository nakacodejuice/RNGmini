# -*- coding: utf-8 -*-
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Request,Response
import datetime
from datetime import timedelta
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
import json
consignment = 3

@csrf_exempt
def rest(request):
    resp = HttpResponse(status=404)
    if request.method == 'POST':
        if (request.body.decode("utf-8") != ''):
            received_json_data = json.loads(request.body.decode("utf-8-sig"))
            if(received_json_data['event']=='GetNewRequest'):
                QueryRequest = Request.objects.filter(isdead=False,isresponsed=False)
                i=1
                datareq=[]
                isnext = False
                print (QueryRequest)
                for Req in QueryRequest:
                    i+=1
                    method =Req.method.encode('utf-8')
                    print (method)
                    datareq.append({'uid':Req.uid,'method':method.decode('unicode-escape'),'params':Req.params,
                                    'compress':Req.compress,'debug':Req.debug,'json':Req.json})
                    if(i==consignment):
                        isnext = True

                        break
                data = {'data': datareq,'isnext':isnext}
                resp =JsonResponse(data)
            elif (received_json_data['event']=='SetResponse'):
                data =received_json_data['data']
                p = Response(uid=data['uid'], method=data['method'], resp=data['resp'])
                p.save()
    return resp