from decimal import Decimal, ROUND_HALF_UP
from .models import Order, Category
from django.utils import timezone
from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
)
from django.contrib.auth.models import User
from django.contrib.auth.decorators import (
    login_required,
    user_passes_test,
)
from django.http import (
    JsonResponse,
    HttpResponse,
)
from django.db import transaction

from .models import Order
from .forms import OrderForm

from products.models import (
    Product,
    ProductStock,
    SubCategory,
    Category,
)

from openpyxl import Workbook
from openpyxl.styles import (
    Font,
    Alignment,
    Border,
    Side,
    PatternFill,
)


# ==========================================================
# ADMIN CHECK
# ==========================================================

def is_admin(user):
    return user.is_superuser


# ==========================================================
# CATEGORY HELPERS
# ==========================================================

def normalize_category_name(name):
    if not name:
        return ""
    return (
        str(name)
        .strip()
        .lower()
        .replace(" ", "")
        .replace("-", "")
        .replace("_", "")
    )


def get_category_name_from_order(order):

    if not order.category:
        return ""

    return normalize_category_name(
        order.category.name
    )


def is_category_1(order):

    return (
        get_category_name_from_order(order)
        == "category1"
    )


def is_category_2(order):

    return (
        get_category_name_from_order(order)
        == "category2"
    )


def is_category_3(order):

    return (
        get_category_name_from_order(order)
        == "category3"
    )


def is_category_4(order):

    return (
        get_category_name_from_order(order)
        == "category4"
    )


# ==========================================================
# FEET TO METER
# ==========================================================

def convert_length_to_meter(length):

    length = Decimal(
        str(length or 0)
    )

    if length == Decimal("100"):

        return Decimal("30.50")

    elif length == Decimal("50"):

        return Decimal("15.25")

    elif length == Decimal("7"):

        return Decimal("2.13")

    elif length == Decimal("3"):

        return Decimal("0.91")

    return (
        length * Decimal("0.305")
    ).quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP
    )


# ==========================================================
# PRODUCT STOCK
# ==========================================================

def get_product_stock(product):

    if not product:
        return None

    return (
        ProductStock.objects
        .filter(
            product_id=product.id
        )
        .first()
    )


def get_available_categories(user):
    # ADMIN CAN SEE ALL CATEGORIES
    if user.is_superuser or user.is_staff:
        return Category.objects.all().order_by("name")

    # SALES USER SEES ONLY CATEGORIES WITH AVAILABLE STOCK
    available_category_ids = (
        ProductStock.objects.filter(
            out_of_stock=False,
            product__category__isnull=False,
        )
        .values("product__category_id")
        .distinct()
    )

    return Category.objects.filter(
        id__in=available_category_ids
    ).order_by("name")


# ==========================================================
# ORDER LIST
# ==========================================================

