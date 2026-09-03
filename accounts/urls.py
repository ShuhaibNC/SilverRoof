from django.urls import path
from . import views

urlpatterns = [
    
    # Home Page
    path(
        "",
        views.home,
        name="home"
    ),

    # Admin Login
    path(
        "admin-login/",
        views.admin_login,
        name="admin_login"
    ),

    # Sales Member Login
    path(
        "sales-login/",
        views.sales_login,
        name="sales_login"
    ),

    # Logout
    path(
        "logout/",
        views.logout_view,
        name="logout"
    ),

    # Sales Member Management
    path(
        "sales/",
        views.sales_member_list,
        name="sales_list"
    ),

    path(
        "sales/add/",
        views.sales_member_create,
        name="add_sales"
    ),

    path(
    "sales-member/<int:member_id>/sales/",
    views.sales_member_sales_detail,
    name="sales_member_sales_detail"
),
path(
    "sales-member/<int:member_id>/export/",
    views.export_sales_member_excel,
    name="export_sales_member_excel"
),

]