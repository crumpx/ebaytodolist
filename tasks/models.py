# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

TASKTYPE=(('R','重寄'),('D','寄錯重寄'),('M','改地址'),('S','特殊要求'),('O','加急'),('T','退款'))
STATUS=(('O','开启'),('C','关闭'),('P','正在处理'),('H','等待'))

class Task(models.Model):
    id = models.AutoField(primary_key=True)
    creator = models.ForeignKey(User) 
    tasktype = models.CharField(max_length=1, choices=TASKTYPE)
    product = models.CharField(max_length=200, blank=True, null=True)
    seller = models.CharField(max_length=200, blank=True, null=True)
    buyer = models.CharField(max_length=200, blank=True, null=True)
    buyername= models.CharField(max_length=200, blank=True, null=True)
    buyeremail = models.CharField(max_length=200, blank=True, null=True)
    address = models.CharField(max_length=2000, blank=True, null=False)
    tracking = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=1, choices=STATUS) 
    createtime = models.DateTimeField()
    lastupdatedtime = models.DateTimeField(blank=True, null=True)
    comment = models.CharField(max_length=2000, blank=True, null=True)
    def __unicode__(self):
        return str(self.id)

    def taskdisplay(self):
        return str(self.get_tasktype_display())

    def statusdisplay(self):
        return str(self.get_status_display())