@login_required
def order_list(request):

    location = request.GET.get(
        "location",
        ""
    )

    selected_status = request.GET.get(
        "status",
        ""
    )

    selected_sales_member = request.GET.get(
        "sales_member",
        ""
    )

    sales_members = (
        User.objects
        .filter(
            is_active=True,
            is_superuser=False
        )
        .order_by("username")
    )


    # ======================================================
    # ADMIN
    # ======================================================

    if request.user.is_superuser:

        orders = (
            Order.objects
            .select_related(
                "sales_member",
                "product",
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

        if location:

            orders = orders.filter(
                location=location
            )

        if selected_status:

            orders = orders.filter(
                status=selected_status
            )

        if selected_sales_member:

            orders = orders.filter(
                sales_member_id=selected_sales_member
            )


    # ======================================================
    # SALES MEMBER
    # ======================================================

    else:

        orders = (
            Order.objects
            .filter(
                sales_member=request.user
            )
            .select_related(
                "sales_member",
                "product",
                "category",
                "subcategory",
                "brand",
                "thickness",
                "colour",
                "design",
            )
            .order_by("-id")
        )

        if location:

            orders = orders.filter(
                location=location
            )

        if selected_status:

            orders = orders.filter(
                status=selected_status
            )


    return render(
        request,
        "orders/order_list.html",
        {
            "orders": orders,
            "selected_location": location,
            "selected_status": selected_status,
            "sales_members": sales_members,
            "selected_sales_member": selected_sales_member,
        }
    )


# ==========================================================
# GET SUBCATEGORIES
# ==========================================================

@login_required
def get_subcategories(request):

    category_id = request.GET.get(
        "category_id"
    )

    if not category_id:

        return JsonResponse(
            {
                "subcategories": []
            }
        )


    subcategories = (
        SubCategory.objects
        .filter(
            category_id=category_id
        )
        .order_by("name")
    )


    data = []

    for subcategory in subcategories:

        data.append(
            {
                "id": subcategory.id,
                "name": subcategory.name,
            }
        )


    return JsonResponse(
        {
            "subcategories": data
        }
    )


# ==========================================================
# GET PRODUCTS
# ==========================================================

@login_required
def get_products(request):

    category_id = request.GET.get(
        "category_id"
    )

    subcategory_id = request.GET.get(
        "subcategory_id"
    )


    if not category_id:

        return JsonResponse(
            {
                "products": []
            }
        )


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
        .filter(
            category_id=category_id
        )
    )


    if subcategory_id:

        products = products.filter(
            subcategory_id=subcategory_id
        )


    # ======================================================
    # NORMAL USERS SEE ONLY PRODUCTS WITH AVAILABLE STOCK
    # ======================================================

    if not request.user.is_superuser:

        available_product_ids = (
            ProductStock.objects
            .filter(
                out_of_stock=False
            )
            .values_list(
                "product_id",
                flat=True
            )
        )

        products = products.filter(
            id__in=available_product_ids
        )


    products = products.order_by(
        "product_name",
        "id",
    )


    data = []


    for product in products:

        stock = get_product_stock(product)

        available_length = Decimal("0.00")
        available_quantity = 0


        if stock:

            available_length = Decimal(
                str(stock.length_ft or 0)
            )

            available_quantity = int(
                stock.quantity or 0
            )


        data.append(
            {
                "id": product.id,

                "name": (
                    product.product_name
                    or f"Product {product.id}"
                ),

                "category_id": (
                    product.category_id
                ),

                "subcategory_id": (
                    product.subcategory_id
                    or ""
                ),

                "subcategory": (
                    product.subcategory.name
                    if product.subcategory
                    else ""
                ),

                "width_ft": (
                    str(product.width_ft)
                    if product.width_ft is not None
                    else ""
                ),

                "colour_id": (
                    product.colour_id
                    or ""
                ),

                "colour": (
                    product.colour.name
                    if product.colour
                    else ""
                ),

                "brand_id": (
                    product.brand_id
                    or ""
                ),

                "brand": (
                    product.brand.name
                    if product.brand
                    else ""
                ),

                "thickness_id": (
                    product.thickness_id
                    or ""
                ),

                "thickness": (
                    product.thickness.name
                    if product.thickness
                    else ""
                ),

                "design_id": (
                    product.design_id
                    or ""
                ),

                "design": (
                    product.design.name
                    if product.design
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
                    available_length
                ),

                "stock_quantity": (
                    available_quantity
                ),
            }
        )


    return JsonResponse(
        {
            "products": data
        }
    )

# ==========================================================
# GET PRODUCT DETAILS
# ==========================================================

@login_required
def get_product_details(request):

    category_id = request.GET.get("category_id")
    subcategory_id = request.GET.get("subcategory_id")
    thickness_id = request.GET.get("thickness_id")
    width = request.GET.get("width")
    design_id = request.GET.get("design_id")
    colour_id = request.GET.get("colour_id")
    brand_id = request.GET.get("brand_id")

    # ======================================================
    # CATEGORY IS REQUIRED
    # ======================================================

    if not category_id:
        return JsonResponse({
            "thicknesses": [],
            "widths": [],
            "designs": [],
            "colours": [],
            "brands": [],
            "product": None,
        })

    # ======================================================
    # BASE PRODUCTS
    # ======================================================

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
        .filter(category_id=category_id)
    )

    # ======================================================
    # SUBCATEGORY
    # ======================================================

    if subcategory_id:
        products = products.filter(
            subcategory_id=subcategory_id
        )

    # ======================================================
    # THICKNESS OPTIONS
    # ======================================================

    thicknesses = (
        products
        .exclude(thickness__isnull=True)
        .values(
            "thickness__id",
            "thickness__name"
        )
        .distinct()
        .order_by("thickness__name")
    )

    thickness_data = []

    for item in thicknesses:
        thickness_data.append({
            "id": item["thickness__id"],
            "name": item["thickness__name"],
        })

    # ======================================================
    # FILTER THICKNESS
    # ======================================================

    if thickness_id:
        products = products.filter(
            thickness_id=thickness_id
        )

    # ======================================================
    # WIDTH OPTIONS
    # ======================================================

    widths = (
        products
        .exclude(width_ft__isnull=True)
        .values_list(
            "width_ft",
            flat=True
        )
        .distinct()
        .order_by("width_ft")
    )

    width_data = []

    for item in widths:
        width_data.append({
            "id": str(item),
            "name": str(item),
        })

    # ======================================================
    # FILTER WIDTH
    # ======================================================

    if width:
        products = products.filter(
            width_ft=width
        )

    # ======================================================
    # DESIGN OPTIONS
    # ======================================================

    designs = (
        products
        .exclude(design__isnull=True)
        .values(
            "design__id",
            "design__name"
        )
        .distinct()
        .order_by("design__name")
    )

    design_data = []

    for item in designs:
        design_data.append({
            "id": item["design__id"],
            "name": item["design__name"],
        })

    # ======================================================
    # FILTER DESIGN
    # ======================================================

    if design_id:
        products = products.filter(
            design_id=design_id
        )

    # ======================================================
    # COLOUR OPTIONS
    # ======================================================

    colours = (
        products
        .exclude(colour__isnull=True)
        .values(
            "colour__id",
            "colour__name"
        )
        .distinct()
        .order_by("colour__name")
    )

    colour_data = []

    for item in colours:
        colour_data.append({
            "id": item["colour__id"],
            "name": item["colour__name"],
        })

    # ======================================================
    # FILTER COLOUR
    # ======================================================

    if colour_id:
        products = products.filter(
            colour_id=colour_id
        )

    # ======================================================
    # BRAND OPTIONS
    # ======================================================

    brands = (
        products
        .exclude(brand__isnull=True)
        .values(
            "brand__id",
            "brand__name"
        )
        .distinct()
        .order_by("brand__name")
    )

    brand_data = []

    for item in brands:
        brand_data.append({
            "id": item["brand__id"],
            "name": item["brand__name"],
        })

    # ======================================================
    # FILTER BRAND
    # ======================================================

    if brand_id:
        products = products.filter(
            brand_id=brand_id
        )

    # ======================================================
    # FINAL PRODUCT
    # ======================================================

    product = products.order_by(
        "product_name",
        "id"
    ).first()

    product_data = None

    if product:

        product_data = {
            "id": product.id,

            "name": (
                product.product_name
                or str(product)
            ),

            "width_ft": (
                str(product.width_ft)
                if product.width_ft is not None
                else ""
            ),

            "size": (
                product.size
                or ""
            ),
        }

    # ======================================================
    # RESPONSE
    # ======================================================

    return JsonResponse({

        "thicknesses": thickness_data,

        "widths": width_data,

        "designs": design_data,

        "colours": colour_data,

        "brands": brand_data,

        "product": product_data,

    })



