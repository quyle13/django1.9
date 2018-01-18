from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from rango.models import Category
from rango.models import Page
from rango.forms import CategoryForm,PageForm
from rango.forms import UserForm,UserProfileForm
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required




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
    print (request.method)
    print (request.user)
    return render(request,'rango/about.html',{})

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

@login_required
def add_category(request):
    form = CategoryForm()

    if request.method =='POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            #redirect to home page
            return index(request)
        else:
            print(form.errors)
    return render(request,'rango/add_category.html',{'form':form})

@login_required
def add_page(request,category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)

    except Category.DoesNotExist:
        category = None

    form = PageForm()
    if request.method =='POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if category:
                page = form.save(commit = False)
                page.category = category
                page.views = 0
                page.save()
                #return show category page
                return show_category(request,category_name_slug)
        else:
            print (form.errors)
    context_dict = {'form':form,'category':category}
    return render(request,'rango/add_page.html',context_dict)

def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data = request.POST)
        profile_form = UserProfileForm(data = request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            #hash the password with the set_password method
            user.set_password(user.password)
            user.save()


            profile = profile_form.save(commit = False)
            # link 2 forms together
            profile.user = user

            #check if there is picture
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()

            registered = True
        else:
            print (user_form.errors,profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render(request,'rango/register.html',{'user_form':user_form,'profile_form':profile_form,'registered':registered})


def user_login(request):

    if request.method == 'POST':
        print ('not here')
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username = username,password = password)
        if user:
            if user.is_active:
                #if the account is valid and active, w can log user in
                login(request,user)
                #reverse to obtain URL of the Rango application
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:
            print ("Invalid login details:{0},{1}".format(username,password))
            return HttpResponse("Invalid login details supplied.")
    else:
        print ('inside user login - method GET')
        return render(request,'rango/login.html',{})

@login_required
def restricted(request):
    return render(request,'rango/restricted.html',{})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))
