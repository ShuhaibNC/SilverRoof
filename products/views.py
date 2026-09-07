from decimal import Decimal, InvalidOperation

from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
)

from django.http import JsonResponse

from django.contrib.auth.decorators import (
    login_required,
    user_passes_test,
)

from django.contrib import messages

from .forms import (
    ProductForm,
    ProductStockForm,
)

from .models import (
    Product,
    ProductStock,
    SubCategory,
    Thickness,
    Colour,
    Design,
    Brand,
    Category,
)

from django.contrib.auth.decorators import user_passes_test


# ==========================================================
# CHECK ADMIN
# ==========================================================

def is_admin(user):
    return user.is_superuser


def is_sales_member(user):
    return user.is_authenticated and not user.is_staff


# ==========================================================
# CATEGORY NAME HELPER
# ==========================================================

def get_category_name(category):

    if not category:
        return ""

    return (
        category.name
        .strip()
        .lower()
        .replace(" ", "")
        .replace("-", "")
        .replace("_", "")
    )


# ==========================================================
# PRODUCT LIST
# ==========================================================

@login_required
def product_list(request):

    products = (
        Product.objects
        .select_related(
            "category",
            "subcategory",
            "brand",
            "thickness",
            "colour",
            "design",
        )
        .all()
        .order_by("-id")
    )

    return render(
        request,
        "products/product_list.html",
        {
            "products": products
        }
    )


# ==========================================================
# ADD PRODUCT
# ADMIN ONLY
# ==========================================================

@login_required
@user_passes_test(is_admin)
def add_product(request):

    if request.method == "POST":

        form = ProductForm(request.POST)

        if form.is_valid():

            product = form.save()

            ProductStock.objects.get_or_create(
                product=product
            )

            messages.success(
                request,
                "Product added successfully."
            )

            return redirect("product_list")

        else:

            print("FORM ERRORS:")
            print(form.errors)

    else:

        form = ProductForm()

    return render(
        request,
        "products/product_form.html",
        {
            "form": form
        }
    )


# ==========================================================
# EDIT PRODUCT
# ADMIN ONLY
# ==========================================================

@login_required
@user_passes_test(is_admin)
def edit_product(request, id):

    product = get_object_or_404(
        Product,
        id=id
    )

    if request.method == "POST":

        form = ProductForm(
            request.POST,
            instance=product
        )

        if form.is_valid():

            product = form.save()

            ProductStock.objects.get_or_create(
                product=product
            )

            messages.success(
                request,
                "Product updated successfully."
            )

            return redirect("product_list")

    else:

        form = ProductForm(
            instance=product
        )

    return render(
        request,
        "products/product_form.html",
        {
            "form": form,
            "product": product
        }
    )


# ==========================================================
# DELETE PRODUCT
# ADMIN ONLY
# ==========================================================

@login_required
@user_passes_test(is_admin)
def delete_product(request, id):

    product = get_object_or_404(Product, id=id)

    if request.method == "POST":
        product.delete()

        messages.success(
            request,
            "Product deleted successfully."
        )

        return redirect("product_list")

    return render(
        request,
        "products/product_confirm_delete.html",
        {
            "product": product
        }
    )


# ==========================================================
# STOCK LIST
# ADMIN ONLY
# ==========================================================

@login_required
def stock_list(request):

    stocks = (
        ProductStock.objects
        .select_related(
            "product",
            "product__category",
            "product__subcategory",
            "product__colour",
            "product__brand",
            "product__thickness",
            "product__design",
        )
        .all()
        .order_by(
            "product__category__name",
            "product__product_name"
        )
    )

    return render(
        request,
        "products/stock_list.html",
        {
            "stocks": stocks
        }
    )


# ==========================================================
# ADD STOCK
# ADMIN ONLY
# ==========================================================