@login_required
def add_order(request):

    categories = Category.objects.all().order_by("name")

    if request.method == "POST":

        form = OrderForm(
            request.POST,
            categories=categories
        )

        if form.is_valid():

            try:
                with transaction.atomic():

                    # -----------------------------------------
                    # CREATE ORDER
                    # -----------------------------------------

                    order = form.save(commit=False)

                    order.sales_member = request.user
                    order.order_taken_by = request.user


                    # -----------------------------------------
                    # CATEGORY FROM SUBCATEGORY
                    # -----------------------------------------

                    if (
                        not order.category
                        and order.subcategory
                        and order.subcategory.category
                    ):
                        order.category = order.subcategory.category


                    # -----------------------------------------
                    # FIND SELECTED PRODUCT
                    # -----------------------------------------

                    selected_product = order.product

                    if not selected_product:

                        product_filters = {}

                        # CATEGORY
                        if order.category:
                            product_filters["category"] = order.category

                        # SUBCATEGORY
                        if order.subcategory:
                            product_filters["subcategory"] = order.subcategory

                        # THICKNESS
                        if order.thickness:
                            product_filters["thickness"] = order.thickness

                        # WIDTH
                        if order.width_ft is not None:
                            product_filters["width_ft"] = order.width_ft

                        # DESIGN
                        if order.design:
                            product_filters["design"] = order.design

                        # COLOUR
                        if order.colour:
                            product_filters["colour"] = order.colour

                        # BRAND
                        if order.brand:
                            product_filters["brand"] = order.brand


                        selected_product = Product.objects.filter(
                            **product_filters
                        ).first()


                        if selected_product:
                            order.product = selected_product


                    # -----------------------------------------
                    # COPY PRODUCT DETAILS
                    # -----------------------------------------

                    if selected_product:

                        order.category = selected_product.category
                        order.subcategory = selected_product.subcategory

                        if selected_product.subcategory:
                            order.subcategory_text = (
                                selected_product.subcategory.name
                            )


                        # THICKNESS
                        order.thickness = selected_product.thickness


                        # WIDTH
                        if selected_product.width_ft is not None:
                            order.width_ft = selected_product.width_ft


                        # DESIGN
                        order.design = selected_product.design


                        # COLOUR
                        order.colour = selected_product.colour


                        # BRAND
                        order.brand = selected_product.brand


                        if selected_product.colour:
                            order.colour_text = (
                                selected_product.colour.name
                            )


                        if selected_product.design:
                            order.design_text = (
                                selected_product.design.name
                            )


                        order.core_number = (
                            selected_product.core_number or ""
                        )


                        order.size_text = (
                            selected_product.size or ""
                        )


                        # RATE
                        if (
                            selected_product.sqt_rate is not None
                            and not order.rate
                        ):
                            order.rate = Decimal(
                                str(selected_product.sqt_rate)
                            )


                    # -----------------------------------------
                    # CATEGORY NAME
                    # -----------------------------------------

                    category_name = ""

                    if order.category:
                        category_name = (
                            order.category.name
                            .strip()
                            .lower()
                            .replace(" ", "")
                            .replace("-", "")
                            .replace("_", "")
                        )


                    # -----------------------------------------
                    # CATEGORY 1 AND CATEGORY 2
                    # LENGTH × RATE
                    # -----------------------------------------

                    if category_name in ["category1", "category2"]:

                        requested_length = Decimal(
                            str(order.length_ft or 0)
                        )

                        if requested_length <= 0:

                            form.add_error(
                                "length_ft",
                                "Please enter length greater than 0."
                            )

                            raise ValueError(
                                "Invalid length"
                            )


                        order.amount = (
                            requested_length
                            * Decimal(str(order.rate or 0))
                        ).quantize(
                            Decimal("0.01"),
                            rounding=ROUND_HALF_UP
                        )

                        order.sq_mtr = Decimal("0.00")
                        order.sqm_price = Decimal("0.00")


                    # -----------------------------------------
                    # CATEGORY 3
                    # QUANTITY × RATE
                    # -----------------------------------------

                    elif category_name == "category3":

                        requested_quantity = int(
                            order.sheets or 0
                        )

                        if requested_quantity <= 0:

                            form.add_error(
                                "sheets",
                                "Please enter quantity greater than 0."
                            )

                            raise ValueError(
                                "Invalid quantity"
                            )


                        order.amount = (
                            Decimal(str(requested_quantity))
                            * Decimal(str(order.rate or 0))
                        ).quantize(
                            Decimal("0.01"),
                            rounding=ROUND_HALF_UP
                        )

                        order.sq_mtr = Decimal("0.00")
                        order.sqm_price = Decimal("0.00")


                    # -----------------------------------------
                    # CATEGORY 4
                    # LENGTH × WIDTH × QUANTITY
                    # -----------------------------------------

                    elif category_name == "category4":

                        length_meter = Decimal(
                            str(order.length_ft or 0)
                        )

                        width_meter = Decimal(
                            str(order.width_meter or 0)
                        )

                        quantity = Decimal(
                            str(order.sheets or 1)
                        )


                        if length_meter <= 0:

                            form.add_error(
                                "length_ft",
                                "Please enter length in meters."
                            )

                            raise ValueError(
                                "Invalid length"
                            )


                        if width_meter <= 0:

                            form.add_error(
                                "width_meter",
                                "Please enter width in meters."
                            )

                            raise ValueError(
                                "Invalid width"
                            )


                        order.sq_mtr = (
                            length_meter
                            * width_meter
                            * quantity
                        ).quantize(
                            Decimal("0.01"),
                            rounding=ROUND_HALF_UP
                        )


                        order.sqm_price = (
                            order.sq_mtr
                            * Decimal(str(order.rate or 0))
                        ).quantize(
                            Decimal("0.01"),
                            rounding=ROUND_HALF_UP
                        )


                        order.amount = order.sqm_price


                    # -----------------------------------------
                    # OTHER CATEGORY
                    # -----------------------------------------

                    else:

                        if order.amount is None:
                            order.amount = Decimal("0.00")


                    # -----------------------------------------
                    # SAVE ORDER
                    # -----------------------------------------

                    order.status = form.cleaned_data["status"]

                    order.save()


                return redirect("order_list")


            except Exception as e:
                print("ORDER SAVE ERROR:", e)
                form.add_error(None, str(e))

        else:
            print("FORM ERRORS:")
            print(form.errors)


    else:

        form = OrderForm(
            categories=categories
        )


    return render(
        request,
        "orders/order_form.html",
        {
            "form": form,
            "categories": categories,
        }
    )
