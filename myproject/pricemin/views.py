
from django.shortcuts import render
from pricemin.models import Region, Town, Adress, Product, Events
from pricemin.forms import TownForm, AdressForm, ProductForm, EventsForm
from django.shortcuts import get_list_or_404, render, render_to_response, redirect
from django.template import RequestContext, loader
from django.http import HttpResponseRedirect, HttpResponseNotFound, HttpResponse
from django.template.context_processors import csrf
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from pricemin.models import Adress, Town, Product
from django.utils import timezone
from datetime import timedelta
from django.utils.http import urlquote
from django.utils.encoding import iri_to_uri
from django.contrib import auth

#flag = '' # переменная для определения с какого устройства вход

exceptions_town = [1, 2, 3, 4, 5, 6, 7, 8, 9,10,
		           11, 12, 13, 14, 15, 16, 17, 
				   18, 19, 20, 21, 22, 23, 24, 
				   25, 26, 27, 28, 29, 30] 
#Список городов которые ненадо удалять т.к. это районы Москвы и Санкт-Петербурга

# Функция для обновления даты 
def updateTime():
    green = timezone.now() - timedelta(days=1) #дней пока цена зеленая
    yelow = timezone.now() - timedelta(days=3) #дней пока цена желная
    red = timezone.now() - timedelta(days=7) #дней пока цена красная
    color = {'green':green, 'yelow':yelow, 'red':red} #словарь с цветами по дате
    return color

time_delete_town = 1 #время через которое удаляется объект Город
time_delete_adress = 3 #время через которое удаляется объект Адрес
time_delete_product = 14 #время через которое удаляется объект Продукт
time_delete_event = 20 #время через которое удаляется объект Событие

class ProductUpdate(UpdateView):
    model = Product
    fields = ['product_name', 'product_price']

# Create your views here.
# Сдесь мы стартуем из десктопа
def index(request): 
    return render(request, 'pricemin/des/index.html')

#Для десктопа
def index_des(request):
    flag = 'des'
    region_list = Region.objects.all().order_by('region_name')
    return render(request, 'pricemin/des/index_des.html', {'region_list':region_list, 'flag':flag})

#для Мобильных устройств здесь!
def index_mob(request):
    flag = 'mob'
    region_list = Region.objects.all().order_by('region_name')
    return render(request, 'pricemin/mob/index_mob.html', {'region_list':region_list, 'flag':flag})

##Страница "о программе" из десктопа 
def about_des(request, flag): 
        return render(request, 'pricemin/des/about_des.html')

# Страница "о программе" из смартфона    
def about_mob(request, flag, town_id):
    flag = flag
    town = Town.objects.get(id=town_id)
    return render_to_response('pricemin/mob/about_mob.html', {'flag':flag, 'town':town})

# Страница со списком городов откуда выбираем город и попадаем на 
def town_list(request, flag, region_id):
    if request.user.is_authenticated():
        if Region.objects.filter(id=region_id).exists():
            region = Region.objects.get(id=region_id)
            list = Town.objects.filter(region__id=region_id)
            for town in list:
                if town.town_date < timezone.now() - timezone.timedelta(days=time_delete_town) and town.id not in exceptions_town:
                    adress_list = Adress.objects.filter(town__id=town.id)
                    if adress_list:
                        continue
                    else:
                        town.delete_obj()
            town_list = Town.objects.filter(region__id=region_id).order_by('town_name')
            context = {'town_list':town_list, 'region':region, 'flag':flag}
            response_des = render_to_response('pricemin/des/town_list.html', context)
            response_mob = render_to_response('pricemin/mob/town_list_mob.html', context)
            response_pro = render_to_response('pricemin/pro/town_list_pro.html', context)
            response_mega_des = render_to_response('pricemin/des/town_list_mega.html', context)
            response_mega_mob = render_to_response('pricemin/mob/town_list_mega_mob.html', context)
            response_mega_pro = render_to_response('pricemin/pro/town_list_mega_pro.html', context)
            if region.id == 1 or region.id == 2:
                if flag == 'des':
                    return response_mega_des
                elif flag == 'mob':
                    return response_mega_mob
                elif flag == 'pro':
                    return response_mega_pro
            if flag == 'des':
                return response_des
            elif flag == 'mob':
                return response_mob
            elif flag == 'pro':
                return response_pro
            else:
                return HttpResponseNotFound('<h1>Page not found</h1>')
        else:
            region_list = Region.objects.all().order_by('region_name')
            if flag == 'des':
                return HttpResponseRedirect(reverse('index_des'))
            else:
                return HttpResponseRedirect(reverse('index_mob'))
    else:
        if flag == 'des':
            return HttpResponseRedirect(reverse('index_des'))
        else:
            return HttpResponseRedirect(reverse('index_mob'))

