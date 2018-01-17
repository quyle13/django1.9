from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from rango.models import Category
from rango.models import Page


def index(request):
    #descending order - likes
    #:5 dice array
    context_dict = {}
    category_list = Category.objects.order_by('-likes')[:5]
    top_page = Page.objects.order_by('-views')[:5]

    context_dict['categories'] = category_list
    context_dict['pages'] = top_page
    return render(request,'rango/index.html',context_dict)
def about(request):
    return render(request,'rango/about.html')

def show_category(request,category_name_slug):
    context_dict = {}
    try:
        category = Category.objects.get(slug=category_name_slug)

        #get all the pages of the category
        pages = Page.objects.filter(category = category)
        context_dict['pages'] = pages
        context_dict['category'] = category


    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['pages'] = None
    return render(request,'rango/category.html',context_dict)


