from core.models import Product, Profile, UpdateNote
from core.utils import create_chart_data, create_or_link_product, validate_url_with_stores, create_or_find_product
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import redirect, render

# Create your views here.


def index_landing(request):
    template_name = "landing/index.html"
    context = {}
    return render(request, template_name, context)

def unfollow_product(request, pk):
    product = Product.objects.get(pk=pk)
    if request.user in product.users.all():
        product.users.remove(request.user)
        messages.success(request, "El producto fue removido de tu whislist!")
    else:
        messages.error(request, "El producto no esta en tu wishlist!")
    return redirect(index)

@login_required(login_url='/login')
def index(request):
    template_name = "index.html"
    context = {}
    products = Product.objects.all().reverse()
    context["products"] = products
    if request.POST:
        url = request.POST["url"]
        if validate_url_with_stores(url):
            if not create_or_link_product(url, request):
                messages.error(request, 'El Producto no pudo ser agregado a tu lista. Por Favor intenta mas tarde.')
        else:
            messages.error(request, 'Lo sentimos, la url ingresada no pertenece a ninguna de nuestras tiendas compatibles. Estamos trabajando para agregar la mayor cantidad de tiendas posibles!')
    return render(request, template_name, context)


def login_view(request):
    template_name = "login.html"
    context = {}
    logout(request)
    if request.POST:
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            messages.error(request, 'Usuario y/o Contraseña Incorrectos')
    return render(request, template_name, context)


def register_view(request):
    template_name = "register.html"
    context = {}
    if request.POST:
        if len(User.objects.filter(email=request.POST["email"])) != 0:
            messages.error(request, 'El usuario ya se encuentra registrado.')
        else:        
            if request.POST["password"] == request.POST["confirm_password"]:
                user = User.objects.create_user(request.POST["email"], request.POST["email"], request.POST["password"])
                user.first_name = request.POST["firstname"]
                user.last_name = request.POST["lastname"]
                user.save()
                profile = Profile.objects.create(user=user)
                profile.save()
                messages.success(request, 'Usuario registrado con exito!')
                return redirect('login')
            else:
                messages.success(request, 'Las contraseñas ingresadas no coinciden')
    return render(request, template_name, context)


@login_required(login_url='/login')
def product_detail(request, pk):
    template_name = "product_detail.html"
    context = {}
    product = Product.objects.get(pk=pk)
    context["product"] = product
    chart_data = create_chart_data(product)
    context["labels"] = chart_data[0]
    context["prices"] = chart_data[1]
    if context["prices"]:
        context["max_price"] = int(max(chart_data[1], key=float)) + ((int(max(chart_data[1], key=float))*10)/100)
    return render(request, template_name, context)


@login_required(login_url='/login')
def config_view(request):
    template_name = "config.html"
    context = {}
    if request.POST:
        if "notifications" in request.POST:
            if int(request.POST["notifications"]) == 1:
                request.user.profile.notifications = True
                request.user.profile.save()
            else:
                request.user.profile.notifications = False
                request.user.profile.save()
        if "updates_notifications" in request.POST:
            if int(request.POST["updates_notifications"]) == 1:
                request.user.profile.updates_notifications = True
                request.user.profile.save()
            else:
                request.user.profile.updates_notifications = False
                request.user.profile.save()
        return JsonResponse({"result": "200"})
    return render(request, template_name, context)


def updates_view(request):
    template_name="landing/updates.html"
    context = {}
    context["notes"] = UpdateNote.objects.all().order_by("-date")
    return render(request, template_name, context)

def search_product(request):
    context = {}
    if request.POST:
        url = request.POST["url"]
        if validate_url_with_stores(url):
            product = create_or_find_product(url)
            if not product:
                messages.error(request, 'No pudimos consultar tu producto. Por favor intenta más tarde')
            else:
                context["product"] = product
                chart_data = create_chart_data(context["product"])
                context["labels"] = chart_data[0]
                context["prices"] = chart_data[1]
                if context["prices"]:
                    context["max_price"] = int(max(chart_data[1], key=float))
        else:
            messages.error(request, 'Lo sentimos, la url ingresada no pertenece a ninguna de nuestras tiendas compatibles. Estamos trabajando para agregar la mayor cantidad de tiendas posibles!')
    template_name="landing/search_product.html"
    return render(request, template_name, context)