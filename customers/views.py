from django.shortcuts import render, redirect, get_object_or_404

from .models import Customer
from .forms import CustomerForm


# ==========================================
# CUSTOMER LIST
# ==========================================

def customer_list(request):

    customers = Customer.objects.all().order_by("-id")

    return render(
        request,
        "customers/customer_list.html",
        {
            "customers": customers
        }
    )


# ==========================================
# ADD CUSTOMER
# ==========================================

def add_customer(request):

    if request.method == "POST":

        form = CustomerForm(request.POST)

        if form.is_valid():

            # SAVE CUSTOMER
            customer = form.save()

            print("CUSTOMER SAVED:", customer.customer_name)

            return redirect("customer_list")

        else:

            print("FORM ERRORS:")
            print(form.errors)

    else:

        form = CustomerForm()

    return render(
        request,
        "customers/customer_form.html",
        {
            "form": form
        }
    )


# ==========================================
# EDIT CUSTOMER
# ==========================================

def edit_customer(request, id):

    customer = get_object_or_404(
        Customer,
        id=id
    )

    if request.method == "POST":

        form = CustomerForm(
            request.POST,
            instance=customer
        )

        if form.is_valid():

            # SAVE UPDATED CUSTOMER
            customer = form.save()

            print("CUSTOMER UPDATED:", customer.customer_name)

            return redirect("customer_list")

        else:

            print("FORM ERRORS:")
            print(form.errors)

    else:

        form = CustomerForm(
            instance=customer
        )

    return render(
        request,
        "customers/customer_form.html",
        {
            "form": form,
            "customer": customer
        }
    )


# ==========================================
# DELETE CUSTOMER
# ==========================================

def delete_customer(request, id):

    customer = get_object_or_404(
        Customer,
        id=id
    )

    customer.delete()

    return redirect("customer_list")