@login_required
@user_passes_test(is_admin)
def add_stock(request):

    if request.method == "POST":

        form = ProductStockForm(request.POST)

        if form.is_valid():

            stock = form.save(commit=False)

            product = form.cleaned_data.get("product")

            # ==================================================
            # PRODUCT VALIDATION
            # ==================================================

            if not product:

                form.add_error(
                    "product",
                    "Please select a product."
                )

            else:

                stock.product = product

                category_name = get_category_name(
                    product.category
                )

                # ==================================================
                # CATEGORY 1 / CATEGORY 2
                # STOCK BASED ON LENGTH
                # ==================================================

                if category_name in [
                    "category1",
                    "category2"
                ]:

                    # Category 1 and 2 do not use quantity
                    stock.quantity = 0

                    if stock.length_ft is None:

                        form.add_error(
                            "length_ft",
                            "Please enter available length."
                        )

                    elif stock.length_ft <= Decimal("0"):

                        form.add_error(
                            "length_ft",
                            "Available length must be greater than 0."
                        )

                    else:

                        stock.out_of_stock = False


                # ==================================================
                # CATEGORY 3
                # STOCK BASED ON PRODUCT NOS
                # ==================================================

                elif category_name == "category3":

                    # Category 3 does not use length
                    stock.length_ft = Decimal("0.00")

                    # Product NOS is the source of truth
                    stock.quantity = product.nos or 0

                    if stock.quantity <= 0:

                        stock.out_of_stock = True

                    else:

                        stock.out_of_stock = False


                # ==================================================
                # OTHER CATEGORY
                # ==================================================

                else:

                    # Default stock status
                    stock.out_of_stock = False


                # ==================================================
                # SAVE STOCK
                # ==================================================

                if not form.errors:

                    stock.save()

                    messages.success(
                        request,
                        "Stock added successfully."
                    )

                    return redirect(
                        "stock_list"
                    )

        # If form is invalid, page will show errors

    else:

        form = ProductStockForm()


    return render(
        request,
        "products/stock_form.html",
        {
            "form": form,
            "stock": None,
            "categories": Category.objects.all().order_by(
                "name"
            ),
            "edit": False,
        }
    )


# ==========================================================
# STOCK FILTER OPTIONS
# ==========================================================

@login_required
@user_passes_test(is_admin)
def stock_filter_options(request):

    category_id = request.GET.get("category")
    subcategory_id = request.GET.get("subcategory")
    thickness_id = request.GET.get("thickness")
    colour_id = request.GET.get("colour")
    design_id = request.GET.get("design")
    brand_id = request.GET.get("brand")

    products = Product.objects.all()

    if category_id:

        products = products.filter(
            category_id=category_id
        )

    if subcategory_id:

        products = products.filter(
            subcategory_id=subcategory_id
        )

    if thickness_id:

        products = products.filter(
            thickness_id=thickness_id
        )

    if colour_id:

        products = products.filter(
            colour_id=colour_id
        )

    if design_id:

        products = products.filter(
            design_id=design_id
        )

    if brand_id:

        products = products.filter(
            brand_id=brand_id
        )


    subcategory_ids = (
        products
        .exclude(subcategory_id__isnull=True)
        .values_list(
            "subcategory_id",
            flat=True
        )
        .distinct()
    )


    thickness_ids = (
        products
        .exclude(thickness_id__isnull=True)
        .values_list(
            "thickness_id",
            flat=True
        )
        .distinct()
    )


    colour_ids = (
        products
        .exclude(colour_id__isnull=True)
        .values_list(
            "colour_id",
            flat=True
        )
        .distinct()
    )


    design_ids = (
        products
        .exclude(design_id__isnull=True)
        .values_list(
            "design_id",
            flat=True
        )
        .distinct()
    )


    brand_ids = (
        products
        .exclude(brand_id__isnull=True)
        .values_list(
            "brand_id",
            flat=True
        )
        .distinct()
    )


    subcategories = (
        SubCategory.objects
        .filter(id__in=subcategory_ids)
        .order_by("name")
    )


    thicknesses = (
        Thickness.objects
        .filter(id__in=thickness_ids)
        .order_by("name")
    )


    colours = (
        Colour.objects
        .filter(id__in=colour_ids)
        .order_by("name")
    )


    designs = (
        Design.objects
        .filter(id__in=design_ids)
        .order_by("name")
    )


    brands = (
        Brand.objects
        .filter(id__in=brand_ids)
        .order_by("name")
    )


    widths = (
        products
        .exclude(width_ft__isnull=True)
        .order_by("width_ft")
    )


    return JsonResponse({

        "subcategories": [
            {
                "id": item.id,
                "name": item.name
            }
            for item in subcategories
        ],

        "thicknesses": [
            {
                "id": item.id,
                "name": item.name
            }
            for item in thicknesses
        ],

        "colours": [
            {
                "id": item.id,
                "name": item.name
            }
            for item in colours
        ],

        "designs": [
            {
                "id": item.id,
                "name": item.name
            }
            for item in designs
        ],

        "brands": [
            {
                "id": item.id,
                "name": item.name
            }
            for item in brands
        ],

        "widths": [
            {
                "product_id": item.id,
                "width": str(item.width_ft)
            }
            for item in widths
        ]

    })


# ==========================================================
# EDIT STOCK
# ADMIN ONLY
# ==========================================================

