import re

from celery import Celery
from django.core import serializers
import jdatetime
import requests
from bs4 import BeautifulSoup
from django.http.response import HttpResponse
from Scraping.models import Links , Prices

import logging
logger = logging.getLogger(__name__)

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'}
app = Celery('tar')

@app.task
def get_prices():

    _links = Links.objects.all()
    for _link in _links:

        site = re.findall("//(.*?)/", _link.url)
        if site != []:
            obj = Prices.objects.create(link=_link , date=jdatetime.datetime.now())
            r = requests.get(_link, headers=headers)
            soup = BeautifulSoup(r.text, "html.parser")
            product={
                "price":"00",
                "unit":"تومان",
            }



            #1- iransote.com
            if site[0] == "iransote.com":
                p = soup.find("p" , attrs = {"class" : "price"})
                if soup.find("p" , attrs = {"class" : "stock out-of-stock"}) == None:
                    s = p.find("ins")
                    if s!= None:
                        a = re.sub(r',', '', s.text).strip()
                    else:
                        a = re.sub(r',', '', p.text).strip()
                    b = re.findall(r'\d+', a)
                else:
                    b = [""]
                product["price"] = b[0]
                # print(product)


            #2- iranloop.ir
            elif site[0] == "iranloop.ir":
                p = soup.find("p" , attrs = {"class" : "our_price_display"})
                if soup.find("p" , attrs = {"id" : "availability_statut"}).text == " موجود است":
                    s = p.find("span" , attrs = {"class" : "price"})
                    if s!= None:
                        a = re.sub(r',' , '' , s.text).strip()
                        b = re.findall(r'\d+',a)
                else:
                    b = [""]
                product["price"] = b[0]
                # print(product)

            #3- www.sazforoosh.com
            elif site[0] == "www.sazforoosh.com":
                p = soup.find("div" , attrs = {"class" : "price"})
                if soup.find("div" , attrs = {"id" : "product"}).find('p'):
                    b = [""]
                else:
                    s = p.find("h3")
                    a = re.sub(r',' , '' , s.text).strip()
                    b = re.findall(r'\d+',a)
                product["price"] = b[0]
                # print(product)

            #4- sazkala.com
            elif site[0] == "sazkala.com":
                p = soup.find("p" , attrs = {"class" : "price"})
                if soup.find("div" , attrs = {"class" : "absolute-label-product outofstock-product"}):
                    b = [""]
                else:
                    s = p.find("ins")
                    if s!= None:
                        a = re.sub(r',', '', s.text).strip()
                    else:
                        a = re.sub(r',', '', p.text).strip()
                    b = re.findall(r'\d+', a)
                product["price"] = b[0]
                # print(product)

            #5- sedastore.com
            elif site[0] == "sedastore.com":
                p = soup.find("p" , attrs = {"class" : "price"})
                if soup.find("p" , attrs = {"class" : "woocommerce-error"}) or soup.find("p" , attrs = {"class" : "price"}).find("strong"):
                    b = [""]
                else:
                    s = p.find("ins")
                    if s != None:
                        a = re.sub(r',', '', s.text).strip()
                    else:
                        a = re.sub(r',', '', p.text).strip()
                    b = re.findall(r'\d+', a)
                product["price"] = b[0]
                # print(product)

            #6- www.djcenter.net
            elif site[0] == "www.djcenter.net":
                p = soup.find("span" , attrs = {"itemprop" : "price"})
                if p != None:
                    s = re.sub(r'\s+', ' ', p.text).strip()
                    a = re.sub(r',', '', s)
                    b = re.findall(r'\d+', a)
                else:
                    b = [""]
                product["price"] = b[0]
                # print(product)

            #7- digiseda.ir
            elif site[0] == "digiseda.ir":
                p = soup.find("div" , attrs = {"id" : "our_price_display" , "class" : "prd-price"})
                if p != None:
                    if soup.find("span" , attrs = {"id" : "our_price_display" , "class" : "price"}) == None :
                        s = re.sub(r'\s+', ' ', p.text).strip()
                        a = re.sub(r',', '', s)
                        b = re.findall(r'\d+', a)
                    else:
                        b = [""]
                    product["price"] = b[0]
                # print(product)

            #8- rayanseda.com
            elif site[0] == "rayanseda.com":
                p = soup.find("div" , attrs = {"class" : "col-md-6 col-12 cost-product"})
                if p != None:
                    if p.find("span" , attrs = {"class" : "row-off-cost"}):
                        s = p.find("span" , attrs = {"class" : "row-off-cost"})
                    else:
                        s = p.find("span", attrs={"class": "prise-row orginal"})
                    a = re.sub(r',', '', s.text).strip()
                    b = re.findall(r'\d+', a)
                else:
                    b = [""]
                product["price"] = b[0]
                # print(product)

            #9- www.sornashop.com
            elif site[0] == "www.sornashop.com":
                p = soup.find("p" , attrs = {"class" : "price"})
                if p != None:
                    if soup.find("p" , attrs = {"class" : "stock out-of-stock"}) == None:
                        if p.find("ins") != None:
                            s = p.find("ins")
                        else:
                            s = p.find("bdi")
                        a = re.sub(r',', '', s.text).strip()
                        b = re.findall(r'\d+', a)
                    else:
                        b = [""]
                    product["price"] = b[0]
                # print(product)

            #10- davarmelody.com
            elif site[0] == "davarmelody.com":
                if soup.find("div" , attrs = {"id" : "product"}).find("p") == None:
                    p = soup.find("span" , attrs = {"itemprop" : "price"})
                    s = re.sub(r'\s+', ' ', p.text).strip()
                    a = re.sub(r',', '', s)
                    b = re.findall(r'\d+', a)
                else:
                    b = [""]
                product["price"] = b[0]
                # print(product)

            #11- www.tehranmelody.com
            elif site[0] == "www.tehranmelody.com" or  site[0] =="tehranmelody.software":
                if soup.find("button" , attrs = {"id" : "button-cart"}):
                    p = soup.find("div" , attrs = {"class" : "price"})
                    s = re.sub(r'\s+', ' ', p.text).strip()
                    a = re.sub(r',', '', s)
                    b = re.findall(r'\d+', a)
                else:
                    b = [""]
                product["price"] = b[0]
                # print(product)

            #12- navamarket.ir
            elif site[0] == "navamarket.ir":
                p = soup.find("span" , attrs = {"class" : "price" , "itemprop" : "price"})
                if p.attrs['content'] == '1' or p.attrs['content'] == '4':
                    b = [""]
                else:
                    s = re.sub(r'\s+', ' ', p.text).strip()
                    a = re.sub(r',', '', s)
                    b = re.findall(r'\d+', a)
                product["price"] = b[0]
                # print(product)

            #13- golhastore.ir
            elif site[0] == "golhastore.ir":
                p = soup.find("span" , attrs = {"class" : "price" , "itemprop" : "price"})
                if p.text == 'لطفا تماس بگیرید.':
                    b = [""]
                else:
                    s = re.sub(r'\s+', ' ', p.text).strip()
                    a = re.sub(r',', '', s)
                    b = re.findall(r'\d+', a)
                product["price"] = b[0]
                # print(product)

            #14- ertebat.co
            elif site[0] == "ertebat.co":
                if soup.find("span" , attrs = {"itemprop" : "price"}):
                    p = soup.find("span", attrs={"itemprop": "price"})
                    s = re.sub(r'\s+', ' ', p.text).strip()
                    a = re.sub(r'\.', '', s)
                    b = re.findall(r'\d+', a)
                else:
                    b = [""]
                product["price"] = b[0]
                # print(product)

            #15- delshadmusic.com
            elif site[0] == "delshadmusic.com":
                if soup.find("button" , attrs = {"name" : "add-to-cart"}):
                    p = soup.find("span" , attrs = {"class" : "woocommerce-Price-amount amount"})
                    s = re.sub(r'\s+', ' ', p.text).strip()
                    a = re.sub(r',', '', s)
                    b = re.findall(r'\d+', a)
                else:
                    b = [""]
                product["price"] = b[0]
                # print(product)

            obj.value = product["price"]
            obj.unit = product["unit"]
            obj.save()
            # leads_as_json = serializers.serialize('json', [obj, ])
            # return HttpResponse(leads_as_json, content_type='json')
