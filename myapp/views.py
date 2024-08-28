from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from .models import *
from .serializers import transaction_serializer,UserSerializer
from rest_framework.response import Response
from django.http import JsonResponse



class transaction_view(APIView):
    def get(self,request):
        objs=Transaction.objects.all()
        serializer=transaction_serializer(objs,many=True)
       
        data=[serializer.data]
        return Response(data)
    
    def post(self,request):
        serializer=transaction_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)    

        else:
            return Response(serializer.errors)
        



class user_detail(APIView):
    def get(self,request,pk=None):
        if pk!=None:
            user=User.objects.get(id=pk)
            serializer=UserSerializer(user)
            return Response(serializer.data)
        users=User.objects.all()
        serializers=UserSerializer(users,many=True)
        return Response(serializers.data)




# scheduler for updating s3 csv

import csv
import io
import boto3
from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse

def upload_user_data_to_s3(request):
    # Fetch user data
    users = User.objects.all()

    # Prepare CSV data
    csv_data = [['Username', 'Email']]
    for user in users:
        csv_data.append([user.username, user.email])



    # Write CSV data to a string
    csv_buffer = io.StringIO()
    csv_writer = csv.writer(csv_buffer)
    csv_writer.writerows(csv_data)
    
    # Upload CSV data to S3
    s3 = boto3.client(
            "s3",
            aws_access_key_id="ACCESS_KEY",
            aws_secret_access_key="SECRET_ACCESS_KEY"
        )
    bucket_name = 'beckendtest'
    s3_key = 'user_data.csv'

    s3.put_object(
        Bucket=bucket_name,
        Key=s3_key,
        Body=csv_buffer.getvalue(),
        ContentType='text/csv'
    )

    return HttpResponse('User data uploaded to S3 successfully.')





class  index(APIView):
    def get(self,request):
        data=[
            {"urls":{
                "for user datails":"http://127.0.0.1:8000/users/7",
                "for transaction":"http://127.0.0.1:8000/transaction"
            }},
        {"distribute in equal":
            {
                    "paid_by": 7,
                    "transaction_name": "Bill paid",
                    "amount": 1500,
                    "distribute": 1,
                    "owees": []
                }
        },
        {  "distibute in exact":
            {
                        "paid_by": 8,
                        "transaction_name": "flipkart Shopping",
                        "amount": 550,
                        "distribute": 2,
                        "owees": [{"user":7,"amount":400},{"user":9,"amount":150}]
                    }},
                    {"distribute in percentage":    {
                        "paid_by": 7,
                        "transaction_name": "distribute in percantage",
                        "amount": 800,
                        "distribute": 3,
                        "owees": [{"user":9,"amount":40},{"user":10,"amount":20}]
                    }}
            ]

        return Response(data)
