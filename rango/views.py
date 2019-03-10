from django.shortcuts import render
from django.http import HttpResponse
from .models import Category , Page
from .forms import CategoryForm, PageForm
from django.core.urlresolvers import reverse

def index(request):
    categorylist= Category.objects.order_by('-likes')[:5]
    most_viewed_page_list = Page.objects.order_by('-views')[:5]
    context_dic={'categories': categorylist, 'most_viewed_pages': most_viewed_page_list}
    return render(request,'rango/index.html',context=context_dic)

def about(request):
    context_dic = {'author': "Vikas Baghel"}
    return render(request,'rango/about.html', context=context_dic)



def show_category(request, category_name_slug):
    context_dict={}
    try:
        category=Category.objects.get(slug=category_name_slug)
        pages=Page.objects.filter(category=category)
        context_dict['category']=category
        context_dict['pages']=pages
    except Category.DoesNotExit:
        context_dict['category']=None
        context_dict['pages']=None
    return render(request,'rango/category.html',context=context_dict)



def add_category(request):
    form = CategoryForm()
    # A HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        # Have we been provided with a valid form?
        if form.is_valid():
        # Save the new category to the database.
            form.save(commit=True)
            # Now that the category is saved
            # We could give a confirmation message
            # But since the most recent category added is on the index page
            # Then we can direct the user back to the index page.
            return index(request)
        else:
            # The supplied form contained errors -
            # just print them to the terminal.
            print(form.errors)
        # Will handle the bad form, new form, or no form supplied cases.
        # Render the form with error messages (if any).
    return render(request, 'rango/add_category.html', {'form': form})

def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None
    form = PageForm()
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                return show_category(request, category_name_slug)
        else:
             print(form.errors)
    context_dict = {'form':form, 'category': category}
    return render(request, 'rango/add_page.html', context_dict)

# Create your views here.