@login_required
@user_passes_test(is_admin)
def edit_stock(request, id):

    stock = get_object_or_404(
        ProductStock,
        id=id
    )

    product = stock.product

    category_name = get_category_name(
        product.category
    )

    categories = Category.objects.all().order_by(
        "name"
    )


    if request.method == "POST":

        # ==================================================
        # CATEGORY 1 / CATEGORY 2
        # ==================================================

        if category_name in [
            "category1",
            "category2"
        ]:

            length_ft = request.POST.get(
                "length_ft",
                "0"
            )

            try:

                stock.length_ft = Decimal(
                    str(length_ft)
                )

            except (
                InvalidOperation,
                TypeError,
                ValueError
            ):

                messages.error(
                    request,
                    "Please enter a valid length."
                )

                return render(
                    request,
                    "products/stock_form.html",
                    {
                        "stock": stock,
                        "edit": True,
                        "categories": categories,
                    }
                )


            if stock.length_ft < 0:

                messages.error(
                    request,
                    "Length cannot be negative."
                )

                return render(
                    request,
                    "products/stock_form.html",
                    {
                        "stock": stock,
                        "edit": True,
                        "categories": categories,
                    }
                )


            # Category 1 and 2 stock status

            stock.out_of_stock = (
                stock.length_ft <= Decimal("0.00")
            )


        # ==================================================
        # CATEGORY 3
        # ==================================================

        elif category_name == "category3":

            # Category 3 quantity always comes from Product NOS
            stock.quantity = product.nos or 0

            # Category 3 does not use length
            stock.length_ft = Decimal("0.00")

            # Category 3 stock status
            stock.out_of_stock = (
                stock.quantity <= 0
            )


        # ==================================================
        # OTHER CATEGORY
        # ==================================================

        else:

            stock.out_of_stock = False


        # ==================================================
        # SAVE STOCK
        # ==================================================

        stock.save()

        messages.success(
            request,
            "Stock updated successfully."
        )

        return redirect(
            "stock_list"
        )


    # ======================================================
    # GET REQUEST
    # ======================================================

    return render(
        request,
        "products/stock_form.html",
        {
            "stock": stock,
            "product": product,
            "edit": True,
            "categories": categories,
        }
    )


# ==========================================================
# DELETE STOCK
# ADMIN ONLY
# ==========================================================

@login_required
@user_passes_test(is_admin)
def delete_stock(request, id):

    stock = get_object_or_404(
        ProductStock,
        id=id
    )

    if request.method == "POST":

        stock.delete()

        messages.success(
            request,
            "Stock deleted successfully."
        )

        return redirect(
            "stock_list"
        )

    return render(
        request,
        "products/stock_confirm_delete.html",
        {
            "stock": stock
        }
    )


# ==========================================================
# GET SUBCATEGORIES BY CATEGORY
# ==========================================================

@login_required
def get_subcategories(request):

    category_id = request.GET.get(
        "category_id"
    )

    if not category_id:

        return JsonResponse({
            "subcategories": []
        })

    subcategories = (
        SubCategory.objects
        .filter(
            category_id=category_id
        )
        .order_by("name")
    )

    data = [
        {
            "id": subcategory.id,
            "name": subcategory.name
        }
        for subcategory in subcategories
    ]

    return JsonResponse({
        "subcategories": data
    })


# ==========================================================
# LOAD SUBCATEGORIES
# ==========================================================

@login_required
def load_subcategories(request):

    category_id = request.GET.get(
        "category"
    )

    if not category_id:

        return JsonResponse(
            [],
            safe=False
        )

    subcategories = (
        SubCategory.objects
        .filter(
            category_id=category_id
        )
        .order_by("name")
    )

    data = [
        {
            "id": subcategory.id,
            "name": subcategory.name
        }
        for subcategory in subcategories
    ]

    return JsonResponse(
        data,
        safe=False
    )


# ==========================================================
# PRODUCTS BY CATEGORY
# ==========================================================

@login_required
def get_products_by_category(request):

    category_id = request.GET.get(
        "category_id"
    )

    if not category_id:

        return JsonResponse({
            "products": []
        })

    products = (
        Product.objects
        .filter(
            category_id=category_id
        )
        .select_related(
            "subcategory",
            "brand",
            "thickness",
            "colour",
            "design",
            "category"
        )
        .order_by(
            "subcategory__name",
            "product_name"
        )
    )

    data = []

    for product in products:

        data.append({

            "id": product.id,

            "product_name": (
                product.product_name
                or ""
            ),

            "subcategory_id": (
                product.subcategory.id
                if product.subcategory
                else None
            ),

            "subcategory_name": (
                product.subcategory.name
                if product.subcategory
                else (
                    product.subcategory_text
                    or ""
                )
            ),

        })

    return JsonResponse({
        "products": data
    })


