import datetime

from cities_light.models import Country
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.text import slugify

# Create your models here.

User = settings.AUTH_USER_MODEL

class SlugMixin(models.Model):
    slug = models.SlugField(max_length=200, unique=True, blank=True)

    class Meta:
        abstract = True

    def generate_unique_slug(self, base_value):
        base_slug = slugify(base_value)
        slug = base_slug
        counter = 1
        while self.__class__.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        return slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug(self.name)

        super().save(*args, **kwargs)

class Category(SlugMixin):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='categories/', null=True, blank=True)

    def __str__(self):
        return self.name



class SubCategory(SlugMixin):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='sub-categories/', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name


class Seller(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="sellers/", null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Product(SlugMixin):
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=100, blank=True, null=True)
    details = models.TextField(blank=True, null=True)
    price = models.FloatField()
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.PositiveIntegerField(default=0)
    delivery = models.CharField(max_length=100, blank=True, null=True)
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    views = models.PositiveIntegerField(default=0)
    rating = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(5)], default=0)
    guarantee = models.CharField(max_length=50, blank=True, null=True)

    sub_category = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True)
    seller = models.ForeignKey(Seller, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


    @property
    def get_main_media(self):
        medias = self.media_set.all()
        if medias.exists():
            media = medias.filter(main=True).first()
            return media
        return None

    @property
    def rating_percentage(self):
        return round(self.rating / 5 * 100, 2)

    @property
    def get_discount(self):
        discounts = self.discount_set.filter(end_date__gte=datetime.date.today()).order_by('-id')
        if discounts.exists():
            return discounts.first()
        return None

    @property
    def final_price(self):
        discount = self.get_discount
        return discount.new_price if discount else self.price

class Media(models.Model):
    image = models.ImageField(upload_to='media-products/')
    main = models.BooleanField(default=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f'Media of {self.product.name}'


class Property(models.Model):
    name = models.CharField(max_length=100)
    value = models.TextField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Choice(models.Model):
    name = models.CharField(max_length=100)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Variant(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='variants/', blank=True, null=True)
    delta_price = models.FloatField(default=0)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    @property
    def get_next_price(self):
        return self.choice.product.final_price + self.delta_price

    def __str__(self):
        return self.name


class Discount(models.Model):
    percentage = models.FloatField(blank=True, null=True)
    dis_price = models.FloatField(blank=True, null=True)
    new_price = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    end_date = models.DateField(blank=True, null=True)

    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product.name} - {self.percentage}% discount"

    def save(self, *args, **kwargs):
        price = self.product.price
        if self.percentage:
            self.new_price = price * (100 - self.percentage) / 100
            self.dis_price = price - self.new_price
        elif self.dis_price:
            self.new_price = price - self.dis_price
            self.percentage = 100 - (self.new_price * 100 / price)
        elif self.new_price:
            self.percentage = 100 - (self.new_price * 100 / price)
            self.dis_price = price - self.new_price
        else:
            self.end_date = datetime.date.today()
        super().save(*args, **kwargs)


class Review(models.Model):
    text = models.TextField()
    rate = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], default=5)
    created_at = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user.username} - {self.text}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        avg_rate = self.product.review_set.aggregate(models.Avg('rate'))['rate__avg'] or 0
        self.product.rating = round(avg_rate, 2)
        self.product.save(update_fields=['rating'])


class AdBanner(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='adverts/')
    url = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=False)
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.title
