from django.http import HttpResponse
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from spyne.error import ResourceNotFoundError, ResourceAlreadyExistsError
from spyne.server.django import DjangoApplication
from spyne.model.primitive import Unicode, Integer,String, Boolean
import time
import uuid
from spyne.service import Service
from spyne.protocol.soap import Soap11
from spyne.application import Application
from spyne.decorator import rpc
from spyne.util.django import DjangoComplexModel, DjangoService
from ImpersonalRNG.models import Request, Response

from SoapLikeRNG.models import FieldContainer

TIMEOUT = 20 #20 сек

class Container(DjangoComplexModel):
    class Attributes(DjangoComplexModel.Attributes):
        django_model = FieldContainer
        django_exclude = ['excluded_field']


class DataExchange(Service):
    @rpc(String, String, Boolean,Boolean,Boolean, _returns=String)
    def ВыполнитьАлгоритмИПолучитьРезультат(ctx, Идентификатор, ПараметрыАлгоритма, СжиматьРезультат, РежимОтладки, JSON):
        uid = str(uuid.uuid4())
        p = Request(uid=uid, method=Идентификатор, params = ПараметрыАлгоритма ,
                    compress=СжиматьРезультат, debug=РежимОтладки, json=JSON)
        p.save()
        i=0
        response = '';
        while (i<TIMEOUT):
            try:
                QueryResponse = Response.objects.get(uid=uid)
                response = QueryResponse[0]['resp']
                break
            except ObjectDoesNotExist:
                print ("doesn't ready!!!")
            i+=1;
            time.sleep(1)
        if(response==''):
            response = "Timeout"
            p.isdead = True
        else:
            p.isresponsed = True
        p.save()
        return response

class ContainerService(Service):
    @rpc(Integer, _returns=Container)
    def get_container(ctx, pk):
        try:
            return FieldContainer.objects.get(pk=pk)
        except FieldContainer.DoesNotExist:
            raise ResourceNotFoundError('Container')

    @rpc(Container, _returns=Container)
    def create_container(ctx, container):
        try:
            return FieldContainer.objects.create(**container.as_dict())
        except IntegrityError:
            raise ResourceAlreadyExistsError('Container')

class ExceptionHandlingService(DjangoService):

    """Service for testing exception handling."""

    @rpc(_returns=Container)
    def raise_does_not_exist(ctx):
        return FieldContainer.objects.get(pk=-1)

    @rpc(_returns=Container)
    def raise_validation_error(ctx):
        raise ValidationError('Is not valid.')


app = Application([DataExchange, ContainerService,
                   ExceptionHandlingService],
    'http://www.dataexchange.org',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11(),
)
