from django.contrib import admin
from portal_app.models import*

admin.site.register([UserModel,StudentModel,ResultModel,FeeModel,FeePaymentModel])
