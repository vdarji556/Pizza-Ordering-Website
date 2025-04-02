from django.db import models
from django.contrib.auth.models import User
import uuid
from django.db.models import Sum
class BaseModel(models.Model):
    uid = models.UUIDField(default=uuid.uuid4,editable=True,primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class PizzaCategory(BaseModel):
    category_name = models.CharField(max_length=100)

class Pizza(BaseModel):
    category = models.ForeignKey(PizzaCategory, on_delete = models.CASCADE,related_name ="category" )
    pizza_name = models.CharField(max_length=100)
    price = models.IntegerField(default=100)
    image = models.ImageField(upload_to='pizza')

class Cart(BaseModel):
    user = models.ForeignKey(User, null=True,blank=True,on_delete=models.SET_NULL , related_name="cart")
    is_paid = models.BooleanField(default=False)

    # def get_cart_total(self):
    #     return CartItems.objects.filter(cart=self).aggregate(Sum('pizza__price'))['pizza__price__sum']

    def get_cart_total(self):
        return sum(item.total_price() for item in self.cartitems.all())

class CartItems(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE,related_name="cartitems")
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)  

    def total_price(self):
        return self.pizza.price * self.quantity  #

