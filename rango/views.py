from django.shortcuts import render
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm
from rango.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from datetime import datetime
from registration.backends.simple.views import RegistrationView

from utils import log


def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val


def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request, 'visits', 1))
    last_visit_cookie = get_server_side_cookie(request,
                                               'last_visit',
                                               str(datetime.now()))
    # last_visit_cookie[:-7] 切片操作用来去掉小数点后面的毫秒数
    last_visit_time = datetime.strptime(last_visit_cookie[:-7],
                                        '%Y-%m-%d %H:%M:%S')
    if (datetime.now() - last_visit_time).seconds > 5:
        visits += 1
        request.session['last_visit'] = str(datetime.now())
    else:
        request.session['last_visit'] = last_visit_cookie
    request.session['visits'] = visits


def index(request):
    # Query the database for a list of ALL categories currently stored.
    # Order the categories by no. likes in descending order.
    # Retrieve the top 5 only - or all if less than 5.
    # Place the list in our context_dict dictionary
    # that will be passed to the template engine.

    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    context_dict = {'categories': category_list,
                    'pages': page_list, }

    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']

    response = render(request, 'rango/index.html', context=context_dict)
    return response


def about(request):
    context_dict = {'boldmessage': 'linmu'}
    return render(request, 'rango/about.html', context=context_dict)


def show_category(request, category_name_slug):
    # Create a context dictionary which we can pass
    # to the template rendering engine.
    context_dict = {}

    try:
        # Can we find a category name slug with the given name?
        # If we can't, the get() method raises a DoesNotExist exception.
        # So the get() method returns one model instance or raises an exception.
        category = Category.objects.get(slug=category_name_slug)

        # Retrieve all of the associated pages.
        # Note that filter() will return a list of page objects or an empty list.
        pages = Page.objects.filter(category=category)

        # Adds our results list to the template context under name pages.
        context_dict['pages'] = pages
        # We also add the category object from
        # the database to the context dictionary
        # we'll use this in the template to verify that the category exists.
        context_dict['category'] = category
    except Category.DoesNotExist:
        # We  get hera if we didn't find the specified category.
        # Don't do anything
        # the template  will display the 'no category' message for us.
        context_dict['category'] = None
        context_dict['pages'] = None

    return render(request, 'rango/category.html', context_dict)


@login_required
def add_category(request):
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database
            cat = form.save(commit=True)
            log(cat, cat.slug)
            # Now that the category is saved
            # We could give a confirmation message
            # But since the most recent category added is on the index page
            # Then we can direct the user back to the index page.
            return redirect(reverse('index'))
        else:
            # The supplied form contained errors
            # Just print them to the terminal
            print(form.errors)
    # Will handle the bad form, or no form supplied cases.
    # Render the form with error messages (if any)
    return render(request, 'rango/add_category.html', {'form': form})


@login_required
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
                page.save()
            return redirect(reverse('show_category', args=[category_name_slug]))
        else:
            log(form.errors)

    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context_dict)


class MyRegistrationView(RegistrationView):
    def get_success_url(self, user):
        return reverse('index')


def test(request):
    return render(request, 'jinja_test/test.html', context={})


# def register(request):
#     registered = False
#
#     if request.method == 'POST':
#         user_form = UserForm(data=request.POST)
#         profile_form = UserProfileForm(data=request.POST)
#
#         # If the two forms are valid...
#         if user_form.is_valid() and profile_form.is_valid():
#             user = user_form.save()
#
#             # Now we hash the password with the set_password method.
#             # Once hashed, we can update the user object.
#             user.set_password(user.password)
#             user.save()
#
#             profile = profile_form.save(commit=False)
#             profile.user = user
#
#             if 'picture' in request.FILES:
#                 profile.picture = request.FILES['picture']
#
#             profile.save()
#
#             registered = True
#         else:
#             log(user_form.errors, profile_form.errors)
#     else:
#         user_form = UserForm()
#         profile_form = UserProfileForm()
#
#     context_dict = {
#         'user_form': user_form,
#         'profile_form': profile_form,
#         'registered': registered,
#     }
#     return render(request, 'accounts/register.html', context_dict)
#
#
# def user_login(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         next = request.POST.get('next')
#
#         # Use Django's machinery to attempt to see if the username/password
#         # combination is valid - a User object is returned if it is.
#         user = authenticate(username=username, password=password)
#         if user:
#             if user.is_active:
#                 login(request, user)
#                 if next:
#                     return redirect(next)
#                 else:
#                     return redirect(reverse('index'))
#             else:
#                 return HttpResponse('Your Rango account is disabled.')
#         else:
#             log('Invalid login deails: {0}, {1}'.format(username, password))
#             return render(request, 'rango/404.html', {})
#
#     else:
#         next = request.GET.get('next')
#         return render(request, 'registration/login.html', {'next': next})
#
#
# @login_required
# def user_logout(request):
#     logout(request)
#     return redirect(reverse('index'))