# Лицевая страница где вверху обозначен город и два выбора "адрес" \ 
# и "продукт"
def town(request, flag, town_id):
    if request.user.is_authenticated():
        if request.user.is_active == True:
            try:
                user = auth.get_user(request)
                region = Region.objects.get(town__id=town_id)
                town = Town.objects.get(id=town_id)
                events = Events.objects.filter(town__id=town_id).order_by('-eventDate')[:7]
                context =  {'town':town, 'region':region, 'flag':flag, 'events':events, 'id': user.id}
                if flag == 'des':
                    return render_to_response( 'pricemin/des/town.html', context)
                if flag == 'mob':
                    return  render_to_response( 'pricemin/mob/town_mob.html', context)
                if flag == 'pro':
                    return  render_to_response( 'pricemin/pro/town_pro.html', context)
                else:
                    return  HttpResponseNotFound('<h1>Page not found</h1>')
            except Region.DoesNotExist:
                if flag == 'des':
                    return HttpResponseRedirect(reverse('index_des'))
                else:
                    return HttpResponseRedirect(reverse('index_mob'))
        else:
            return  redirect('deactivate', flag)
    else:
        if flag == 'des':
            return HttpResponseRedirect(reverse('index_des'))
        else:
            return HttpResponseRedirect(reverse('index_mob'))

#Нажав "Выбрать адрес" переходим на страницу со списком продуктов для\
		#этого адреса
def adress_list(request, flag, region_id, town_id):
    try:
        region = Region.objects.get(id=region_id)
        town = Town.objects.get(id=town_id)
        events = Events.objects.filter(town__id=town_id).order_by('-eventDate')[:7]
        list = Adress.objects.filter(town__id=town_id)
        for adress in list:
            if adress.adress_date < timezone.now() - timezone.timedelta(days=time_delete_adress):
                product_list = Product.objects.filter(adress__id=adress.id)
                if product_list:
                    continue
                else:
                    adress.delete_obj() 
        adress_list = Adress.objects.filter(town__id=town_id).order_by('street')      
        context = {'adress_list':adress_list, 'town':town, 'region':region, 'flag':flag, 'events':events}
        if flag == 'des':
            return render_to_response('pricemin/des/adress_list.html', context)
        elif flag == 'mob':
            return render_to_response('pricemin/mob/adress_list_mob.html', context)
        elif flag == 'pro':
            return render_to_response('pricemin/pro/adress_list_pro.html', context)
        else:
            return  HttpResponseNotFound('<h1>Page not found</h1>')
    except ObjectDoesNotExist:
        if flag == 'des':
            return HttpResponseRedirect(reverse('index_des'))
        else:
            return HttpResponseRedirect(reverse('index_mob'))


def products_adress(request, flag, region_id, adress_id, town_id):
    try:
        region = Region.objects.get(id=region_id)
        town = Town.objects.get(id=town_id)
        adress = Adress.objects.get(id=adress_id)
        events = Events.objects.filter(town__id=town_id).order_by('-eventDate')[:7]
        list = adress.product_set.all()
        for product in list:
            if product.product_date < timezone.now() - timezone.timedelta(days=time_delete_product):
                product.delete_obj() 
        products_list = adress.product_set.all().order_by('product_name')
        color = updateTime()
        context = {'products_list':products_list, 'adress':adress, 'town':town , 'region':region, 'color':color, 'flag':flag, 'events':events}
        if flag == 'des':
            return render_to_response('pricemin/des/products_adress.html', context)
        elif flag == 'mob':
            return render_to_response('pricemin/mob/products_adress_mob.html', context)
        elif flag == 'pro':
            return render_to_response('pricemin/pro/products_adress_pro.html', context)
        else:
            return  HttpResponseNotFound('<h1>Page not found</h1>')
    except ObjectDoesNotExist:
        if flag == 'des':
            return HttpResponseRedirect(reverse('index_des'))
        else:
            return HttpResponseRedirect(reverse('index_mob'))


#============================== Create ============================================

def town_create(request, flag, region_id):
    try:
        user = auth.get_user(request)
        user_id = user.id
        region = Region.objects.get(id=region_id)
        region = Region.objects.get(id=region_id)
        town_form = TownForm({'region':region, 'user_id': user_id})
        args={}
        args.update(csrf(request))
        args['flag']=flag
        args['form']=town_form
        args['region']=region
        args['user_id']=user_id
        if flag == 'des':
            return render_to_response('pricemin/des/town_create.html', args)
        elif flag == 'mob':
            return render_to_response('pricemin/mob/town_create_mob.html', args)
        elif flag == 'pro':
            return render_to_response('pricemin/pro/town_create_pro.html', args)
        else:
            return  HttpResponseNotFound('<h1>Page not found</h1>')
    except ObjectDoesNotExist:
        if flag == 'des':
            return HttpResponseRedirect(reverse('index_des'))
        else:
            return HttpResponseRedirect(reverse('index_mob'))


def adress_create(request, flag, region_id, town_id):
    try:
        user = auth.get_user(request)
        user_id = user.id
        region = Region.objects.get(id=region_id)
        region = Region.objects.get(id=region_id)
        town = Town.objects.get(id=town_id)
        events = Events.objects.filter(town__id=town_id).order_by('-eventDate')[:7]
        adress_form = AdressForm({'town':town, 'user_id': user_id})
        args = {}   
        args.update(csrf(request))
        args['flag'] = flag
        args['form'] = adress_form
        args['town'] = town
        args['region']= region
        args['events']=events
        args['user_id']=user_id
        if flag == 'des':
            return render_to_response('pricemin/des/adress_create.html', args)
        elif flag == 'mob':
            return render_to_response('pricemin/mob/adress_create_mob.html', args)
        elif flag == 'pro':
            return render_to_response('pricemin/pro/adress_create_pro.html', args)
        else:
            return  HttpResponseNotFound('<h1>Page not found</h1>')
    except ObjectDoesNotExist:
        if flag == 'des':
            return HttpResponseRedirect(reverse('index_des'))
        else:
            return HttpResponseRedirect(reverse('index_mob'))