# ==========================================================
# EDIT ORDER
# ==========================================================

@login_required
def edit_order(request, id):

    if request.user.is_superuser:

        order = get_object_or_404(
            Order,
            id=id
        )

    else:

        order = get_object_or_404(
            Order,
            id=id,
            sales_member=request.user
        )


    categories = get_available_categories(
        request.user
    )


    if request.method == "POST":

        form = OrderForm(
            request.POST,
            instance=order
        )


        if form.is_valid():

            with transaction.atomic():

                old_product = order.product

                old_category_name = (
                    get_category_name_from_order(
                        order
                    )
                )

                old_length = Decimal(
                    str(order.length_ft or 0)
                )

                old_quantity = int(
                    order.sheets or 0
                )


                updated_order = form.save(
                    commit=False
                )

                updated_order.sales_member = (
                    order.sales_member
                )

                updated_order.order_taken_by = (
                    order.order_taken_by
                )

                new_product = (
                    updated_order.product
                )


                if not new_product:

                    form.add_error(
                        "product",
                        "Please select a product."
                    )

                    return render(
                        request,
                        "orders/order_form.html",
                        {
                            "form": form,
                            "order": order,
                            "categories": categories,
                        }
                    )


                updated_order.category = (
                    new_product.category
                )

                updated_order.subcategory = (
                    new_product.subcategory
                )

                updated_order.brand = (
                    new_product.brand
                )

                updated_order.thickness = (
                    new_product.thickness
                )

                updated_order.colour = (
                    new_product.colour
                )

                updated_order.design = (
                    new_product.design
                )


                updated_order.width_ft = (
                    Decimal(
                        str(
                            new_product.width_ft
                            or 0
                        )
                    )
                )

                updated_order.width_meter = (
                    updated_order.width_ft
                    * Decimal("0.3048")
                ).quantize(
                    Decimal("0.0001"),
                    rounding=ROUND_HALF_UP
                )


                new_category_name = (
                    get_category_name_from_order(
                        updated_order
                    )
                )


                new_length = Decimal(
                    str(
                        updated_order.length_ft
                        or 0
                    )
                )

                new_quantity = int(
                    updated_order.sheets
                    or 0
                )


                old_is_length = (
                    old_category_name
                    in [
                        "category1",
                        "category2",
                    ]
                )

                old_is_quantity = (
                    old_category_name
                    == "category3"
                )

                new_is_length = (
                    new_category_name
                    in [
                        "category1",
                        "category2",
                    ]
                )

                new_is_quantity = (
                    new_category_name
                    == "category3"
                )


                # ==============================================
                # VALIDATE
                # ==============================================

                if (
                    new_is_length
                    and new_length <= 0
                ):

                    form.add_error(
                        "length_ft",
                        "Length must be greater than 0."
                    )

                    return render(
                        request,
                        "orders/order_form.html",
                        {
                            "form": form,
                            "order": order,
                            "categories": categories,
                        }
                    )


                if (
                    new_is_quantity
                    and new_quantity <= 0
                ):

                    form.add_error(
                        "sheets",
                        "Quantity must be greater than 0."
                    )

                    return render(
                        request,
                        "orders/order_form.html",
                        {
                            "form": form,
                            "order": order,
                            "categories": categories,
                        }
                    )


                # ==============================================
                # RESTORE OLD STOCK
                # ==============================================

                old_stock = None

                if old_product:

                    old_stock = (
                        ProductStock.objects
                        .select_for_update()
                        .filter(
                            product_id=
                            old_product.id
                        )
                        .first()
                    )


                if old_stock:

                    if old_is_length:

                        old_stock.length_ft = (
                            Decimal(
                                str(
                                    old_stock.length_ft
                                    or 0
                                )
                            )
                            + old_length
                        )

                    elif old_is_quantity:

                        old_stock.quantity = (
                            int(
                                old_stock.quantity
                                or 0
                            )
                            + old_quantity
                        )

                    old_stock.out_of_stock = False

                    old_stock.save()


                # ==============================================
                # GET NEW STOCK
                # ==============================================

                new_stock = (
                    ProductStock.objects
                    .select_for_update()
                    .filter(
                        product_id=
                        new_product.id
                    )
                    .first()
                )


                # ==============================================
                # NEW LENGTH STOCK
                # ==============================================

                if new_is_length:

                    length_meter = (
                        convert_length_to_meter(
                            new_length
                        )
                    )

                    updated_order.sq_mtr = (
                        length_meter
                        * updated_order.width_meter
                    ).quantize(
                        Decimal("0.01"),
                        rounding=ROUND_HALF_UP
                    )

                    updated_order.sqm_price = (
                        updated_order.sq_mtr
                        * Decimal(
                            str(
                                updated_order.rate
                                or 0
                            )
                        )
                    ).quantize(
                        Decimal("0.01"),
                        rounding=ROUND_HALF_UP
                    )

                    updated_order.amount = (
                        updated_order.sqm_price
                    )


                    if new_stock is None:

                        updated_order.status = (
                            "Out of Stock"
                        )

                        updated_order.save()

                        return redirect(
                            "order_list"
                        )


                    available_length = Decimal(
                        str(
                            new_stock.length_ft
                            or 0
                        )
                    )


                    if new_length > available_length:

                        updated_order.status = (
                            "Out of Stock"
                        )

                        updated_order.save()

                        return redirect(
                            "order_list"
                        )


                    new_stock.length_ft = (
                        available_length
                        - new_length
                    )

                    new_stock.out_of_stock = (
                        new_stock.length_ft
                        <= Decimal("0.00")
                    )

                    new_stock.save()


                # ==============================================
                # NEW QUANTITY STOCK
                # ==============================================

                elif new_is_quantity:

                    updated_order.amount = (
                        Decimal(
                            str(new_quantity)
                        )
                        * Decimal(
                            str(
                                updated_order.rate
                                or 0
                            )
                        )
                    ).quantize(
                        Decimal("0.01"),
                        rounding=ROUND_HALF_UP
                    )


                    if new_stock is None:

                        updated_order.status = (
                            "Out of Stock"
                        )

                        updated_order.save()

                        return redirect(
                            "order_list"
                        )


                    available_quantity = int(
                        new_stock.quantity
                        or 0
                    )


                    if (
                        new_quantity
                        > available_quantity
                    ):

                        updated_order.status = (
                            "Out of Stock"
                        )

                        updated_order.save()

                        return redirect(
                            "order_list"
                        )


                    new_stock.quantity = (
                        available_quantity
                        - new_quantity
                    )

                    new_stock.out_of_stock = (
                        new_stock.quantity <= 0
                    )

                    new_stock.save()


                updated_order.save()


            return redirect(
                "order_list"
            )


    else:

        form = OrderForm(
            instance=order
        )


    return render(
        request,
        "orders/order_form.html",
        {
            "form": form,
            "order": order,
            "categories": categories,
        }
    )


