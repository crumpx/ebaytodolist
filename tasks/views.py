# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import auth, messages
from django.template.context import RequestContext
#from django.forms.formsets import formset_factory

from django.contrib.auth.decorators import login_required
from .forms import *
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import *
import datetime
# Create your views here.


def login(request):
    form = LoginForm(request.POST)
    if form.is_valid():
        username = request.POST.get('username','')
        password = request.POST.get('password','')
        user = auth.authenticate(username = username,
               password = password)
        if user is not None and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect('/tasklist/')
        else:
            return render_to_response('login.html', \
                   RequestContext(request,{'form':form, \
                                  'password_is_wrong':True}))
    else:
        return render_to_response('login.html',RequestContext(request, \
                                   {'form':form,}))

def index(request):
    html = "<html><body>hello!</body></html>"
    return HttpResponse(html)

@login_required  
def logout(request):  
    auth.logout(request)  
    return HttpResponseRedirect("/accounts/login/")  


@login_required
def tasklist(request,param=None):
    try:
        lines = Task.objects.filter(buyer = request.GET['search'] )
    except:
        if request.path == '/tasklist/open/':
            lines = Task.objects.filter(status = 'O' )
        elif request.path =="/tasklist/closed/":
            lines = Task.objects.filter(status = 'C' )
        else:

            lines = Task.objects.order_by('-id')

    paginator = Paginator(lines,20)
    page = request.GET.get('page')
    try:
        show_lines = paginator.page(page)
    except PageNotAnInteger:
        show_lines = paginator.page(1)
    except EmptyPage:
        show_lines = paginator.page(paginator.num_pages)

    return render_to_response('tasklist.html',RequestContext(request,{'lines': show_lines}))

@login_required
def taskdetial(request, param=None):
    username = request.user.username

    if request.method =='GET':

        try:
            if request.GET.get('delete'):
                Task.objects.filter(id=param).delete()
                return HttpResponseRedirect('/tasklist/')
        except:
            pass

        if param != None:
            task = Task.objects.get(id=param)
            form = TaskForm(initial={'creator': task.creator, \
                             'tasktype':task.tasktype, \
                             'product':task.product, \
                             'seller': task.seller, \
                             'buyer': task.buyer, \
                             'buyername': task.buyername.title(), \
                             'buyeremail': task.buyeremail, \
                             'address': task.address.title(), \
                             'tracking': task.tracking, \
                             'status': task.status, \
                             'comment':task.comment, \
                             'lastupdatedtime': datetime.datetime.now(),})
            return render_to_response('taskdetial.html',RequestContext(request,{'form':form,}))
        else:
            form = TaskForm(initial={'creator':User.objects.get(username=username)})
            return render_to_response('taskdetial.html',RequestContext(request,{'form':form,}))
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            if param != None:
       	        task = Task.objects.get(id=param)
                tracking = form.cleaned_data['tracking']
                if len(tracking) > 22:
                    tracking=tracking[len(tracking)-22:]
                task.tasktype = form.cleaned_data['tasktype']
                task.product = form.cleaned_data['product']
                task.seller = form.cleaned_data['seller']
                task.buyer = form.cleaned_data['buyer']
                task.buyername= form.cleaned_data['buyername'].title()
                task.buyeremail= form.cleaned_data['buyeremail']
                task.address = form.cleaned_data['address'].title()
                task.tracking = tracking
                task.status = form.cleaned_data['status']
                task.comment = form.cleaned_data['comment']
                task.lastupdatedtime = datetime.datetime.now()
                task.save()
                if form.cleaned_data['sendmail']:
                    from django.core.mail import send_mail
                    subject = 'Your replacement shipped from %s' % form.cleaned_data['seller']
                    msg='Dear %s,\n\nYour replacement for\n\n' \
                        '%s\n\n is being shipped.\n\n' \
                        'The new tracking number for this package is: \n\n%s\n\n' \
                        'please use ebay message if you need any futher assistance.\n\n' \
                        'This mail box is not being monitored. Do not directly reply to this email address.\n' \
                        '' % (form.cleaned_data['buyername'].title(),form.cleaned_data['product'], tracking)
                    try:
                        if send_mail(subject, msg, \
                                     'noreply@goldantay.com', \
                                     [form.cleaned_data['buyeremail']], \
                                     fail_silently=False,  \
                                     html_message=True):
                            return HttpResponseRedirect('/tasklist/')
                    except ValueError as error:
                        return HttpResponse('发送失败！%s',(error))
                else:
                    return HttpResponseRedirect('/tasklist/')

            else:
                tracking = form.cleaned_data['tracking']
                if len(tracking) > 22:
                    tracking=tracking[len(tracking)-22:]
                task = Task.objects.create(
                    creator = User.objects.get(username=username),
                    tasktype = (form.cleaned_data['tasktype']),
                    product = form.cleaned_data['product'],
                    seller = form.cleaned_data['seller'],
                    buyer = form.cleaned_data['buyer'],
                    buyername = form.cleaned_data['buyername'].title(),
                    buyeremail = form.cleaned_data['buyeremail'],
                    address = form.cleaned_data['address'].title(),
                    tracking = tracking,
                    status = form.cleaned_data['status'],
                    comment = form.cleaned_data['comment'],
                    createtime=datetime.datetime.now(),
                    lastupdatedtime = datetime.datetime.now()
                    )
                task.save()
                return HttpResponseRedirect('/tasklist/')
        return render_to_response('taskdetial.html',RequestContext(request,{'form':form,}))

#def send_email_to_buyer(request,buyeremail):
#    print 'hello~~~', buyeremail
