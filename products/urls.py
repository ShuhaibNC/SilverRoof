from django.urls import path

from . import views


urlpatterns = [

    # ======================================================
    # PRODUCT LIST
    # ======================================================

    path(
        "",
        views.product_list,
        name="product_list"
    ),

    # ======================================================
    # ADD PRODUCT
    # ======================================================

    path(
        "add/",
        views.add_product,
        name="add_product"
    ),

    # ======================================================
    # EDIT PRODUCT
    # ======================================================

    path(
        "edit/<int:id>/",
        views.edit_product,
        name="edit_product"
    ),

    # ======================================================
    # DELETE PRODUCT
    # ======================================================

    path(
        "delete/<int:id>/",
        views.delete_product,
        name="delete_product"
    ),


    # ======================================================
    # STOCK
    # ======================================================

    path(
        "stock/",
        views.stock_list,
        name="stock_list"
    ),

    path(
        "stock/add/",
        views.add_stock,
        name="add_stock"
    ),

    path(
        "stock/edit/<int:id>/",
        views.edit_stock,
        name="edit_stock"
    ),

    path(
        "stock/delete/<int:id>/",
        views.delete_stock,
        name="delete_stock"
    ),

    path(
        "stock/filter-options/",
        views.stock_filter_options,
        name="stock_filter_options"
    ),


    # ======================================================
    # SUBCATEGORIES
    # ======================================================

    path(
        "load-subcategories/",
        views.load_subcategories,
        name="load_subcategories"
    ),

    path(
        "get-subcategories/",
        views.get_subcategories,
        name="get_subcategories"
    ),


    # ======================================================
    # SALES MEMBER PRODUCT APIs
    # ======================================================

    path(
        "get-products-by-category/",
        views.get_products_by_category,
        name="get_products_by_category"
    ),

    path(
        "get-products-by-subcategory/",
        views.get_products_by_subcategory,
        name="get_products_by_subcategory"
    ),

    path(
        "get-product-details/",
        views.get_product_details,
        name="get_product_details"
    ),
    path(
    "stock/detail/<int:id>/",
    views.stock_detail,
    name="stock_detail"
),

]