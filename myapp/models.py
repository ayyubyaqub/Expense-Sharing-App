from django.db import models

# Create your models here.
from django.contrib.auth.models import User
# User: Each user should have a userId, name, email, mobile number.
class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile')
    mobile=models.BigIntegerField() 

#  EQUAL, EXACT or PERCENT
ditribution_method=[(1,'equal'),(2,'exact'),(3,'percent')]    
class Transaction(models.Model):
    paid_by=models.ForeignKey(User,on_delete=models.CASCADE,related_name='transactions')
    transaction_name=models.CharField(max_length=254,null=True,blank=True)
    amount=models.IntegerField()
    distribute=models.IntegerField(choices=ditribution_method,default=1)
    created_at=models.DateTimeField(auto_now_add=True,null=True,blank=True)

class owee(models.Model):
    transaction=models.ForeignKey(Transaction,on_delete=models.CASCADE,related_name='transaction_owee')
    amount=models.IntegerField()
    user=models.ForeignKey(User,on_delete=models.PROTECT,related_name='creditors')