# ==========================================================
# PRODUCTS BY SUBCATEGORY
# ==========================================================

@login_required
def get_products_by_subcategory(request):

    subcategory_id = request.GET.get(
        "subcategory_id"
    )

    if not subcategory_id:

        return JsonResponse({
            "products": []
        })

    products = (
        Product.objects
        .filter(
            subcategory_id=subcategory_id
        )
        .select_related(
            "category",
            "subcategory",
            "brand",
            "thickness",
            "colour",
            "design"
        )
        .order_by(
            "product_name",
            "id"
        )
    )

    data = []

    for product in products:

        data.append({

            "id": product.id,

            "product_name": (
                product.product_name
                or ""
            ),

            "width_ft": (
                str(product.width_ft)
                if product.width_ft is not None
                else ""
            ),

            "thickness": (
                product.thickness.name
                if product.thickness
                else ""
            ),

            "design": (
                product.design.name
                if product.design
                else ""
            ),

            "colour": (
                product.colour.name
                if product.colour
                else ""
            ),

            "brand": (
                product.brand.name
                if product.brand
                else ""
            ),

            "core_number": (
                product.core_number
                or ""
            ),

            "sqt_rate": (
                str(product.sqt_rate)
                if product.sqt_rate is not None
                else ""
            ),

            "size": (
                product.size
                or ""
            ),

        })

    return JsonResponse({
        "products": data
    })


# ==========================================================
# STOCK DETAIL
# ==========================================================

def stock_detail(request, id):

    stock = get_object_or_404(
        ProductStock,
        id=id
    )

    return render(
        request,
        "products/stock_detail.html",
        {
            "stock": stock
        }
    )


# ==========================================================
# PRODUCT DETAILS
# ==========================================================

@login_required
def get_product_details(request):

    product_id = request.GET.get(
        "product_id"
    )

    if not product_id:

        return JsonResponse({
            "error": "Product ID is required."
        }, status=400)

    product = get_object_or_404(
        Product.objects.select_related(
            "category",
            "subcategory",
            "brand",
            "thickness",
            "colour",
            "design"
        ),
        id=product_id
    )

    stock = getattr(
        product,
        "stock_details",
        None
    )

    stock_length = Decimal("0")

    stock_quantity = 0

    if stock:

        stock_length = (
            stock.length_ft
            if stock.length_ft is not None
            else Decimal("0")
        )

        stock_quantity = (
            stock.quantity
            if stock.quantity is not None
            else 0
        )

    category_name = get_category_name(
        product.category
    )

    return JsonResponse({

        "id": product.id,

        "category_id": (
            product.category.id
            if product.category
            else None
        ),

        "category_name": (
            product.category.name
            if product.category
            else ""
        ),

        "product_name": (
            product.product_name
            or ""
        ),

        "subcategory_id": (
            product.subcategory.id
            if product.subcategory
            else None
        ),

        "subcategory_name": (
            product.subcategory.name
            if product.subcategory
            else (
                product.subcategory_text
                or ""
            )
        ),

        "width_ft": (
            str(product.width_ft)
            if product.width_ft is not None
            else ""
        ),

        "width_meter": str(
            (
                product.width_ft
                if product.width_ft is not None
                else Decimal("0")
            )
            * Decimal("0.3048")
        ),

        "thickness": (
            product.thickness.name
            if product.thickness
            else ""
        ),

        "design": (
            product.design.name
            if product.design
            else ""
        ),

        "colour": (
            product.colour.name
            if product.colour
            else ""
        ),

        "brand": (
            product.brand.name
            if product.brand
            else ""
        ),

        "core_number": (
            product.core_number
            or ""
        ),

        "sqt_rate": (
            str(product.sqt_rate)
            if product.sqt_rate is not None
            else ""
        ),

        "size": (
            product.size
            or ""
        ),

        "stock_length_ft": str(
            stock_length
        ),

        "stock_quantity": stock_quantity,

        "out_of_stock": (
            stock.out_of_stock
            if stock
            else False
        ),

        "category_type": category_name,

    })


# ==========================================================
# STOCK DETAIL
# ==========================================================

def stock_detail(request, id):

    stock = get_object_or_404(
        ProductStock,
        id=id
    )

    return render(
        request,
        "products/stock_detail.html",
        {
            "stock": stock
        }
    )