def product_create(request, flag, region_id, adress_id, town_id):
    try:
        user = auth.get_user(request)
        user_id = user.id
        region = Region.objects.get(id=region_id)
        town = Town.objects.get(id=town_id)
        region = Region.objects.get(id=region_id)
        adress= Adress.objects.get(id=adress_id)
        events = Events.objects.filter(town__id=town_id).order_by('-eventDate')[:7]
        product_form = ProductForm({'adress':adress, 'user_id': user_id})
        args = {}
        args.update(csrf(request))
        args['flag'] = flag
        args['form'] = product_form
        args['adress'] = adress
        args['town'] = town
        args['region']= region
        args['events']=events
        args['user_id']=user_id
        if flag == 'des':
            return render_to_response('pricemin/des/product_create.html', args)
        elif flag == 'mob':
            return render_to_response('pricemin/mob/product_create_mob.html', args)
        elif flag == 'pro':
            return render_to_response('pricemin/pro/product_create_pro.html', args)
        else:
            return  HttpResponseNotFound('<h1>Page not found</h1>')
    except ObjectDoesNotExist:
        if flag == 'des':
            return HttpResponseRedirect(reverse('index_des'))
        else:
            return HttpResponseRedirect(reverse('index_mob'))


def event_create(request, flag, town_id):
    try:
        user = auth.get_user(request)
        user_id = user.id
        town = Town.objects.get(id=town_id)
        events = Events.objects.filter(town__id=town_id).order_by('-eventDate')[:7]
        event_form = EventsForm({'town':town, 'user_id': user_id})
        args = {}
        args.update(csrf(request))
        args['flag'] = flag
        args['form'] = event_form
        args['town'] = town
        args['events']=events
        args['user_id']=user_id
        if flag == 'des':
            return render_to_response('pricemin/des/event_create.html', args)
        elif flag == 'mob':
            return render_to_response('pricemin/mob/event_create_mob.html', args)
        elif flag == 'pro':
            return render_to_response('pricemin/pro/event_create_pro.html', args)
        else:
            return  HttpResponseNotFound('<h1>Page not found</h1>')
    except ObjectDoesNotExist:
        if flag == 'des':
            return HttpResponseRedirect(reverse('index_des'))
        else:
            return HttpResponseRedirect(reverse('index_mob'))


def addtown(request, flag, region_id):
    try:
        region = Region.objects.get(id=region_id)
        args = {}
        args.update(csrf(request))
        args['flag'] = flag
        args['region'] = region
        town_list = Town.objects.filter(region__id=region_id)
        townName_list = []
        error_exist = 'Такой город уже существует!'
        for i in town_list:
            townName_list.append(i.town_name)
        if request.method == 'POST':
            form = TownForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                cd_prefix = cd['prefix']
                cd_town_name = cd['town_name']
                cd_town_name = cd_town_name.capitalize()
                cd_town_name = cd_town_name.strip()
                cd_region = cd['region']
                if Town.objects.filter(prefix=cd_prefix, town_name=cd_town_name, region=cd_region).exists():
                    args['error_exist'] = error_exist
                    args['form'] = form
                    args['errors'] = form.errors
                    if flag == 'des':
                        return render_to_response('pricemin/des/town_create.html', args)
                    elif flag == 'mob':
                        return render_to_response('pricemin/mob/town_create_mob.html', args)
                    elif flag == 'pro':
                        return render_to_response('pricemin/pro/town_create_pro.html', args)
                    else:
                        return HttpResponseNotFound('<h1>Page not found</h1>')
                else:
                    newForm = form.save(commit=False)
                    newForm.town_name = newForm.town_name.capitalize()
                    newForm.town_name = newForm.town_name.strip()
                    if newForm.town_name not in townName_list:
                        newForm.save()
                    return HttpResponseRedirect(reverse('town_list', args=(flag, region.id,)))
            else:
                args['form'] = form
                args['errors'] = form.errors
                if flag == 'des':
                    return render_to_response('pricemin/des/town_create.html', args)
                elif flag == 'mob':
                    return render_to_response('pricemin/mob/town_create_mob.html', args)
                elif flag == 'pro':
                    return render_to_response('pricemin/pro/town_create_pro.html', args)
                else:
                    return HttpResponseNotFound('<h1>Page not found</h1>')

    except ObjectDoesNotExist:
        if flag == 'des':
            return HttpResponseRedirect(reverse('index_des'))
        else:
            return HttpResponseRedirect(reverse('index_mob'))

