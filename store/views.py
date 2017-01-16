from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from .models import Staff, Category, Comment, Order

from .forms import AddComment, SignUpForm, UserLogin, EditComment


class IndexView(generic.ListView):
    template_name = 'index.html'
    context_object_name = 'latest_store_list'

    def get_queryset(self):
        return Staff.objects.order_by('-price')[:5]


class CatListView(generic.ListView):
    template_name = 'cats.html'
    context_object_name = 'cats'

    def get_queryset(self):
        return Category.objects.order_by('name')


# class DetailView(generic.DetailView):
#     model = Staff
#     template_name = 'staff_page.html'
#     context_object_name = 'staff'


def item_page(request, item_id):
    item = get_object_or_404(Staff, pk=item_id)
    comments = Comment.objects.filter(staff_id=item_id)
    authors = []
    for x in comments:
        authors.append(User.objects.get(pk=x.user_id))
    data = zip(comments, authors)
    comment_form = AddComment
    return render(request, 'staff_page.html', {'item': item,
                                               'data': data,
                                               'comment_form': comment_form,
                                               })


def category(request, category_id):
    items_on_cat = Staff.objects.filter(category__id=category_id)
    category_object = Category.objects.get(pk=category_id)
    return render(request, 'category.html', {'category': items_on_cat,
                                             'category_object': category_object})


@login_required
def add_comment(request, item_id):
    item = get_object_or_404(Staff, pk=item_id)
    if request.method == "POST":
        form = AddComment(request.POST)
        if form.is_valid():
            comment = Comment()
            comment.user_id = request.user.id
            comment.time_added = timezone.now()
            comment.staff = item
            comment.text = form.cleaned_data.get('text')
            comment.save()
            return HttpResponseRedirect(reverse('store:detail', args=(item_id,)))
    else:
        return HttpResponseRedirect(reverse('store:detail', args=(item_id,)))


@login_required
def edit_comment(request, comment_id):
    get_object_or_404(Comment, pk=comment_id)
    if request.method == "POST":
        form = EditComment(request.POST)
        if form.is_valid():
            comment = Comment.objects.get(pk=comment_id)
            comment.text = form.cleaned_data.get('text')
            comment.save()
            return HttpResponseRedirect(reverse('store:user_comments'))
    else:
        return HttpResponseRedirect(reverse('store:user_comments'))


@login_required
def edit_comment_page(request, comment_id):
    comment_form = EditComment
    comment = Comment.objects.filter(pk=comment_id)
    return render(request, 'edit_comment.html', {'comment': comment,
                                                 'comment_form': comment_form})


def signup(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('store:index', ))
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if not form.is_valid():
            return render(request, 'signup.html', {'form': form})
        else:
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            email = form.cleaned_data.get('email')
            User.objects.create_user(username=username, password=password, email=email)
            user = authenticate(username=username, password=password)
            login(request, user)
            return HttpResponseRedirect(reverse('store:index', ))
    else:
        return render(request, 'signup.html', {'form': SignUpForm})


@login_required
def user_logout(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('store:index', ))
    else:
        logout(request)
        return HttpResponseRedirect(reverse('store:index', ))


def user_login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('store:index', ))

    if request.method == 'POST':
        form = UserLogin(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('login')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('store:index', ))
            else:
                error_message = 'Wrong login/password'
                return render(request, 'login.html', {'form': UserLogin,
                                                      'error': error_message})

    else:
        return render(request, 'login.html', {'form': UserLogin})


@login_required
def create_order(request, item_id):
    if request.method == 'POST':
        item = get_object_or_404(Staff, pk=item_id)
        order = Order()
        order.user_id = request.user.id
        order.item = item
        order.save()
        return HttpResponseRedirect(reverse('store:detail', args=(item_id,)))
    else:
        return HttpResponseRedirect(reverse('store:index', ))


@login_required
def user_comments(request):
    comments = Comment.objects.filter(user_id=request.user.id)
    return render(request, 'user_comments.html', {'comments': comments,})


@login_required
def delete_comment(request, comment_id):
    Comment.objects.filter(pk=comment_id).delete()
    return HttpResponseRedirect(reverse('store:user_comments', ))


def search(request):
    if 'search_text' in request.GET and request.GET['search_text']:
        search_text = request.GET['search_text']
        result = Staff.objects.filter(name__icontains=search_text)
        if result:
            return render(request, 'search_results.html', {'result': result})
        else:
            error_message = 'No objects'
            return render(request, 'search_results.html', {'error_message': error_message})
    else:
        error_message = 'Enter search request'
        return render(request, 'search_results.html', {'error_message': error_message})


def user_orders(request):
    orders = Order.objects.filter(user_id=request.user.id)
    return render(request, 'user_orders.html', {'orders': orders,
                                                })
