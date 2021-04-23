from django.http import HttpResponse, Http404
from django.views.generic.base import TemplateView
# import collections
# import datetime
# import json
# import traceback
# import jdatetime
# from django.shortcuts import redirect, get_object_or_404, render
# from rest_framework.decorators import api_view
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import viewsets, status
# from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *
from django.core import serializers
# from api.tasks import refresh_sms_token
# from django.forms.models import model_to_dict
from .models import *
# from django.core import serializers
import logging
# import firebase_admin
# from firebase_admin import credentials, messaging
# from json import JSONEncoder
# from rest_framework.authtoken.models import *
from rest_framework import mixins
from rest_framework import generics


class HomePageView(TemplateView):

    template_name = "index.html"



logger = logging.getLogger(__name__)




class MusicitemsList(APIView):
    """
    List all musicitem, create a new musicitem.
    """

    def get(self, request, format=None):
        musicitem = Musicitems.objects.all()
        serializer = MusicitemsSerializer(musicitem, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        _name = request.data["name"]
        try:
            obj = Musicitems.objects.get(name=_name)
        except Musicitems.DoesNotExist:
            obj = Musicitems.objects.create(name=_name)
        obj_price = []
        obj_link = []
        i = 0
        for k, v in request.data.items():
            if k == 'name':
                obj.name = v
            elif k == 'your_price':
                obj.your_price = v
            elif k == 'is_active':
                obj.is_active = v
            elif k == 'description':
                obj.description = v
            elif k == 'image':
                obj.image = v
            obj.save()
        for k, v in request.data.items():
            if k == 'links':
                _links = request.data.get('links')
                for _link in _links:
                    obj_link.append(Links.objects.create(musicitem=obj))
                    for k, v in _link.items():
                        if k == 'url':
                            obj_link[i].url = v
                        obj_link[i].save()
                    for k, v in _link.items():
                        if k == 'prices':
                            _prices = _link["prices"]
                            if _prices:
                                _prices = _link["prices"]
                                for _price in _prices:
                                    obj_price.append(Prices.objects.create(link=obj_link[i], **_price))
                    i += 1
        leads_as_json = serializers.serialize('json', [obj,])
        leads_as_json1 = serializers.serialize('json', obj_link)
        leads_as_json2 = serializers.serialize('json', obj_price)
        leads_as_json3 =leads_as_json+leads_as_json1+leads_as_json2
        return HttpResponse(leads_as_json3, content_type='json')

class MusicitemsDetail(APIView):
    """
    Retrieve, update or delete a musicitem instance.
    """
    def get_object(self, pk):
        try:
            return Musicitems.objects.get(pk=pk)
        except Musicitems.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        musicitem = self.get_object(pk)
        serializer = MusicitemsSerializer(musicitem)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        musicitem = self.get_object(pk)
        serializer = MusicitemsSerializer(musicitem, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        musicitem = self.get_object(pk)
        musicitem.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)





class LinksList(APIView):
    """
    List all musicitem, create a new musicitem.
    """

    def get(self, request, format=None):
        _link = Links.objects.all()
        serializer = LinksSerializer(_link, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        _url = request.data["url"]
        try:
            obj = Links.objects.get(url=_url)
        except :
            obj = Links.objects.create(url=_url)

        if request.data.get('musicitem'):
            _musicitems = request.data.get('musicitem')
            for _musicitem in _musicitems:
                obj.musicitem = Musicitems.objects.create(**_musicitem)
        obj.save
        leads_as_json = serializers.serialize('json', [obj,])
        return HttpResponse(leads_as_json, content_type='json')


        # serializer = LinksSerializer(data=request.data)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LinksDetail(APIView):
    """
    Retrieve, update or delete a musicitem instance.
    """
    def get_object(self, pk):
        try:
            return Links.objects.get(pk=pk)
        except Links.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        _link = self.get_object(pk)
        serializer = LinksSerializer(_link)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        _link = self.get_object(pk)
        serializer = LinksSerializer(_link, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        _link = self.get_object(pk)
        _link.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class PricesList(APIView):
    """
    List all musicitem, create a new musicitem.
    """
    def get(self, request, format=None):
        _price = Prices.objects.all()
        serializer = PricesSerializer(_price, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = PricesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PricesDetail(APIView):
    """
    Retrieve, update or delete a musicitem instance.
    """
    def get_object(self, pk):
        try:
            return Prices.objects.get(pk=pk)
        except Prices.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        _price = self.get_object(pk)
        serializer = PricesSerializer(_price)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        _price = self.get_object(pk)
        serializer = PricesSerializer(_price, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        _price = self.get_object(pk)
        _price.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)









#
# # @api_view(['POST'])
# class MusicitemsViewSet(viewsets.ModelViewSet):
#     permission_classes = (AllowAny,)
#     queryset = Musicitems.objects.all().order_by("id")
#     serializer_class = MusicitemsSerializer
#
#     def list(self, request, *args, **kwargs):
#         queryset = self.filter_queryset(self.get_queryset())
#         queryset = queryset.filter(name=self.request.id)
#         page = self.paginate_queryset(queryset)
#         if page is not None:
#             serializer = MusicitemsSerializer(page, many=True)
#             return self.get_paginated_response(serializer.data)
#         serializer = MusicitemsSerializer(queryset, many=True)
#         return Response(serializer.data)
#
#     def create(self, request, *args, **kwargs):
#         # _id = request.id
#         _id = 5
#         try:
#             obj = Musicitems.objects.get(id=_id)
#         except Musicitems.DoesNotExist:
#             obj = Musicitems.objects.create(id=_id)
#
#         for k, v in request.data.items():
#             if k == 'name':
#                 obj.name = v
#             elif k == 'your_price':
#                 obj.your_price = v
#             elif k == 'is_active':
#                 obj.is_active = v
#             obj.save()
#         leads_as_json = serializers.serialize('json', [obj, ])
#         return HttpResponse(leads_as_json, content_type='json')
        # return JsonResponse([obj.first_name,obj.last_name,obj.is_legal], safe=False)
        # return JsonResponse ({'status':'ok',},encoder=JSONEncoder

# class PeopleViewSet(viewsets.ModelViewSet):
#     permission_classes = (IsAuthenticated,)
#     queryset = Peoples.objects.all()
#     serializer_class = PeopleSerializer
#
#     def list(self, request, *args, **kwargs):
#         queryset = self.filter_queryset(self.get_queryset())
#         queryset = queryset.filter(meeting_owner=self.request.user)
#         page = self.paginate_queryset(queryset)
#         if page is not None:
#             serializer = PeopleSerializer(page, many=True)
#             return self.get_paginated_response(serializer.data)
#
#         serializer = PeopleSerializer(queryset, many=True)
#         return Response(serializer.data)
#
#     def create(self, request, *args, **kwargs):
#         _id = request.user.id
#         try:
#             obj = Peoples.objects.get(id=_id)
#         except Peoples.DoesNotExist:
#             obj = Peoples.objects.create(id=_id)
#
#         for k, v in request.data.items():
#             if k == 'first_name':
#                 obj.first_name = v
#             elif k == 'last_name':
#                 obj.last_name = v
#             elif k == 'mobile':
#                 obj.mobile = v
#             elif k == 'is_legal':
#                 obj.is_legal = v
#             elif k == 'description':
#                 obj.description = v
#             elif k == 'image':
#                 obj.image = v
#             elif k == 'places':
#                 places = request.data.get('places')
#             obj.save()
#         for place in places:
#             Places.objects.create(place_owner=obj, **place)
#         leads_as_json = serializers.serialize('json', [obj, ])
#         return HttpResponse(leads_as_json, content_type='json')
#         # return JsonResponse([obj.first_name,obj.last_name,obj.is_legal], safe=False)
#         # return JsonResponse ({'status':'ok',},encoder=JSONEncoder)
#
#
# def refresh_sms_token_view(request):
#     if not request.user.is_staff:
#         return HttpResponse(status=403)
#     else:
#         try:
#             # eager = refresh_sms_token.apply()
#             ee = refresh_sms_token()
#             # return redirect('Http://127.0.0.1:8000/admin/constance/config/')
#             return redirect('Http://185.211.57.73/admin/constance/config/')
#         except Exception as e:
#             trace_back = traceback.format_exc()
#             message = str(e) + "\n" + str(trace_back)
#             logger.debug("ERROR:\n%s" % message)
#             return HttpResponse(status=500)
#
#
# @api_view(['POST'])
# def get_childern_view_by_token(request):
#     try:
#         ranks = Ranks.objects.all()
#     except Ranks.DoesNotExist:
#         return HttpResponse('جایگاهی تعریف نشده است.', status=500)
#     childern = {}
#     r = []
#     _parent_id = []
#     try:
#         if request.data.get('rank_name'):
#             _ranks = Ranks.objects._mptt_filter(rank_owner=request.user, rank_name=request.data.get('rank_name'))
#         else:
#             _ranks = Ranks.objects._mptt_filter(rank_owner=request.user)
#     except Ranks.DoesNotExist:
#         return HttpResponse('جایگاهی برای شما تعریف نشده است.', status=500)
#     for _rank in _ranks:
#         _parent_id.append(_rank.id)
#
#     if _parent_id == []:
#         return HttpResponse('جایگاهی برای شما تعریف نشده است.', status=500)
#     else:
#         for _rank in _ranks:
#             childs = {}
#             pids = []
#             pids.append(_rank.id)
#             for pid in pids:
#                 for rank in ranks:
#                     if rank.tree_id == _rank.tree_id:
#                         if pid == rank.parent_id:
#                             if rank.rank_owner_id is not None:
#                                 c = rank.rank_owner_id
#                                 if c in childs.keys():
#                                     pass
#                                 else:
#                                     pic = ("http://185.211.57.73/static/uploads/%s" % rank.rank_owner.image)
#
#                                     # title = rank.rank_owner.first_name + " " + rank.rank_owner.last_name
#                                     # slug = slugify(title)
#                                     # basename, file_extension = rank.rank_owner.image.split(".")
#                                     # new_filename = "%s.%s" % (slug, file_extension)
#                                     child = {"rank_name": rank.rank_name, "id": rank.rank_owner.id,
#                                              "first_name": rank.rank_owner.first_name,
#                                              "last_name": rank.rank_owner.last_name, "mobile": rank.rank_owner.mobile,
#                                              "is_legal": rank.rank_owner.is_legal,
#                                              # "pic":"http://185.211.57.73/static/uploads/%s" % (rank.rank_owner.image)
#                                              "pic": pic
#                                              }
#                                     r.append(child)
#                                     childs[rank.rank_name] = child
#                                     child = {}
#                             p = rank.id
#                             if p in pids:
#                                 pass
#                             else:
#                                 pids.append(rank.id)
#             if request.data.get('rank_name'):
#                 _rank_ = Ranks.objects.get(rank_owner=request.user, rank_name=request.data.get('rank_name'))
#             else:
#                 _rank_ = Ranks.objects.get(rank_owner=request.user)
#
#             childern["جایگاه"] = _rank_.rank_name
#             childern["تعداد کل"] = len(r)
#             childern["لیست"] = r
#         t = 0
#         for i in childern.values():
#             if i:
#                 t += 1
#             else:
#                 t += 0
#         if t == 0:
#             return HttpResponse('شما زیردستی ندارید.', status=500)
#         else:
#             return JsonResponse(childern, safe=False)
#
#
# @api_view(['POST'])
# def get_place_by_owner(request):
#     obj = []
#     try:
#         places = Places.objects.filter(place_owner=request.user)
#         for place in places:
#             obj.append(place)
#         leads_as_json = serializers.serialize('json', obj)
#         return HttpResponse(leads_as_json, content_type='json')
#     except Places.DoesNotExist:
#         places = None
#         return HttpResponse("مکانی برای شما یافت نشد.")
#
# @api_view(['POST'])
# def set_fcm_token(request):
#     try:
#         people = Peoples.objects.get(id=request.user.id)
#         people.fcm_token = request.data.get('fcm_token')
#         people.save()
#         from json import JSONEncoder
#         return JsonResponse({'status': 'ok', }, encoder=JSONEncoder)
#     except Places.DoesNotExist:
#         return HttpResponse("خطا در ثبت  توکن")
#
# @api_view(['POST'])
# def call_fcm(request):
#     import firebase_admin
#     from firebase_admin import credentials, messaging
#     from json import JSONEncoder
#
#     cred = credentials.Certificate('/opt/w/civil/civilportal.json')
#     # cred = credentials.Certificate('civilportal.json')
#
#     try:
#         default_app = firebase_admin.initialize_app(cred)
#     except Exception as e:
#         print(e)
#     _user = Peoples.objects.get(id=request.user.id)
#     token = _user.fcm_token
#     message = messaging.Message(
#         data={
#             "messageFrom": "Vouch!",
#             "body": "برای شما در تاریخ 18 مهر جلسه ای تایین شده است برای اطلاع بیشتر به اپ مراجعه نمایید"
#         },
#         token=token,
#     )
#     response = messaging.send(message)
#     return JsonResponse({'token': token, 'response': response}, encoder=JSONEncoder)
#
# class RepViewSet(viewsets.ModelViewSet):
#     permission_classes = (IsAuthenticated,)
#     queryset = Audiences.objects.all()
#     serializer_class = AudienceSerializer
#
#     def create(self, request, *args, **kwargs):
#         try:
#             ppl_id = request.user.id
#             session_id = request.data.get('session_id')
#             _rep_ppl = Peoples.objects.get(id=request.data.get('rep_ppl'))
#             force = self.request.data.get('force')
#         except:
#             _rep_ppl = None
#             session_id = None
#
#         intrposition = []
#         myformat = '%Y-%m-%d %H:%M:%S'
#         session = Sessions.objects.get(id=session_id)
#         sdate = datetime.datetime.strptime(str(session.start_time), myformat).date()
#         edate = datetime.datetime.strptime(str(session.end_time), myformat).date()
#         stime = datetime.datetime.strptime(str(session.start_time), myformat).time()
#         etime = datetime.datetime.strptime(str(session.end_time), myformat).time()
#
#         try:
#             _sessions = Sessions.objects.filter(meeting_owner_id=_rep_ppl.id)
#         except Sessions.DoesNotExist:
#             _sessions = None
#
#         try:
#             _audiences = Audiences.objects.filter(people_id=_rep_ppl.id)
#         except Audiences.DoesNotExist:
#             _audiences = None
#
#         try:
#             rep_audiences = Audiences.objects.filter(rep_ppl=_rep_ppl.id)
#         except Audiences.DoesNotExist:
#             rep_audiences = None
#
#         for _session in _sessions:
#             if str(_session.start_time.date()) == str(sdate) or str(_session.end_time.date()) == str(edate):
#                 if stime <= _session.end_time.time() <= etime or stime <= _session.start_time.time() <= etime:
#                     s = {}
#                     s["تشکیل دهنده"] = str(
#                         _session.meeting_title)
#                     intrposition.append(s)
#         for _audience in _audiences:
#             if str(_audience.session.start_time.date()) == str(sdate) or str(_audience.session.end_time.date()) == str(
#                     edate):
#                 if stime <= _audience.session.end_time.time() <= etime or stime <= _audience.session.start_time.time() <= etime:
#                     a = {}
#                     a["دعوت شده"] = str(
#                         _audience.session.meeting_title)
#                     intrposition.append(a)
#
#         for rep_audience in rep_audiences:
#             if str(rep_audience.session.start_time.date()) == str(sdate) or str(
#                     rep_audience.session.end_time.date()) == str(edate):
#                 if stime <= rep_audience.session.end_time.time() <= etime or stime <= rep_audience.session.start_time.time() <= etime:
#                     r = {}
#                     r["جایگزین"] = str(
#                         rep_audience.session.meeting_title)
#                     intrposition.append(r)
#
#         if intrposition != [] and force == 0:
#             return Response(', '.join(map(str, intrposition)) + "تداخل با جلسه:")
#         else:
#             if Audiences.objects.get(people=ppl_id, session=session_id):
#                 obj = Audiences.objects.get(people=ppl_id, session=session_id)
#                 obj.rep_ppl = _rep_ppl
#                 obj.save()
#                 if Seens.objects.get(ppl_id=_rep_ppl.id, sesion_id=session_id) is None:
#                     Seens.objects.create(ppl_id=_rep_ppl.id, sesion_id=session_id)
#
#                 cred = credentials.Certificate('/opt/w/civil/civilportal.json')
#                 # cred = credentials.Certificate('civilportal.json')
#                 try:
#                     default_app = firebase_admin.initialize_app(cred)
#                 except Exception as e:
#                     print(e)
#                 if obj.rep_ppl is not None:
#                     token = obj.rep_ppl.fcm_token
#                     if token is not None:
#                         mess = "برای شما در تاریخ {} ساعت {} جلسه ای تایین شده است برای اطلاع بیشتر به اپ مراجعه نمایید".format(
#                             sdate, stime)
#                         message = messaging.Message(
#                             data={
#                                 "body": mess
#                             },
#                             token=token,
#                         )
#                         messaging.send(message)
#                 leads_as_json = serializers.serialize('json', [obj, ])
#                 return HttpResponse(leads_as_json, content_type='json')
#
#
# @api_view(['POST'])
# def get_sessions_by_date(request):
#     # sdate = jalali.Persian(request.data.get('s_time')).gregorian_datetime()
#     sdate = datetime.datetime.strptime(request.data.get('time'), "%Y-%m-%d")
#     s_sessions = []
#     myformat = '%Y-%m-%d %H:%M:%S'
#     try:
#         _sessions = Sessions.objects.filter(meeting_owner=request.user)
#     except Sessions.DoesNotExist:
#         _sessions = None
#
#     try:
#         ppl_audiences = Audiences.objects.filter(people=request.user)
#     except Audiences.DoesNotExist:
#         _audiences = None
#
#     try:
#         rep_audiences = Audiences.objects.filter(rep_ppl=request.user)
#     except Audiences.DoesNotExist:
#         rep_audiences = None
#
#     for _session in _sessions:
#         stime = datetime.datetime.strptime(str(_session.start_time), myformat).date()
#         if stime.year == sdate.year and stime.month == sdate.month and stime.day == sdate.day:
#             s_sessions.append(
#                 {
#                     'id': _session.id,
#                     'meeting_title': _session.meeting_title,
#                     'place_address': str(_session.address),
#                     'start_time': str(_session.start_time),
#                     'end_time': str(_session.end_time),
#                     'image': "http://185.211.57.73/static/uploads/%s" % str(_session.meeting_owner.image),
#                     'owner': True,
#                 }
#             )
#
#     for _audience in ppl_audiences:
#         stime = datetime.datetime.strptime(str(_audience.session.start_time), myformat).date()
#         if stime.year == sdate.year and stime.month == sdate.month and stime.day == sdate.day:
#             s_sessions.append(
#                 {
#                     'id': _audience.session.id,
#                     'meeting_title': _audience.session.meeting_title,
#                     'place_address': str(_audience.session.address),
#                     'start_time': str(_audience.session.start_time),
#                     'end_time': str(_audience.session.end_time),
#                     'image': "http://185.211.57.73/static/uploads/%s" % str(_audience.session.meeting_owner.image),
#                     'owner': False
#                 }
#             )
#
#     for _audience in rep_audiences:
#         stime = datetime.datetime.strptime(str(_audience.session.start_time), myformat).date()
#         if stime.year == sdate.year and stime.month == sdate.month and stime.day == sdate.day:
#             s_sessions.append({
#                 'id': _audience.session.id,
#                 'meeting_title': _audience.session.meeting_title,
#                 'owner': False,
#                 'start_time': str(_audience.session.start_time),
#                 'end_time': str(_session.end_time),
#                 'place_address': str(_audience.session.address),
#                 'image': "http://185.211.57.73/static/uploads/%s" % str(_audience.session.meeting_owner.image),
#             })
#     return JsonResponse(s_sessions, safe=False)
#
# @api_view(['POST'])
# def get_session_by_id(request):
#     r = []
#     session = []
#     session_id = request.data.get('id')
#     try:
#         _audiences = Audiences.objects.filter(session_id=session_id)
#     except Audiences.DoesNotExist:
#         _audiences = None
#     i = 1
#     for _audience in _audiences:
#         rr = {}
#         # rr["id"] = _audience.people.id
#         rr["first_name"] = _audience.people.first_name
#         rr["last_name"] = _audience.people.last_name
#         rr["seen"] = Seens.objects.get(ppl_id = _audience.people.id, sesion_id = session_id).seen
#         rr["image"] = "http://185.211.57.73/static/uploads/%s" % _audience.people.image
#         try:
#             rr["rep_first_name"] = _audience.rep_ppl.first_name
#             rr["rep_last_name"] = _audience.rep_ppl.last_name
#             rr["rep_seen"] = Seens.objects.get(ppl_id = _audience.rep_ppl.id, sesion_id = session_id).seen
#             rr["rep_image"] = "http://185.211.57.73/static/uploads/%s" % _audience.rep_ppl.image
#         except:
#             rr["rep_first_name"] = None
#             rr["rep_last_name"] = None
#             rr["rep_seen"] = False
#             rr["rep_image"] = None
#         r.append(rr)
#         i += 1
#     try:
#         _session = Sessions.objects.get(id=request.data.get('id'))
#     except Sessions.DoesNotExist:
#         _session = None
#     session.append({
#         'id': _session.id,
#         'meeting_title': str(_session.meeting_title),
#         'meeting_owner': str(_session.meeting_owner.first_name) + '-' + str(_session.meeting_owner.last_name),
#         'owner_image': "http://185.211.57.73/static/uploads/%s" % _session.meeting_owner.image,
#         'start_time': str(_session.start_time),
#         'end_time': str(_session.end_time),
#         'place_address': str(_session.address),
#         'people': r
#     })
#     return JsonResponse(session, safe=False)
#
# @api_view(['POST'])
# def seen_session_by_ppl(request):
#     session_id = request.data.get('session_id')
#     _session = Sessions.objects.get(pk=session_id)
#     _ppl = request.user
#     _seen = Seens.objects.get(ppl = _ppl, sesion =_session)
#     obj = []
#     _seen.seen = True
#     _seen.save()
#     obj.append({
#         'session': str(_session.meeting_title),
#         'ppl': str(_ppl.first_name) + ' ' + str(_ppl.last_name),
#         'seen': str(_seen.seen),
#     })
#     return JsonResponse(obj, safe=False)
#
#
#
#
