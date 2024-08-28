from rest_framework import serializers
from .models import *
from django.http import HttpResponse
class owee_serializer(serializers.ModelSerializer):
    class Meta:
        model=owee
        fields='__all__'

class transaction_serializer(serializers.ModelSerializer):
    transaction_owee=owee_serializer(many=True,read_only=True)
    distribute_display_value = serializers.CharField(source='get_distribute_display',read_only=True)
    owees = serializers.ListField(allow_empty=True,write_only=True)
    class Meta:
        model=Transaction
        fields ='__all__'
    def create(self,validated_data): 
        transaction=Transaction.objects.create(paid_by=validated_data['paid_by'],transaction_name=validated_data['transaction_name'],amount=validated_data['amount'],distribute=validated_data['distribute'])
        parameter=validated_data['distribute']
        amount=validated_data['amount']

        match parameter:
   
            case 1  :
                # distribute expenses equally to users
                owee_amount=amount/User.objects.all().count()
                paid_by_user=validated_data['paid_by']  

                total_users=User.objects.all().exclude(id=paid_by_user.id)

                for user in total_users:
                    print(user)
                    owee_obj=owee.objects.create(transaction=transaction,amount=owee_amount,user=user)
  
                    
            case 2 : 
                #  distribute expenses exactly to user
                print("it is distribute method")
                owee_list=validated_data['owees']
                for owee_item in owee_list:
                    try:
                        owee_obj=owee.objects.create(transaction=transaction,amount=owee_item['amount'],user_id=owee_item['user'])
                    except Exception as e:
                        print(e)
                        return HttpResponse(e)
                    print(owee_obj,'owee_obj')
            case 3 : 
                owee_list=validated_data['owees']
                total_percent=sum([i['amount'] for i in owee_list])
                if total_percent<=100:
                    for owee_item in owee_list:
                        try:
                            percentage_amount=(amount*owee_item['amount'])/100
                            owee_obj=owee.objects.create(transaction=transaction,amount=percentage_amount,user_id=owee_item['user'])
                        except Exception as e:
                            print(e)
                            return HttpResponse(e)
                else:
                    return HttpResponse('Wrong percentage')
        
            case _  : 
                pass

        return transaction
    
class profile_serializer(serializers.ModelSerializer):
    class Meta:
        model=Profile
        fields='__all__'


from django.db.models import Sum
from django.contrib.auth.models import User
class UserSerializer(serializers.ModelSerializer):
    profile=profile_serializer()
    # creditors=owee_serializer(many=True,read_only=True)
    summary_creditors=serializers.SerializerMethodField()
    summary_debtors=serializers.SerializerMethodField()
    transactions=transaction_serializer(many=True,read_only=True)
    class Meta:
        model=User
        fields=['first_name','last_name','username','profile','summary_creditors','summary_debtors','transactions']
    def get_summary_creditors(self,obj):
        user_amounts = owee.objects.filter(user=obj).values('transaction__paid_by__username').annotate(total_amount=Sum('amount'))
        return user_amounts
    def get_summary_debtors(self,obj):
        debtors=owee.objects.filter(transaction__paid_by=obj).values('user__username').annotate(total_amount=Sum('amount'))
        return debtors

# distribute in equal
    '''
    {
            "paid_by": 7,
            "transaction_name": "Bill paid",
            "amount": 1500,
            "distribute": 1,
            "owees": []
        }

'''
# distibute in exact
    '''
{
            "paid_by": 8,
            "transaction_name": "flipkart Shopping",
            "amount": 550,
            "distribute": 2,
            "owees": [{"user":7,"amount":400},{"user":9,"amount":150}]
        }
'''
# distribute in percentage
'''
{
            "paid_by": 7,
            "transaction_name": "distribute in percantage",
            "amount": 800,
            "distribute": 3,
            "owees": [{"user":9,"amount":40},{"user":10,"amount":20}]
        }
'''
