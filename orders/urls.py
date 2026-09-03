from django.urls import path

from . import views


urlpatterns = [

    # ======================================================
    # ORDER LIST
    # ======================================================
    path(
        "",
        views.order_list,
        name="order_list"
    ),


    # ======================================================
    # ADD ORDER
    # ======================================================
    path(
        "add/",
        views.add_order,
        name="add_order"
    ),


    # ======================================================
    # EDIT ORDER
    # ======================================================
    path(
        "edit/<int:id>/",
        views.edit_order,
        name="edit_order"
    ),


    # ======================================================
    # DELETE ORDER
    # ======================================================
    path(
        "delete/<int:id>/",
        views.delete_order,
        name="delete_order"
    ),


    # ======================================================
    # GET SUBCATEGORIES
    # ======================================================
    path(
        "get-subcategories/",
        views.get_subcategories,
        name="get_subcategories"
    ),


    # ======================================================
    # GET PRODUCTS BY CATEGORY
    # ======================================================
    path(
        "get-products/",
        views.get_products,
        name="get_products"
    ),


    # ======================================================
    # GET PRODUCT DETAILS
    # ======================================================
    path(
        "get-product-details/",
        views.get_product_details,
        name="get_product_details"
    ),


    # ======================================================
    # EXPORT EXCEL
    # ======================================================
    path(
        "export-excel/",
        views.export_orders_excel,
        name="export_orders_excel"
    ),


    # ======================================================
    # DISPATCH ORDER
    # ======================================================
    path(
        "dispatch/<int:order_id>/",
        views.dispatch_order,
        name="dispatch_order"
    ),

]