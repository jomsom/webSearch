#from django.shortcuts import render

from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response, render
from .models import Category, Page
from websearch.forms import CategoryForm, UserForm, UserProfileForm

def index(request): #request is HttpRequest object

    context = RequestContext(request)
    print('*************', context, '*************')
    print('*************', request, '*************')
    #context_dict = {'boldmessage': "I am bold font from the context"}
    category_list = Category.objects.order_by('-likes')[:10]
    context_dict = {'categories': category_list} # categories is django variable in index
    
    
    # The following two lines are new.
    # We loop through each category returned, and create a URL attribute.
    # This attribute stores an encoded URL (e.g. spaces replaced with underscores).

    for category in category_list:
        category.url = category.name.replace(' ', '_')
    #return HttpResponse("Websearch says hello world!") #without template
    #when respond to client's request, sends context_dict and context back to client
    #where client side,( templates ) can use information in the dictionary. The dictionaly
    # key word is template variable.
    return render_to_response('websearch/index.html', context_dict, context)
    
def about(request):
    print('request: *************', request, '*************')
    context = RequestContext(request)
    return render_to_response('websearch/about.html', context)
    #OR    
    #return render(request, 'websearch/about.html',{'question':'hello'})
    
def category(request, category_name_url):
    context = RequestContext(request) # Request our context from the request passed to us.

    # Change underscores in the category name to spaces.
    # URLs don't handle spaces well, so we encode them as underscores.
    # We can then simply replace the underscores with spaces again to get the name.

    category_name = category_name_url.replace('_', ' ')
    
    # Create a context dictionary which we can pass to the template rendering engine.
    # We start by containing the name of the category passed by the user.

    context_dict = {'category_name': category_name}
    try:
        category = Category.objects.get(name=category_name)
        pages = Page.objects.filter(category=category)
        context_dict['pages'] = pages
        context_dict['category']= category
    except Category.DoesNotExist:
        pass
    return render_to_response('websearch/category.html', context_dict, context)
    
def add_category(request):
    context = RequestContext(request)
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save(commit = True)
            return index(request)
        else:
            print (form.errors)
    else:
        form = CategoryForm()
    return render_to_response('websearch/add_category.html', {'form': form}, context)

def register(request):
    context = RequestContext(request)
    registered =False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
                
            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    
    return render_to_response('websearch/register.html',
            {'user_form': user_form, 'profile_form' : profile_form, 'registered': registered},
            context)
            
def user_login(request):
    context = RequestContext(request)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
    
    return render_to_response('websearch/index.html')