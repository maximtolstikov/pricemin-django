
from django.db import models
from django.core.urlresolvers import reverse

PREFIX_TOWN_CHOICES = (
                (u'г.', u'город'), 
		(u'п.', u'поселок'), 
		(u'ст.', u'станция/станица'), 
		(u'д.', u'деревня'), 
		(u'сел.', u'село'),
                (u'хут.', u'хутор'),
                (u'п.г.т', u'пос. гор. типа')
                )
PREFIX_ADRESS_CHOICES = (
                (u'ул.', u'улица'),
		(u'пер.', u'переулок'),
		(u'пр.т', u'проспект'),
		(u'пр.д', u'проезд'),
		(u'шос.', u'шоссе'),
		(u'п.', u'поселок'), 
                )
PREFIX_EVENT_CHOICES = (
		(u'Акция', u'Акция'), 
		(u'Распродажа', u'Распродажа'), 
		(u'Ликвидация', u'Ликвидация'), 
		(u'Открытие', u'Открытие'), 
		(u'', u'---------'),
		               )


# Create your models here.
class Country(models.Model):
    country_name = models.CharField(max_length=20)
    def __str__(self):
        return self.country_name

class Region(models.Model):
    region_name = models.CharField(max_length=50)
    country = models.ForeignKey(Country)
    def __str__(self):
        return self.region_name

class Town(models.Model):
    user_id = models.CharField(max_length=10, default='1')
    town_name = models.CharField(max_length=50, verbose_name=u'Название')
    prefix = models.CharField(max_length=4, choices = PREFIX_TOWN_CHOICES, verbose_name=u'Префикс' )
    region = models.ForeignKey(Region)
    town_date = models.DateTimeField(auto_now=True, null=True)
    def __str__(self):
        return self.town_name

    def delete_obj(self):
        return self.delete()

    class Meta:
        unique_together = ('prefix', 'town_name', 'region')

class Adress(models.Model):
    user_id = models.CharField(max_length=10, default='1')
    adress_name = models.CharField(max_length=40, verbose_name=u'Магазин')
    number = models.CharField(max_length=5, verbose_name=u'Номер дома')
    street = models.CharField(max_length=30, verbose_name=u'Название улицы')
    prefix = models.CharField(max_length=7, choices = PREFIX_ADRESS_CHOICES, verbose_name=u'Префикс')
    town = models.ForeignKey(Town)
    adress_date = models.DateTimeField(auto_now=True, null=True)
    def __str__(self):
        s1 = self.adress_name
        s2 = self.prefix
        s3 = self.street
        s4 = self.number
        s5 = "'"+s1+"'"+" "+s2+" "+s3+","+" "+s4
        return s5

    def delete_obj(self):
        return self.delete()

    class Meta:
        unique_together = ('number', 'street', 'adress_name')

class Product(models.Model):
    user_id = models.CharField(max_length=10, default='1')
    product_name = models.CharField(max_length=100, verbose_name=u'Название')
    product_weight = models.IntegerField(verbose_name=u'грамм(мл.)')
    product_price = models.FloatField( verbose_name=u'Цена, рублей')
    adress = models.ForeignKey(Adress)
    product_date = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.product_name

    def delete_obj(self):
        return self.delete()

class Events(models.Model):
    user_id = models.CharField(max_length=10, default='1')
    prefix = models.CharField(max_length=20, choices=PREFIX_EVENT_CHOICES, verbose_name=u'Событие', blank=True)
    eventWhere = models.CharField(max_length=100)
    eventStart = models.CharField(max_length=100, blank=True)
    eventStop = models.CharField(max_length=100, blank=True)
    eventComment = models.TextField(max_length=2000, blank=True)
    town = models.ForeignKey(Town)
    eventDate = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.eventWhere
    def delete_obj(self):
        return self.delete()