# ==========================================================
# DELETE ORDER
# ==========================================================

@login_required
def delete_order(request, id):

    if request.user.is_superuser:

        order = get_object_or_404(
            Order,
            id=id
        )

    else:

        order = get_object_or_404(
            Order,
            id=id,
            sales_member=request.user
        )


    if request.method == "POST":

        with transaction.atomic():

            product = order.product


            if product:

                stock = (
                    ProductStock.objects
                    .select_for_update()
                    .filter(
                        product_id=product.id
                    )
                    .first()
                )


                if stock is None:

                    stock = (
                        ProductStock.objects
                        .create(
                            product=product,
                            length_ft=Decimal(
                                "0.00"
                            ),
                            quantity=0,
                        )
                    )


                if (
                    is_category_1(order)
                    or is_category_2(order)
                ):

                    stock.length_ft = (
                        Decimal(
                            str(
                                stock.length_ft
                                or 0
                            )
                        )
                        + Decimal(
                            str(
                                order.length_ft
                                or 0
                            )
                        )
                    )


                elif is_category_3(order):

                    stock.quantity = (
                        int(
                            stock.quantity
                            or 0
                        )
                        + int(
                            order.sheets
                            or 0
                        )
                    )


                stock.out_of_stock = False

                stock.save()


            order.delete()


        return redirect(
            "order_list"
        )


    return render(
        request,
        "orders/order_confirm_delete.html",
        {
            "order": order
        }
    )