def addadress(request, flag, region_id, town_id):
    try:
        region = Region.objects.get(id=region_id)
        town = Town.objects.get(id=town_id)
        args = {}
        args.update(csrf(request))
        args['flag'] = flag
        args['region'] = region
        args['town'] = town
        error_exist = 'Такой магазин уже существует!'
        if request.POST:
            form = AdressForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                cd_prefix = cd['prefix']
                cd_street = cd['street']
                cd_number = cd['number']
                cd_adress_name = cd['adress_name']
                cd_town = cd['town']
                cd_adress_name = cd_adress_name.capitalize()
                cd_adress_name = cd_adress_name.strip()
                cd_street = cd_street.capitalize()
                cd_street = cd_street.strip()
                cd_number = cd_number.strip()
                if Adress.objects.filter(prefix=cd_prefix, street=cd_street, number=cd_number, adress_name=cd_adress_name, town=cd_town).exists():
                    args['error_exist'] = error_exist
                    args['form'] = form
                    args['errors'] = form.errors
                    if flag == 'des':
                        return render_to_response('pricemin/des/adress_create.html', args)
                    elif flag == 'mob':
                        return render_to_response('pricemin/mob/adress_create_mob.html', args)
                    elif flag == 'pro':
                        return render_to_response('pricemin/pro/adress_create_pro.html', args)
                    else:
                        return HttpResponseNotFound('<h1>Page not found</h1>')
                else:
                    newForm = form.save(commit=False)
                    newForm.adress_name = newForm.adress_name.capitalize()
                    newForm.adress_name = newForm.adress_name.strip()
                    newForm.street = newForm.street.capitalize()
                    newForm.street = newForm.street.strip()
                    newForm.number = newForm.number.strip()
                    newForm.save()
            else:
                args['form'] = form
                args['errors'] = form.errors
                if flag == 'des':
                    return render_to_response('pricemin/des/adress_create.html', args)
                elif flag == 'mob':
                    return render_to_response('pricemin/mob/adress_create_mob.html', args)
                elif flag == 'pro':
                    return render_to_response('pricemin/pro/adress_create_pro.html', args)
                else:
                    return HttpResponseNotFound('<h1>Page not found</h1>')
        return HttpResponseRedirect(reverse('adress_list', args=(flag, region.id, town.id,)))
    except ObjectDoesNotExist:
        if flag == 'des':
            return HttpResponseRedirect(reverse('index_des'))
        else:
            return HttpResponseRedirect(reverse('index_mob'))

def addproduct(request, flag, region_id, adress_id, town_id):
    try:
        region = Region.objects.get(id=region_id)
        town = Town.objects.get(id=town_id)
        adress = Adress.objects.get(id=adress_id)
        error_exist = 'Продукт по этому адресу уже существует!'
        args = {}
        args.update(csrf(request))
        args['flag'] = flag
        args['region'] = region
        args['town'] = town
        args['adress'] = adress
        product_list = Product.objects.filter(adress__id=adress_id)
        productName_list = []
        for i in product_list:
            productName_list.append(i.product_name)
        if request.POST:
                form = ProductForm(request.POST)
                if form.is_valid():
                    cd = form.cleaned_data
                    cd_product_name = cd['product_name']
                    cd_product_name = cd_product_name.capitalize()
                    cd_product_name = cd_product_name.strip()
                    cd_product_name = ' '.join(cd_product_name.split())
                    cd_adress = cd['adress']
                    if Product.objects.filter(product_name=cd_product_name, adress=cd_adress).exists():
                        args['error_exist']=error_exist
                        args['form'] = form
                        args['errors'] = form.errors
                        if flag == 'des':
                            return render_to_response('pricemin/des/product_create.html', args)
                        elif flag == 'mob':
                            return render_to_response('pricemin/mob/product_create_mob.html', args)
                        elif flag == 'pro':
                            return render_to_response('pricemin/pro/product_create_pro.html', args)
                        else:
                            return HttpResponseNotFound('<h1>Page not found</h1>')
                    else:
                        newForm = form.save(commit=False)
                        newForm.product_name = newForm.product_name.capitalize()
                        newForm.product_name = newForm.product_name.strip()
                        newForm.product_name = ' '.join(newForm.product_name.split())
                        if newForm.product_name not in productName_list:
                            newForm.save()
                else:
                    args['form'] = form
                    args['errors'] = form.errors
                    if flag == 'des':
                        return render_to_response('pricemin/des/product_create.html', args)
                    elif flag == 'mob':
                        return render_to_response('pricemin/mob/product_create_mob.html', args)
                    elif flag == 'pro':
                        return render_to_response('pricemin/pro/product_create_pro.html', args)
                    else:
                        return HttpResponseNotFound('<h1>Page not found</h1>')
        return HttpResponseRedirect(reverse('products_adress', args=(flag, region.id, adress.id, town.id,)))
    except ObjectDoesNotExist:
        if flag == 'des':
            return HttpResponseRedirect(reverse('index_des'))
        else:
            return HttpResponseRedirect(reverse('index_mob'))

def addEvent(request, flag, town_id):
    try:
        town = Town.objects.get(id=town_id)
        args = {}
        args.update(csrf(request))
        args['flag'] = flag
        args['town'] = town
        if request.POST:
                form = EventsForm(request.POST)
                if form.is_valid():
                    form.save()
                else:
                    args['form'] = form
                    args['errors'] = form.errors
                    if flag == 'des':
                        return render_to_response('pricemin/des/event_create.html', args)
                    elif flag == 'mob':
                        return render_to_response('pricemin/mob/event_create_mob.html', args)
                    elif flag == 'pro':
                        return render_to_response('pricemin/pro/event_create_pro.html', args)
                    else:
                        return HttpResponseNotFound('<h1>Page not found</h1>')
        return HttpResponseRedirect(reverse('events', args=(flag, town.id,)))
    except ObjectDoesNotExist:
        if flag == 'des':
            return HttpResponseRedirect(reverse('index_des'))
        else:
            return HttpResponseRedirect(reverse('index_mob'))


