from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404, redirect, render

from products.models import Category, Product
from sales.models import SalesOrder

from .forms import CategoryForm, ProductForm, SalesOrderForm, UserForm

User = get_user_model()


def is_admin_or_staff(user):
    return (user.is_authenticated) and (user.role == "admin" or user.is_staff)


@user_passes_test(is_admin_or_staff, login_url="/")
def admin_panel_index(request):
    return render(request, "adminpanel/index.html")


@user_passes_test(is_admin_or_staff, login_url="/")
def user_list(request):
    users = User.objects.all()
    return render(request, "adminpanel/user_list.html", {"users": users})


@user_passes_test(is_admin_or_staff, login_url="/")
def user_create(request):
    if request.method == "POST":
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "User created successfully.")
            return redirect("adminpanel:user_list")
    else:
        form = UserForm()
    return render(
        request, "adminpanel/user_form.html", {"form": form, "title": "Create User"}
    )


@user_passes_test(is_admin_or_staff, login_url="/")
def user_update(request, user_id):
    user_obj = get_object_or_404(User, id=user_id)
    if request.method == "POST":
        form = UserForm(request.POST, request.FILES, instance=user_obj)
        if form.is_valid():
            form.save()
            messages.success(request, "User updated successfully.")
            return redirect("adminpanel:user_list")
    else:
        form = UserForm(instance=user_obj)
    return render(
        request,
        "adminpanel/user_form.html",
        {"form": form, "title": f"Edit User #{user_id}"},
    )


# ---- Product Management ----
@user_passes_test(is_admin_or_staff, login_url="/")
def product_list(request):
    products = Product.objects.select_related("category").all()
    return render(request, "adminpanel/product_list.html", {"products": products})


@user_passes_test(is_admin_or_staff, login_url="/")
def product_create(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Product created successfully.")
            return redirect("adminpanel:product_list")
    else:
        form = ProductForm()
    return render(
        request,
        "adminpanel/product_form.html",
        {"form": form, "title": "Create Product"},
    )


@user_passes_test(is_admin_or_staff, login_url="/")
def product_update(request, product_id):
    product_obj = get_object_or_404(Product, id=product_id)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product_obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Product updated successfully.")
            return redirect("adminpanel:product_list")
    else:
        form = ProductForm(instance=product_obj)
    return render(
        request,
        "adminpanel/product_form.html",
        {"form": form, "title": f"Edit Product #{product_id}"},
    )


@user_passes_test(is_admin_or_staff, login_url="/")
def salesorder_list(request):
    orders = SalesOrder.objects.select_related("customer").all()
    return render(request, "adminpanel/salesorder_list.html", {"orders": orders})


@user_passes_test(is_admin_or_staff, login_url="/")
def salesorder_update(request, order_id):
    order_obj = get_object_or_404(SalesOrder, id=order_id)
    if request.method == "POST":
        form = SalesOrderForm(request.POST, instance=order_obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Sales order updated successfully.")
            return redirect("adminpanel:salesorder_list")
    else:
        form = SalesOrderForm(instance=order_obj)
    return render(
        request,
        "adminpanel/salesorder_form.html",
        {"form": form, "title": f"Edit SalesOrder #{order_id}", "order": order_obj},
    )


def is_admin_only(user):
    return user.is_authenticated and (user.role == "admin" or user.is_staff)


@user_passes_test(is_admin_only, login_url="/")
def category_list(request):
    categories = Category.objects.all()
    return render(request, "adminpanel/category_list.html", {"categories": categories})


@user_passes_test(is_admin_only, login_url="/")
def category_create(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Category created successfully.")
            return redirect("adminpanel:category_list")
    else:
        form = CategoryForm()
    return render(
        request,
        "adminpanel/category_form.html",
        {"form": form, "title": "Create Category"},
    )


@user_passes_test(is_admin_only, login_url="/")
def category_update(request, category_id):
    category_obj = get_object_or_404(Category, id=category_id)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category_obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Category updated successfully.")
            return redirect("adminpanel:category_list")
    else:
        form = CategoryForm(instance=category_obj)
    return render(
        request,
        "adminpanel/category_form.html",
        {"form": form, "title": f"Edit Category #{category_id}"},
    )
