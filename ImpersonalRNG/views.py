# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Request,Response
from datetime import  timedelta
import django.utils.timezone as t
import json
consignment = 3
TIMEOUT = 20 #20 сек

@csrf_exempt
def rest(request):
    resp = HttpResponse(status=404)
    if request.method == 'POST':
        if (request.body.decode("utf-8") != ''):
            received_json_data = json.loads(request.body.decode("utf-8-sig"))
            if(received_json_data['event']=='GetNewRequest'):
                QueryRequest = Request.objects.filter(isdead=False,isresponsed=False,datetime__gte=t.now()-timedelta(seconds=TIMEOUT+10))
                i=1
                datareq=[]
                isnext = False
                for Req in QueryRequest:
                    i+=1
                    method =Req.method.encode('utf-8')
                    datareq.append({'uid':Req.uid,'method':Req.method,'params':Req.params,
                                    'compress':Req.compress,'debug':Req.debug,'json':Req.json})
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
    return resp