#=================================== Update ==========================================

def update_form_adress(request, flag, region_id, adress_id, product_id, town_id):
    try:
        user = auth.get_user(request)
        user_id = user.id
        town = Town.objects.get(id=town_id)
        region = Region.objects.get(id=region_id)
        adress= Adress.objects.get(id=adress_id)
        product = Product.objects.get(id=product_id)
        events = Events.objects.filter(town__id=town_id).order_by('-eventDate')[:7]
        product_name = product.product_name
        product_weight = product.product_weight
        product_price = product.product_price
        form = ProductForm({'adress':adress, 'product_name':product_name, 'product_price':product_price , 'product_weight': product_weight, 'user_id': user_id})
        args = {}
        args.update(csrf(request))
        args['flag'] = flag
        args['form'] = form
        args['adress'] = adress
        args['town'] = town
        args['region']= region
        args['product'] = product
        args['events']=events
        args['user_id']=user_id
        if flag == 'des':
            return render_to_response('pricemin/des/update_form_adress.html', args)
        elif flag == 'mob':
            return render_to_response('pricemin/mob/update_form_adress_mob.html', args)
        elif flag == 'pro':
            return render_to_response('pricemin/pro/update_form_adress_pro.html', args)
        else:
            return  HttpResponseNotFound('<h1>Page not found</h1>')
    except ObjectDoesNotExist:
        if flag == 'des':
            return HttpResponseRedirect(reverse('index_des'))
        else:
            return HttpResponseRedirect(reverse('index_mob'))


def update_form_town(request, flag, region_id, product_id, query, town_id):
    try:
        user = auth.get_user(request)
        user_id = user.id
        region = Region.objects.get(id=region_id)
        town = Town.objects.get(id=town_id)
        region = Region.objects.get(id=region_id)
        adress= Adress.objects.get(product__id=product_id)
        product = Product.objects.get(id=product_id)
        events = Events.objects.filter(town__id=town_id).order_by('-eventDate')[:7]
        product_name = product.product_name
        product_weight = product.product_weight
        product_price = product.product_price
        q = query
        form = ProductForm({'adress':adress, 'product_name':product_name, 'product_price':product_price , 'product_weight': product_weight, 'user_id': user_id})
        args = {}
        args.update(csrf(request))
        args['flag'] = flag
        args['form'] = form
        args['adress'] = adress
        args['town'] = town
        args['region']= region
        args['product'] = product
        args['events']=events
        args['query'] = q
        args['user_id']=user_id
        if flag == 'des':
            return render_to_response('pricemin/des/update_form_town.html', args)
        elif flag == 'mob':
            return render_to_response('pricemin/mob/update_form_town_mob.html', args)
        elif flag == 'pro':
            return render_to_response('pricemin/pro/update_form_town_pro.html', args)
        else:
            return  HttpResponseNotFound('<h1>Page not found</h1>')
    except ObjectDoesNotExist:
        if flag == 'des':
            return HttpResponseRedirect(reverse('index_des'))
        else:
            return HttpResponseRedirect(reverse('index_mob'))

# Функция формы обновления события
def update_form_event(request, flag, event_id,  town_id):
    try:
        user = auth.get_user(request)
        user_id = user.id
        town = Town.objects.get(id=town_id)
        event = Events.objects.get(id=event_id)
        prefix = event.prefix
        eventWhere = event.eventWhere
        eventComment = event.eventComment
        eventStart = event.eventStart
        eventStop = event.eventStop
        form = EventsForm({'prefix':prefix, 'eventWhere':eventWhere, 'eventComment':eventComment, 'town': town, 'eventStart': eventStart, 'eventStop': eventStop, 'user_id': user_id})
        args = {}
        args.update(csrf(request))
        args['flag'] = flag
        args['form'] = form
        args['event'] = event
        args['town'] = town
        args['user_id']=user_id
        if flag == 'des':
            return render_to_response('pricemin/des/update_event.html', args)
        elif flag == 'mob':
            return render_to_response('pricemin/mob/update_event_mob.html', args)
        elif flag == 'pro':
            return render_to_response('pricemin/pro/update_event_pro.html', args)
        else:
            return  HttpResponseNotFound('<h1>Page not found</h1>')
    except ObjectDoesNotExist:
        if flag == 'des':
            return HttpResponseRedirect(reverse('index_des'))
        else:
            return HttpResponseRedirect(reverse('index_mob'))


def product_update_adress(request, flag, region_id, adress_id, product_id, town_id):
    try:
        r = Region.objects.get(id=region_id)
        t = Town.objects.get(id=town_id)
        a = Adress.objects.get(id=adress_id)
        p = Product.objects.get(pk=product_id)
        if request.POST:
            form = ProductForm(request.POST, instance=p)
            if form.is_valid():
                form.save()
        return HttpResponseRedirect(reverse('products_adress', args=(flag, r.id, a.id, t.id,)))
    except ObjectDoesNotExist:
        if flag == 'des':
            return HttpResponseRedirect(reverse('index_des'))
        else:
            return HttpResponseRedirect(reverse('index_mob'))

