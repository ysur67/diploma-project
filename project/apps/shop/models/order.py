from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from apps.catalog.models import Product
from django.conf import settings
from dadata import Dadata
from geopy import distance
from decimal import Decimal
from apps.main.models import SiteSettings


class OrderMixin(models.Model):
    class Meta:
        abstract = True

    id = models.CharField(
        max_length=20,
        verbose_name='Идентификатор',
        primary_key=True,
    )
    title = models.CharField(
        max_length=200,
        verbose_name='Наименование типа доставки'
    )
    active = models.BooleanField(
        default=False,
        verbose_name='Активность'
    )

    def __str__(self):
        return self.title


class ShippingType(OrderMixin):
    class Meta:
        verbose_name = 'Вариант доставки'
        verbose_name_plural = 'Варианты доставки'

    is_calculated = models.BooleanField(verbose_name="Расчитывать доставку?", default=True)
    km_multiplier = models.DecimalField(verbose_name="руб/км", default=0, decimal_places=2, max_digits=6)
    min_price = models.DecimalField(verbose_name='Минимальная стоимость заказа', default=0, decimal_places=2, max_digits=10)

    def count_shipping_price(self, distance):
        return round(Decimal(distance) * self.km_multiplier, 2)

    def calculate_shipping(self, address):
        site_settings = SiteSettings.objects.first()
        shop_address_code_lat = site_settings.address_code_lat
        shop_address_code_lon = site_settings.address_code_lon
        shop_address_code = (shop_address_code_lat, shop_address_code_lon)
        request_addres_code = ShippingType.get_address_code(address)
        distance = self.calculate_distance(request_addres_code, shop_address_code)
        return self.count_shipping_price(distance)

    def count_to_door_shipping(self, order_price):
        TO_DOOR_MULTIPLIER = 0.1
        return round(order_price * TO_DOOR_MULTIPLIER, 2)

    @classmethod
    def get_suggestions(cls, address):
        token = settings.DADATA_TOKEN
        dadata = Dadata(token)
        return dadata.suggest('address', address)

    @classmethod
    def get_address_code(cls, address):
        token = settings.DADATA_TOKEN
        secret = settings.DADATA_SECRET_KEY
        dadata = Dadata(token, secret)
        data = dadata.clean("address", address)
        result = (data.get('geo_lat'), data.get('geo_lon'))
        return result

    @classmethod
    def calculate_distance(cls, address1, address2):
        return distance.distance(address1, address2).km


class OrderStatus(OrderMixin):
    class Meta:
        verbose_name = 'Статус заказа'
        verbose_name_plural = 'Статусы заказов'

    color = models.CharField(verbose_name="Цвет", max_length=100, default='')

    @classmethod
    def get_first(cls):
        status_exists = cls.objects.first()
        if status_exists:
            return cls.objects.first().id
        else:
            DEFAULT_STATUS = cls.objects.create(
                id='WIP',
                title='В обработке',
                active=True,
            )
            return DEFAULT_STATUS.id


class PaymentType(OrderMixin):
    class Meta:
        verbose_name = 'Способ оплаты'
        verbose_name_plural = 'Способы оплаты'


class Order(models.Model):
    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='orders',
        null=True,
        blank=True,
        verbose_name='Пользователь'
    )
    full_name = models.CharField(
        max_length=300,
        verbose_name='ФИО покупателя',
        default='no data'
    )
    phone = models.CharField(
        max_length=20,
        verbose_name='Телефон покупателя',
        default='no data'
    )
    email = models.CharField(
        max_length=50,
        verbose_name='Электронная почта покупателя',
        default='no data'
    )
    shipping_type = models.ForeignKey(
        ShippingType,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name='Тип доставки'
    )
    order_status = models.ForeignKey(
        OrderStatus,
        on_delete=models.SET_DEFAULT,
        default=OrderStatus.get_first,
        verbose_name='Статус заказа'
    )
    payment_type = models.ForeignKey(
        PaymentType,
        on_delete=models.SET_NULL,
        verbose_name='Способ оплаты',
        null=True,
        blank=True,
    )
    city = models.CharField(
        max_length=150,
        null=True,
        blank=True,
    )
    street = models.CharField(
        max_length=200,
        null=True,
        blank=True,
    )
    building = models.CharField(
        max_length=10,
        null=True,
        blank=True,
    )
    appartment = models.CharField(
        max_length=20,
        verbose_name='Квартира/Офис',
        null=True,
        blank=True,
    )
    date = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата заказа'
    )
    total_price = models.FloatField(
        validators=[
            MinValueValidator(0.0)
        ],
        verbose_name='Полная стоимость заказа'
    )
    comment = models.TextField(
        null=True, 
        blank=True,
        verbose_name='Комментарий к заказу'
    )
    is_paid = models.BooleanField(
        verbose_name="Заказ был оплачен",
        default=False
    )
    shipping_price = models.FloatField(
        validators=[
            MinValueValidator(0.0)
        ],
        verbose_name='Стоимость доставки',
        default=0
    )
    full_address = models.CharField(
        verbose_name='Адрес доставки',
        null=True,
        blank=True,
        max_length=200
    )

    def __str__(self):
        return f'{str(self.full_name)} {self.city}'

    def is_shipping_default(self):
        return self.shipping_type.id == 'SELF'


class OrderItem(models.Model):

    class Meta:
        verbose_name = 'Заказной товар'
        verbose_name_plural = 'Заказные товары'

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='order_items'
    )
    amount = models.PositiveIntegerField(
        default=1
    )
    product_price = models.FloatField(
        validators=[
            MinValueValidator(0.0)
        ],
        help_text='Цена товара на момент заказа'
    )
    total = models.FloatField(
        MinValueValidator(0.0),
        help_text='Стоимость товара * кол-во товара'
    )

    def __str__(self):
        return f'{str(self.order)} {str(self.product)}'
