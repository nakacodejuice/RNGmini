# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Request,Response
from datetime import  timedelta
import django.utils.timezone as t
from django.core.exceptions import ObjectDoesNotExist
import json
import time
import uuid
consignment = 3
TIMEOUT = 200 #20 сек

@csrf_exempt
def rest(request):
    resp = HttpResponse(status=404)
    if request.method == 'POST':
        if (request.body.decode("utf-8") != ''):
            received_json_data = json.loads(request.body.decode("utf-8-sig"))
            if(received_json_data['event']=='GetNewRequest'):
                QueryRequest = Request.objects.filter(isdead=False,isresponsed=False,inprogress = False,datetime__gte=t.now()-timedelta(miliseconds=TIMEOUT+10))
                i=1
                datareq=[]
                isnext = False
                for Req in QueryRequest:
                    i+=1
                    method =Req.method.encode('utf-8')
                    datareq.append({'uid':Req.uid,'method':Req.method,'params':Req.params,
                                    'compress':Req.compress,'debug':Req.debug,'json':Req.json})
                    Req.inprogress = True;
                    Req.save()
                    if(i==consignment):
                        isnext = True
                        break
                data = {'data': datareq,'isnext':isnext}
                #resp =JsonResponse(data,enc,False)
                resp = HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json")
            elif (received_json_data['event']=='SetResponse'):
                data =received_json_data['data']
                Response.objects.update_or_create(uid=data['uid'], method=data['method'], resp=data['resp'])
                r= Request.objects.filter(uid=data['uid'])
                for Req in r:
                    Req.isresponsed = True
                    Req.save()
                resp = HttpResponse(status=200)
            elif received_json_data['event']=='SetNewRequest':
                data = received_json_data['data']
                uid = str(uuid.uuid4())
                p = Request(uid=uid, method=data['id'], params=data['params'],compress = False, debug = False, json = True)
                p.save()
                i = 0
                resp = '!!!!!!';
                while (i < TIMEOUT):
                    try:
                        QueryResponse = Response.objects.get(uid=uid)
                        resp = QueryResponse.resp
                        break
                    except ObjectDoesNotExist:
                        print("doesn't ready!!!")
                    i += 1;
                    time.sleep(0.1)
                if (resp == '!!!!!!'):
                    response = "Timeout"
                    p.isdead = True
                else:
                    p.isresponsed = True
                p.save()
    return resp