# функция обновления которая вызывается из города и возвращается туда же
def product_update_town (request, flag, region_id, adress_id, product_id, query, town_id):
    try:
        region = Region.objects.get(id=region_id)
        r = Region.objects.get(id=region_id)
        t = Town.objects.get(id=town_id)
        a = Adress.objects.get(id=adress_id)
        p = Product.objects.get(pk=product_id)
        q = query
        color = updateTime()
        args = {}
        args['flag'] = flag
        args['town'] = t
        args['region']= r
        args['adress'] = a
        args['query'] = q
        if request.POST:
            form = ProductForm(request.POST, instance=p)
            if form.is_valid():
                form.save()
            product_list = Product.objects.filter(adress__town__id=t.id).order_by('product_price').filter(product_name__icontains=q)
            args['list'] = product_list
            args['color'] = color
            if flag == 'des':
                return render_to_response('pricemin/des/search_town_products_result.html', args)
            elif flag == 'mob':
                return render_to_response('pricemin/mob/search_town_products_result_mob.html', args)
            elif flag == 'pro':
                return render_to_response('pricemin/pro/search_town_products_result_pro.html', args)
            else:
                return  HttpResponseNotFound('<h1>Page not found</h1>')
        if flag == 'des':
            return render_to_response('pricemin/des/search_town_products_form.html', args)
        elif flag == 'mob':
            return render_to_response('pricemin/mob/search_town_products_form_mob.html', args)
        elif flag == 'pro':
            return render_to_response('pricemin/pro/search_town_products_form_pro.html', args)
        else:
            return  HttpResponseNotFound('<h1>Page not found</h1>')
    except ObjectDoesNotExist:
        if flag == 'des':
            return HttpResponseRedirect(reverse('index_des'))
        else:
            return HttpResponseRedirect(reverse('index_mob'))


# Функция обновления события после сохранения в форме
def update_event(request, flag, event_id, town_id):
    try:
        e = Events.objects.get(pk=event_id)
        t = Town.objects.get(id=town_id)
        if request.POST:
            form = EventsForm(request.POST, instance=e)
            if form.is_valid():
                form.save()
        return HttpResponseRedirect(reverse('events', args=(flag, t.id,)))
    except ObjectDoesNotExist:
        if flag == 'des':
            return HttpResponseRedirect(reverse('index_des'))
        else:
            return HttpResponseRedirect(reverse('index_mob'))


# Функция написанная специально для кнопки назад из обновления в городе
def product_update_town_back (request, flag, region_id, adress_id, product_id, query, town_id):
    try:
        region = Region.objects.get(id=region_id)
        r = Region.objects.get(id=region_id)
        t = Town.objects.get(id=town_id)
        a = Adress.objects.get(id=adress_id)
        p = Product.objects.get(pk=product_id)
        q = query
        color = updateTime()
        args = {}
        args['flag'] = flag
        args['town'] = t
        args['region']= r
        args['adress'] = a
        args['query'] = q
        product_list = Product.objects.filter(adress__town__id=t.id).order_by('product_price').filter(product_name__icontains=q)
        args['list'] = product_list
        args['color'] = color          
        if flag == 'des':
            return render_to_response('pricemin/des/search_town_products_result.html', args)
        elif flag == 'mob':
            return render_to_response('pricemin/mob/search_town_products_result_mob.html', args)
        elif flag == 'pro':
            return render_to_response('pricemin/pro/search_town_products_result_pro.html', args)
        else:
            return  HttpResponseNotFound('<h1>Page not found</h1>')
    except ObjectDoesNotExist:
        if flag == 'des':
            return HttpResponseRedirect(reverse('index_des'))
        else:
            return HttpResponseRedirect(reverse('index_mob'))

#======================================= Search ==============================================

def search_adress_form (request, flag, region_id, town_id):
    try:
        region = Region.objects.get(id=region_id)
        town = Town.objects.get(id=town_id)
        events = Events.objects.filter(town__id=town_id).order_by('-eventDate')[:7]
        args = {}
        args['flag'] = flag
        args['town'] = town
        args['region']= region
        args['events']=events
        if flag == 'des':
            return render_to_response('pricemin/des/search_adress_form.html', args)
        elif flag == 'mob':
            return render_to_response('pricemin/mob/search_adress_form_mob.html', args)
        elif flag == 'pro':
            return render_to_response('pricemin/pro/search_adress_form_pro.html', args)
        else:
            return  HttpResponseNotFound('<h1>Page not found</h1>')
    except ObjectDoesNotExist:
        if flag == 'des':
            return HttpResponseRedirect(reverse('index_des'))
        else:
            return HttpResponseRedirect(reverse('index_mob'))


