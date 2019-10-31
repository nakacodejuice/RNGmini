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
TIMEOUT = 90000 

@csrf_exempt
def rest(request):
    resp = HttpResponse(status=404)
    if request.method == 'POST':
        if (request.body.decode("utf-8") != ''):
            received_json_data = json.loads(request.body.decode("utf-8-sig"))
            if(received_json_data['event']=='GetNewRequest'):
                QueryRequest = Request.objects.filter(isdead=False,isresponsed=False,inprogress = False,datetime__gte=t.now()-timedelta(milliseconds=TIMEOUT+100))
                #QueryRequest = Request.objects.filter(isdead=False,isresponsed=False,inprogress = False)
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
            elif (received_json_data['event']=='GetDeadRequest'):
                QueryRequest = Request.objects.filter(isdead=True,deadrequested=False,datetime__gte=t.now()-timedelta(seconds=5*60*60))
                datareq =[]
                for req in QueryRequest:
                    datareq.append({'datetime':req.datetime.strftime("%Y-%m-%d %H:%M:%S"),'method':req.method,'uid':req.uid})
                    r = Request.objects.get(uid=req.uid)
                    r.deadrequested=True
                    r.save()
                resp = HttpResponse(json.dumps(datareq, ensure_ascii=False), content_type="application/json")
            elif received_json_data['event']=='SetNewRequest':
                data = received_json_data['data']
                uid = str(uuid.uuid4())
                p = Request(uid=uid, method=data['id'], params=data['params'],compress = False, debug = False, json = True)
                p.save()
                i = 0
                response = '!!!!!!';
                while (i < TIMEOUT):
                    try:
                        QueryResponse = Response.objects.get(uid=uid)
                        response = QueryResponse.resp
                        break
                    except ObjectDoesNotExist:
                        print("doesn't ready!!!")
                    i += 1;
                    time.sleep(0.1)
                if (response == '!!!!!!'):
                    response = "Timeout"
                    p.isdead = True
                else:
                    p.isresponsed = True
                p.save()
                resp = HttpResponse(response, content_type="application/json")
    return resp
