# from django.contrib import admin

# from .models import (
#     Category,
#     SubCategory,
#     Brand,
#     Thickness,
#     Colour,
#     Design,
#     Product,
#     ProductStock,
#     Customer,
# )


# # ==========================================================
# # CATEGORY
# # ==========================================================

# @admin.register(Category)
# class CategoryAdmin(admin.ModelAdmin):

#     list_display = (
#         "id",
#         "name",
#     )

#     search_fields = (
#         "name",
#     )


# # ==========================================================
# # SUB CATEGORY
# # ==========================================================

# @admin.register(SubCategory)
# class SubCategoryAdmin(admin.ModelAdmin):

#     list_display = (
#         "id",
#         "name",
#         "category",
#     )

#     list_filter = (
#         "category",
#     )

#     search_fields = (
#         "name",
#     )


# # ==========================================================
# # BRAND
# # ==========================================================

# @admin.register(Brand)
# class BrandAdmin(admin.ModelAdmin):

#     list_display = (
#         "id",
#         "name",
#     )

#     search_fields = (
#         "name",
#     )


# # ==========================================================
# # THICKNESS
# # ==========================================================

# @admin.register(Thickness)
# class ThicknessAdmin(admin.ModelAdmin):

#     list_display = (
#         "id",
#         "name",
#     )

#     search_fields = (
#         "name",
#     )


# # ==========================================================
# # COLOUR
# # ==========================================================

# @admin.register(Colour)
# class ColourAdmin(admin.ModelAdmin):

#     list_display = (
#         "id",
#         "name",
#     )

#     search_fields = (
#         "name",
#     )


# # ==========================================================
# # DESIGN
# # ==========================================================

# @admin.register(Design)
# class DesignAdmin(admin.ModelAdmin):

#     list_display = (
#         "id",
#         "name",
#     )

#     search_fields = (
#         "name",
#     )


# # ==========================================================
# # PRODUCT
# # ==========================================================

# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):

#     list_display = (
#         "id",
#         "category",
#         "product_name",
#         "width_ft",
#         "colour",
#         "brand",
#         "core_number",
#         "sqt_rate",
#         "size",
#     )

#     list_filter = (
#         "category",
#         "brand",
#         "colour",
#     )

#     search_fields = (
#         "product_name",
#         "category__name",
#         "brand__name",
#         "colour__name",
#         "core_number",
#     )

#     ordering = (
#         "category",
#         "product_name",
#     )


# # ==========================================================
# # PRODUCT STOCK
# # ==========================================================

# @admin.register(ProductStock)
# class ProductStockAdmin(admin.ModelAdmin):

#     list_display = (
#         "id",
#         "product",
#         "category_name",
#         "length_ft",
#         "quantity",
#         "out_of_stock",
#         "updated_at",
#     )

#     list_filter = (
#         "out_of_stock",
#         "product__category",
#     )

#     search_fields = (
#         "product__product_name",
#         "product__category__name",
#     )

#     readonly_fields = (
#         "updated_at",
#     )

#     ordering = (
#         "product__category",
#         "product__product_name",
#     )

#     # ------------------------------------------------------
#     # CATEGORY NAME
#     # ------------------------------------------------------

#     @admin.display(
#         description="Category"
#     )
#     def category_name(self, obj):

#         return obj.product.category.name


# # ==========================================================
# # CUSTOMER
# # ==========================================================

# @admin.register(Customer)
# class CustomerAdmin(admin.ModelAdmin):

#     list_display = (
#         "id",
#         "customer_name",
#         "phone",
#         "location",
#         "gst_number",
#     )

#     list_filter = (
#         "location",
#     )

#     search_fields = (
#         "customer_name",
#         "phone",
#         "gst_number",
#     )

#     ordering = (
#         "customer_name",
#     )



from django.contrib import admin

from .models import (
    Category,
    SubCategory,
    Brand,
    Thickness,
    Colour,
    Design,
    Product,
    ProductStock,
    Customer,
)


# ==========================================================
# CATEGORY
# ==========================================================

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
    )

    search_fields = (
        "name",
    )


# ==========================================================
# SUB CATEGORY
# ==========================================================

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
        "category",
    )

    list_filter = (
        "category",
    )

    search_fields = (
        "name",
    )


# ==========================================================
# BRAND
# ==========================================================

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
    )

    search_fields = (
        "name",
    )


# ==========================================================
# THICKNESS
# ==========================================================

@admin.register(Thickness)
class ThicknessAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
    )

    search_fields = (
        "name",
    )


# ==========================================================
# COLOUR
# ==========================================================

@admin.register(Colour)
class ColourAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
    )

    search_fields = (
        "name",
    )


# ==========================================================
# DESIGN
# ==========================================================

@admin.register(Design)
class DesignAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
    )

    search_fields = (
        "name",
    )


# ==========================================================
# PRODUCT
# ==========================================================

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "category",
        "product_name",
        "width_ft",
        "colour",
        "brand",
        "core_number",
        "sqt_rate",
        "size",
        "nos",
    )

    list_filter = (
        "category",
        "brand",
        "colour",
    )

    search_fields = (
        "product_name",
        "category__name",
        "brand__name",
        "colour__name",
        "core_number",
    )

    ordering = (
        "category",
        "product_name",
    )


# ==========================================================
# PRODUCT STOCK
# ==========================================================

@admin.register(ProductStock)
class ProductStockAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "product",
        "category_name",
        "length_ft",
        "quantity",
        "out_of_stock",
        "updated_at",
    )

    list_filter = (
        "out_of_stock",
        "product__category",
    )

    search_fields = (
        "product__product_name",
        "product__category__name",
    )

    readonly_fields = (
        "updated_at",
    )

    ordering = (
        "product__category",
        "product__product_name",
    )

    # ------------------------------------------------------
    # CATEGORY NAME
    # ------------------------------------------------------

    @admin.display(
        description="Category"
    )
    def category_name(self, obj):

        return obj.product.category.name


# ==========================================================
# CUSTOMER
# ==========================================================

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "customer_name",
        "phone",
        "location",
        "gst_number",
    )

    list_filter = (
        "location",
    )

    search_fields = (
        "customer_name",
        "phone",
        "gst_number",
    )

    ordering = (
        "customer_name",
    )