def search_adress (request, flag, region_id, town_id):
    try:
        region = Region.objects.get(id=region_id)
        town = Town.objects.get(id=town_id)
        events = Events.objects.filter(town__id=town_id).order_by('-eventDate')[:7]
        error = False
        args = {}
        args['flag'] = flag
        args['town'] = town
        args['region']= region
        args['events']=events
        if 'q' in request.GET:
            q = request.GET['q']
            if not q:
                error = True
                args['error'] = error
            else:
                adress_list = Adress.objects.filter(town__id=town_id).filter(adress_name__icontains=q)
                args['adress_list'] = adress_list
                args['query'] = q
                if flag == 'des':
                    return render_to_response('pricemin/des/search_adress_result.html', args)
                elif flag == 'mob':
                    return render_to_response('pricemin/mob/search_adress_result_mob.html', args)
                elif flag == 'pro':
                    return render_to_response('pricemin/pro/search_adress_result_pro.html', args)
                else:
                    return  HttpResponseNotFound('<h1>Page not found</h1>')
        if flag == 'des':
            return render_to_response('pricemin/des/search_adress_form.html', args)
        elif flag == 'mob':
            return render_to_response('pricemin/mob/search_adress_form_mob.html', args)
        elif flag == 'pro':
            return render_to_response('pricemin/pro/search_adress_form_pro.html', args)
        else:
            return  HttpResponseNotFound('<h1>Page not found</h1>')
    except ObjectDoesNotExist:
        if flag == 'des':
            return HttpResponseRedirect(reverse('index_des'))
        else:
            return HttpResponseRedirect(reverse('index_mob'))


def search_product_form (request, flag, region_id, adress_id, town_id):
    try:
        region = Region.objects.get(id=region_id)
        town = Town.objects.get(id=town_id)
        adress= Adress.objects.get(id=adress_id)
        events = Events.objects.filter(town__id=town_id).order_by('-eventDate')[:7]
        args = {}
        args['flag'] = flag
        args['town'] = town
        args['region']= region
        args['adress'] = adress
        args['events']=events
        if flag == 'des':
            return render_to_response('pricemin/des/search_product_form.html', args)
        elif flag == 'mob':
            return render_to_response('pricemin/mob/search_product_form_mob.html', args)
        elif flag == 'pro':
            return render_to_response('pricemin/pro/search_product_form_pro.html', args)
        else:
            return  HttpResponseNotFound('<h1>Page not found</h1>')
    except ObjectDoesNotExist:
        if flag == 'des':
            return HttpResponseRedirect(reverse('index_des'))
        else:
            return HttpResponseRedirect(reverse('index_mob'))


def search_product (request, flag, region_id, adress_id, town_id):
    try:
        region = Region.objects.get(id=region_id)
        town = Town.objects.get(id=town_id)
        adress= Adress.objects.get(id=adress_id)
        events = Events.objects.filter(town__id=town_id).order_by('-eventDate')[:7]
        error = False
        color = updateTime()
        args = {}
        args['flag'] = flag
        args['town'] = town
        args['region']= region
        args['adress'] = adress
        args['events']=events
        if 'q' in request.GET:
            q = request.GET['q']
            if not q:
                error = True
                args['error'] = error
            else:
                products_list = adress.product_set.all().order_by('product_name').filter(product_name__icontains=q)
                args['products_list'] = products_list
                args['query'] = q
                args['color'] = color          
                if flag == 'des':
                    return render_to_response('pricemin/des/search_product_result.html', args)
                elif flag == 'mob':
                    return render_to_response('pricemin/mob/search_product_result_mob.html', args)
                elif flag == 'pro':
                    return render_to_response('pricemin/pro/search_product_result_pro.html', args)
                else:
                    return  HttpResponseNotFound('<h1>Page not found</h1>')
        if flag == 'des':
            return render_to_response('pricemin/des/search_product_form.html', args)
        elif flag == 'mob':
            return render_to_response('pricemin/mob/search_product_form_mob.html', args)
        elif flag == 'pro':
            return render_to_response('pricemin/pro/search_product_form_pro.html', args)
        else:
            return  HttpResponseNotFound('<h1>Page not found</h1>')
    except ObjectDoesNotExist:
        if flag == 'des':
            return HttpResponseRedirect(reverse('index_des'))
        else:
            return HttpResponseRedirect(reverse('index_mob'))


def search_town_form (request, flag, region_id):
    try:
        region = Region.objects.get(id=region_id)
        args = {}
        args['flag'] = flag
        args['region']= region
        args['events']=events
        if flag == 'des':
            return render_to_response('pricemin/des/search_town_form.html', args)
        elif flag == 'mob':
            return render_to_response('pricemin/mob/search_town_form_mob.html', args)
        elif flag == 'pro':
            return render_to_response('pricemin/pro/search_town_form_pro.html', args)
        else:
            return  HttpResponseNotFound('<h1>Page not found</h1>')
    except ObjectDoesNotExist:
        if flag == 'des':
            return HttpResponseRedirect(reverse('index_des'))
        else:
            return HttpResponseRedirect(reverse('index_mob'))


def search_town (request, flag, region_id):
    try:
        region = Region.objects.get(id=region_id)
        error = False
        args = {}
        args['flag'] = flag
        args['region']= region
        if 'q' in request.GET:
            q = request.GET['q']
            if not q:
                error = True
                args['error'] = error
            else:
                town_list = Town.objects.filter(region__id=region_id).order_by('town_name').filter(town_name__icontains=q)
                args['town_list'] = town_list
                args['query'] = q
                if flag == 'des':
                    return render_to_response('pricemin/des/search_town_result.html', args)
                elif flag == 'mob':
                    return render_to_response('pricemin/mob/search_town_result_mob.html', args)
                elif flag == 'pro':
                    return render_to_response('pricemin/pro/search_town_result_pro.html', args)
                else:
                    return  HttpResponseNotFound('<h1>Page not found</h1>')
        if flag == 'des':
            return render_to_response('pricemin/des/search_town_form.html', args)
        elif flag == 'mob':
            return render_to_response('pricemin/mob/search_town_form_mob.html', args)
        elif flag == 'pro':
            return render_to_response('pricemin/pro/search_town_form_pro.html', args)
        else:
            return  HttpResponseNotFound('<h1>Page not found</h1>')
    except ObjectDoesNotExist:
        if flag == 'des':
            return HttpResponseRedirect(reverse('index_des'))
        else:
            return HttpResponseRedirect(reverse('index_mob'))


