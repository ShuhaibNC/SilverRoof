from django.urls import path
from . import views


urlpatterns = [

    # ==========================================
    # MAIN DASHBOARD
    # ==========================================

    path(
        "",
        views.dashboard_redirect,
        name="dashboard"
    ),

    # ==========================================
    # ADMIN DASHBOARD
    # ==========================================

    path(
        "admin/",
        views.admin_dashboard,
        name="admin_dashboard"
    ),

    # ==========================================
    # SALES MEMBERS LIST
    # ==========================================
    # Sales members list
    path(
        "sales/",
        views.sales_members,
        name="sales_members"
    ),


    # ==========================================
    # SALES DASHBOARD
    # ==========================================

    path(
        "sales/dashboard/",
        views.sales_dashboard,
        name="sales_dashboard"
    ),

    # ==========================================
    # ADD SALES MEMBER
    # ==========================================

    path(
        "sales/add/",
        views.add_sales_member,
        name="add_sales_member"
    ),

    # ==========================================
    # DELETE SALES MEMBER
    # ==========================================
path(
    "sales-members/delete/<int:id>/",
    views.delete_sales_member,
    name="delete_sales_member"
),
]