# ==========================================================
# EXPORT ORDERS EXCEL
# ==========================================================

@login_required
def export_orders_excel(request):

    orders = (
        Order.objects
        .select_related(
            "product",
            "category",
            "subcategory",
            "brand",
            "thickness",
            "colour",
            "design",
            "sales_member",
            "order_taken_by",
        )
        .all()
        .order_by("customer_name", "id")
    )


    status = request.GET.get(
        "status"
    )


    if status:

        orders = orders.filter(
            status=status
        )


    workbook = Workbook()

    worksheet = workbook.active

    worksheet.title = "Orders"


    headers = [
        "SL No",
        "Customer Name",
        "Location",
        "Thickness",
        "Design",
        "Colour",
        "Length",
        "Width",
        "Nos",
        "SQ. MTR",
        "Rate",
        "SQM Price",
        "Amount",
        "Loading From",
        "Order Taken By",
    ]

    NUM_COLUMNS = len(headers)


    # ======================================================
    # STYLES
    # ======================================================

    bold_side = Side(
        style="medium",
        color="000000",
    )

    cell_border = Border(
        left=bold_side,
        right=bold_side,
        top=bold_side,
        bottom=bold_side,
    )

    category_2_fill = PatternFill(
        fill_type="solid",
        start_color="00B050",
        end_color="00B050",
    )

    out_of_stock_fill = PatternFill(
        fill_type="solid",
        start_color="FF0000",
        end_color="FF0000",
    )

    normal_font = Font(
        bold=True,
    )

    coloured_row_font = Font(
        bold=True,
        color="FFFFFF",
    )


    for column_number, header in enumerate(
        headers,
        1
    ):

        cell = worksheet.cell(
            row=1,
            column=column_number,
            value=header
        )

        cell.font = Font(
            bold=True
        )

        cell.alignment = Alignment(
            horizontal="center",
            vertical="center"
        )

        cell.border = cell_border


    # ======================================================
    # DATA ROWS
    # ======================================================

    previous_customer_name = None


    for index, order in enumerate(
        orders,
        1
    ):

        row = index + 1

        current_customer_name = (
            order.customer_name
            or ""
        )

        display_customer_name = (
            current_customer_name
            if current_customer_name
            != previous_customer_name
            else ""
        )

        previous_customer_name = (
            current_customer_name
        )

        row_values = [
            index,
            display_customer_name,
            order.location or "",
            str(order.thickness or ""),
            str(order.design or ""),
            str(order.colour or ""),
            float(order.length_ft or 0),
            float(order.width_ft or 0),
            order.sheets or 0,
            float(order.sq_mtr or 0),
            float(order.rate or 0),
            float(order.sqm_price or 0),
            float(order.amount or 0),
            order.loading_from or "",
            str(order.order_taken_by or ""),
        ]

        # --------------------------------------------------
        # ROW COLOUR
        # OUT OF STOCK TAKES PRIORITY OVER CATEGORY 2 GREEN
        # --------------------------------------------------

        row_fill = None

        if order.status == "Out of Stock":

            row_fill = out_of_stock_fill

        elif is_category_2(order):

            row_fill = category_2_fill


        for column_number in range(
            1,
            NUM_COLUMNS + 1
        ):

            cell = worksheet.cell(
                row=row,
                column=column_number,
                value=row_values[column_number - 1]
            )

            cell.border = cell_border

            cell.alignment = Alignment(
                horizontal="center",
                vertical="center"
            )

            if row_fill:

                cell.fill = row_fill

                cell.font = coloured_row_font

            else:

                cell.font = normal_font


    for column in worksheet.columns:

        max_length = 0

        column_letter = (
            column[0].column_letter
        )


        for cell in column:

            if cell.value is not None:

                max_length = max(
                    max_length,
                    len(
                        str(cell.value)
                    )
                )


        worksheet.column_dimensions[
            column_letter
        ].width = (
            max_length + 2
        )


    response = HttpResponse(
        content_type=(
            "application/vnd.openxmlformats-"
            "officedocument.spreadsheetml.sheet"
        )
    )


    response[
        "Content-Disposition"
    ] = (
        'attachment; '
        'filename="orders_report.xlsx"'
    )


    workbook.save(
        response
    )


    return response



# ==========================================================
# DISPATCH ORDER
# ==========================================================

@login_required
@user_passes_test(is_admin)
def dispatch_order(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id
    )


    if order.status == "Pending":

        order.status = "Completed"

        order.dispatch_status = "Dispatched"

        order.dispatch_date = (
            timezone.now().date()
        )

        order.dispatched_by = (
            request.user
        )

        order.save()


    return redirect(
        "order_list"
    )