def search_town_products_form (request, flag, region_id, town_id):
    try:
        region = Region.objects.get(id=region_id)
        town = Town.objects.get(id=town_id)
        events = Events.objects.filter(town__id=town_id).order_by('-eventDate')[:7]
        args = {}
        args['flag'] = flag
        args['town'] = town
        args['region']= region
        args['events']=events
        if flag == 'des':
            return render_to_response('pricemin/des/search_town_products_form.html', args)
        elif flag == 'mob':
            return render_to_response('pricemin/mob/search_town_products_form_mob.html', args)
        elif flag == 'pro':
            return render_to_response('pricemin/pro/search_town_products_form_pro.html', args)
        else:
            return  HttpResponseNotFound('<h1>Page not found</h1>')
    except ObjectDoesNotExist:
        if flag == 'des':
            return HttpResponseRedirect(reverse('index_des'))
        else:
            return HttpResponseRedirect(reverse('index_mob'))


def search_town_products (request, flag, region_id, town_id):
    try:
        region = Region.objects.get(id=region_id)
        town = Town.objects.get(id=town_id)
        events = Events.objects.filter(town__id=town_id).order_by('-eventDate')[:7]
        color = updateTime()
        error = False
        args = {}
        args['flag'] = flag
        args['town'] = town
        args['region']= region
        args['events']=events
        if 'q' in request.GET:
            q = request.GET['q']
            if not q:
                error = True
                args['error'] = error
            else:
                product_list = Product.objects.filter(adress__town__id=town.id).order_by('product_price').filter(product_name__icontains=q)
                args['list'] = product_list
                args['query'] = q  
                args['color'] = color          
                if flag == 'des':
                    return render_to_response('pricemin/des/search_town_products_result.html', args)
                elif flag == 'mob':
                    return render_to_response('pricemin/mob/search_town_products_result_mob.html', args)
                elif flag == 'pro':
                    return render_to_response('pricemin/pro/search_town_products_result_pro.html', args)
                else:
                    return  HttpResponseNotFound('<h1>Page not found</h1>')
        if flag == 'des':
            return render_to_response('pricemin/des/search_town_products_form.html', args)
        elif flag == 'mob':
            return render_to_response('pricemin/mob/search_town_products_form_mob.html', args)
        elif flag == 'pro':
            return render_to_response('pricemin/pro/search_town_products_form_pro.html', args)
        else:
            return  HttpResponseNotFound('<h1>Page not found</h1>')
    except ObjectDoesNotExist:
        if flag == 'des':
            return HttpResponseRedirect(reverse('index_des'))
        else:
            return HttpResponseRedirect(reverse('index_mob'))
            
#==================================== Events ===============================================

def events (request, flag, town_id):
    try:        
        user = auth.get_user(request)
        town = Town.objects.get(id=town_id)
#        events = Events.objects.filter(town__id=town_id)
        events = town.events_set.all().order_by('-eventDate')
        for event in events:
            if event.eventDate < timezone.now() - timezone.timedelta(days=time_delete_event):
                event.delete_obj()
        args = {}
        args['user'] = user
        args['flag'] = flag
        args['town'] = town
        args['events']=events
        if flag == 'des':
            return render_to_response('pricemin/des/events.html', args)
        elif flag == 'mob':
            return render_to_response('pricemin/mob/events_mob.html', args)
        elif flag == 'pro':
            return render_to_response('pricemin/pro/events_pro.html', args)
        else:
            return  HttpResponseNotFound('<h1>Page not found</h1>')
    except ObjectDoesNotExist:
        if flag == 'des':
            return HttpResponseRedirect(reverse('index_des'))
        else:
            return HttpResponseRedirect(reverse('index_mob'))
            

def event (request, flag, event_id, town_id):
    try:
        town = Town.objects.get(id=town_id)
        event = Events.objects.get(id=event_id)
        args = {}
        args['flag'] = flag
        args['town'] = town
        args['event']=event
        if flag == 'des':
            return render_to_response('pricemin/des/event.html', args)
        elif flag == 'mob':
            return render_to_response('pricemin/mob/event_mob.html', args)
        elif flag == 'pro':
            return render_to_response('pricemin/pro/event_pro.html', args)
        else:
            return  HttpResponseNotFound('<h1>Page not found</h1>')
    except ObjectDoesNotExist:
        if flag == 'des':
            return HttpResponseRedirect(reverse('index_des'))
        else:
            return HttpResponseRedirect(reverse('index_mob'))
           
#            ==================== Deactivate========================

def deactivate (request, flag):
    flag = flag
    auth.logout(request)
    if flag == 'des':
        return render_to_response('pricemin/des/deactivate.html') 
    else:
        return render_to_response('pricemin/mob/deactivate_mob.html') 

def incorrect_login (reguest):
        return render_to_response('pricemin/incorrect_login.html') 
