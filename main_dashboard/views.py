from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group
from django.db.models import Sum
from django.views.decorators.cache import never_cache

from products.models import Product
from customers.models import Customer
from orders.models import Order


# ============================================================
# ADMIN CHECK
# ============================================================

def is_admin(user):
    return user.is_authenticated and user.is_superuser


# ============================================================
# DASHBOARD REDIRECT
# ============================================================

@login_required
@never_cache
def dashboard_redirect(request):

    if request.user.is_superuser:
        return redirect("admin_dashboard")

    return redirect("sales_dashboard")


# ============================================================
# ADMIN DASHBOARD
# ============================================================

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):

    total_sales = (
        Order.objects.aggregate(
            total=Sum("amount")
        )["total"] or 0
    )

    # Default value
    sales_members = User.objects.none()

    # Get Sales group
    try:
        sales_group = Group.objects.get(name="Sales")

        sales_members = User.objects.filter(
            groups=sales_group,
            is_superuser=False,
            is_active=True
        )

    except Group.DoesNotExist:
        pass

    context = {
        "products": Product.objects.count(),
        "customers": Customer.objects.count(),
        "orders": Order.objects.count(),
        "sales_members": sales_members.count(),
        "recent_orders": Order.objects.order_by("-id")[:5],
        "total_sales": total_sales,
    }

    return render(
        request,
        "dashboard/admin_dashboard.html",
        context
    )


# ============================================================
# SALES DASHBOARD
# ============================================================

@login_required
def sales_dashboard(request):

    my_orders = Order.objects.filter(
        sales_member=request.user
    ).order_by("-created_at")

    recent_orders = my_orders[:5]

    total_sales = (
        my_orders.aggregate(
            total=Sum("amount")
        )["total"] or 0
    )

    context = {
        "products": Product.objects.count(),
        "customers": Customer.objects.count(),
        "orders": my_orders.count(),
        "total_sales": total_sales,
        "recent_orders": recent_orders,
    }

    return render(
        request,
        "dashboard/sales_dashboard.html",
        context
    )


# ============================================================
# SALES MEMBERS LIST
# ============================================================
@login_required
@user_passes_test(is_admin)
def sales_members(request):

    try:
        sales_group = Group.objects.get(name="Sales")

        members = User.objects.filter(
            groups=sales_group,
            is_superuser=False,
            is_active=True
        ).order_by("first_name", "username")

    except Group.DoesNotExist:
        members = User.objects.none()

    for member in members:

        member.pending_count = Order.objects.filter(
            sales_member=member,
            status="Pending"
        ).count()

        member.dispatched_count = Order.objects.filter(
            sales_member=member,
            status="Completed"
        ).count()

        member.out_of_stock_count = Order.objects.filter(
            sales_member=member,
            status="Out of Stock"
        ).count()

        member.total_sales = (
            Order.objects.filter(
                sales_member=member,
                status="Completed"
            ).aggregate(
                total=Sum("amount")
            )["total"] or 0
        )

    context = {
        "members": members
    }

    return render(
        request,
        "accounts/sales_members.html",
        context
    )

# ============================================================
# ADD SALES MEMBER
# ============================================================

@login_required
@user_passes_test(is_admin)
def add_sales_member(request):

    if request.method == "POST":

        username = request.POST.get(
            "username",
            ""
        ).strip()

        first_name = request.POST.get(
            "first_name",
            ""
        ).strip()

        last_name = request.POST.get(
            "last_name",
            ""
        ).strip()

        email = request.POST.get(
            "email",
            ""
        ).strip()

        password = request.POST.get(
            "password",
            ""
        )

        # VALIDATION

        if not username:

            return render(
                request,
                "accounts/add_sales.html",
                {
                    "error": "Username is required."
                }
            )

        if not password:

            return render(
                request,
                "accounts/add_sales.html",
                {
                    "error": "Password is required."
                }
            )

        if User.objects.filter(
            username=username
        ).exists():

            return render(
                request,
                "accounts/add_sales.html",
                {
                    "error": "Username already exists."
                }
            )

        # CREATE USER

        user = User.objects.create_user(
            username=username,
            password=password
        )

        user.first_name = first_name
        user.last_name = last_name
        user.email = email

        user.is_staff = False
        user.is_superuser = False
        user.is_active = True

        user.save()

        # GET / CREATE SALES GROUP

        sales_group, created = Group.objects.get_or_create(
            name="Sales"
        )

        user.groups.add(sales_group)

        return redirect("sales_members")

    return render(
        request,
        "accounts/add_sales.html"
    )


# ============================================================
# DELETE SALES MEMBER
# ============================================================

# ============================================================
# DELETE SALES MEMBER
# ============================================================

@login_required
@user_passes_test(is_admin)
def delete_sales_member(request, id):

    member = get_object_or_404(
        User,
        id=id,
        is_superuser=False
    )

    if request.method == "POST":

        # Soft delete
        member.is_active = False
        member.save()

        return redirect("sales_members")

    return render(
        request,
        "accounts/delete_sales_member.html",
        {
            "member": member
        }
    )