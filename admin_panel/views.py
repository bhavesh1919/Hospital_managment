from django.shortcuts import render
from app1.models import Docter,Patient
from docter.models import Availability
from patient.models import appointment
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from .models import WebsiteSetting
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from docter.models import Speciality



from django.contrib.auth import update_session_auth_hash
from .models import AdminProfile



from django.shortcuts import render, redirect

from django.utils import timezone

from pharma.models import Product, Category ,Supplier,Purchase,Sale



def website_settings(request):
    website = WebsiteSetting.objects.first()

    return {
        "website_setting": website
    }
    
def Logout(request):
    logout(request)
    return redirect("/login/")

def admindashboard(request):
    doctors = Docter.objects.prefetch_related(
        "doctor_specialities__speciality"
    ).all()
    patients = Patient.objects.all()
    appointments = appointment.objects.select_related(
        "docter",
        "patient",
        "appointment",
    ).all().order_by("-created_at")

    doctor_count = doctors.count()
    patient_count = patients.count()
    appointment_count = appointments.count()

    revenue = appointments.aggregate(
        total=Sum("appointment__fee")
    )["total"] or 0

    return render(request, "admin_dash55.html", {
            "doctors": doctors,
            "patients": patients,
            "appointments": appointments,
            "doctor_count": doctor_count,
            "patient_count": patient_count,
            "appointment_count": appointment_count,
            "revenue": revenue,
        })


def appointment_list(request):
    appointments = appointment.objects.select_related(
        "docter",
        "patient",
        "appointment",
        "docter__profile__user",
        "patient__profile__user"
    ).prefetch_related(
        "docter__doctor_specialities__speciality"
    ).all().order_by("-created_at")
    return render(request, "appointment_list.html", {"appointments": appointments})


def doctor_list(request):
    doctors = Docter.objects.prefetch_related(
        "doctor_specialities__speciality",
        "profile__user"
    ).all()
    return render(request, "docter_list.html", {"doctors": doctors})


def patient_list(request):

    patient = Patient.objects.all()

    return render(request, "patient.html",{"patient":patient})


def patient_copy(request):
    return render(request, "patient copy 8.html")





def profile(request):

    if not request.user.is_superuser:
        return redirect("/")

    admin = request.user

    admin_profile, created = AdminProfile.objects.get_or_create(
        user=admin
    )

   
    if request.method == "POST" and "update_profile" in request.POST:

        admin.first_name = request.POST.get("first_name", "")
        admin.last_name = request.POST.get("last_name", "")
        admin.email = request.POST.get("email", "")

        if request.FILES.get("profile_photo"):
            admin_profile.profile_photo = request.FILES["profile_photo"]

        admin.save()
        admin_profile.save()

        messages.success(
            request,
            "Profile updated successfully."
        )

        return redirect("/profile/")


    if request.method == "POST" and "change_password" in request.POST:

        old_password = request.POST.get("old_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if not admin.check_password(old_password):
            messages.error(request, "Old password is incorrect.")
            return redirect("/profile/")

        if new_password != confirm_password:
            messages.error(
                request,
                "New password and confirm password do not match."
            )
            return redirect("/profile/")

        if len(new_password) < 8:
            messages.error(
                request,
                "Password must contain at least 8 characters."
            )
            return redirect("/profile/")

        admin.set_password(new_password)
        admin.save()

        update_session_auth_hash(request, admin)

        messages.success(
            request,
            "Password changed successfully."
        )

        return redirect("/profile/")

    return render(request, "profile.html", {
        "admin": admin,
        "admin_profile": admin_profile,
    })


def report(request):
    return render(request, "report.html")


def review(request):
    return render(request, "review1.html")

def settings(request):

    setting, created = WebsiteSetting.objects.get_or_create(id=1)

    if request.method == "POST":

        setting.website_name = request.POST.get("website_name")

        if request.FILES.get("website_logo"):
            setting.website_logo = request.FILES.get("website_logo")

        if request.FILES.get("favicon"):
            setting.favicon = request.FILES.get("favicon")

        setting.save()

        return redirect("/settings/")

    return render(
        request,
        "settings.html",
        {
            "setting": setting,
            "website_setting": setting,
        }
    )


def specialities(request):
    return render(request, "specialities.html")


def transaction_list(request):
    return render(request, "transaction_list.html")






@login_required
def specialities(request):

    speciality_list = Speciality.objects.prefetch_related(
        "doctor_specialities__doctor"
    ).all().order_by("id")

    context = {
        "specialities": speciality_list,
    }

    return render(
        request,
        "specialities.html",
        context
    )

@login_required
def add_speciality(request):

    if request.method == "POST":

        name = request.POST.get("name", "").strip()

        if not name:

            messages.error(
                request,
                "Please enter speciality name."
            )

            return redirect("specialities")

        if Speciality.objects.filter(
            name__iexact=name
        ).exists():

            messages.error(
                request,
                "This speciality already exists."
            )

            return redirect("specialities")

        Speciality.objects.create(
            name=name
        )

        messages.success(
            request,
            "Speciality added successfully."
        )

        return redirect("specialities")

    return redirect("specialities")



@login_required
def edit_speciality(request, speciality_id):

    speciality = get_object_or_404(
        Speciality,
        id=speciality_id
    )

    if request.method == "POST":

        name = request.POST.get("name", "").strip()

        if not name:

            messages.error(
                request,
                "Please enter speciality name."
            )

            return redirect("specialities")

        duplicate = Speciality.objects.filter(
            name__iexact=name
        ).exclude(
            id=speciality.id
        ).exists()

        if duplicate:

            messages.error(
                request,
                "This speciality already exists."
            )

            return redirect("specialities")

        speciality.name = name
        speciality.save()

        messages.success(
            request,
            "Speciality updated successfully."
        )

    return redirect("specialities")



@login_required
def delete_speciality(request, speciality_id):

    speciality = get_object_or_404(
        Speciality,
        id=speciality_id
    )

    speciality.delete()

    messages.success(
        request,
        "Speciality deleted successfully."
    )

    return redirect("specialities")



def delete_doctor(request, id):

    if request.method == "POST":

        doctor = get_object_or_404(Docter, id=id)

        user = doctor.profile.user

        doctor.delete()

        user.delete()

    return redirect('/doctors/')




def delete_patient(request, id):

    if request.method == "POST":

        patient = get_object_or_404(Patient, id=id)

        patient.delete()

    return redirect('/patients/')



from patient.models import appointment as Appointment


@login_required(login_url="/login/")
def approve_appointment(request, id):

    if not request.user.is_superuser:
        messages.error(request, "You are not authorized.")
        return redirect("/")

    app = get_object_or_404(Appointment, id=id)

    app.status = "Approved"
    app.save()

    messages.success(request, "Appointment approved successfully.")

    return redirect("/appointments_list/")


@login_required(login_url="/login/")
def reject_appointment(request, id):

    if not request.user.is_superuser:
        messages.error(request, "You are not authorized.")
        return redirect("/")

    app = get_object_or_404(Appointment, id=id)

    app.status = "Rejected"
    app.save()

    messages.success(request, "Appointment rejected successfully.")

    return redirect("/appointments_list/")




def purchase(request):
    purchases = Purchase.objects.all().order_by('-id')

    return render(request, 'purchase.html', {
        'purchases': purchases
    })






def add_purchase(request):

    suppliers = Supplier.objects.all()
    products = Product.objects.all()

    if request.method == "POST":

        supplier_id = request.POST.get("supplier")
        product_id = request.POST.get("product")
        quantity = request.POST.get("quantity")
        purchase_price = request.POST.get("purchase_price")

        Purchase.objects.create(
            supplier_id=supplier_id,
            product_id=product_id,
            quantity=quantity,
            purchase_price=purchase_price
        )

        return redirect("purchase")

    return render(request, "add-purchase.html", {
        "suppliers": suppliers,
        "products": products
    })

def sales(request):
    return render(request, 'sales.html')


def transactions_list(request):
    return render(request, 'transactions-list.html')


# =========================
# ADD PAGES
# =========================





def add_supplier(request):

    if request.method == "POST":

        name = request.POST.get("name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        address = request.POST.get("address")

        Supplier.objects.create(
            name=name,
            phone=phone,
            email=email,
            address=address
        )

        return redirect('/supplier/add/')

    return render(request, 'add-supplier.html')


# =========================
# EDIT PAGES
# =========================

def edit_product(request, id):
    return render(request, 'edit-product.html')


def edit_purchase(request, id):
    return render(request, 'edit-purchase.html')


# =========================
# EXPIRED PRODUCTS
# =========================

def expired(request):
    products = Product.objects.filter(
        expiry_date__lt=timezone.now().date()
    )

    return render(request, 'expired.html', {
        'products': products
    })

def outstock(request):
    return render(request, 'outstock.html')






# =========================
# Pharma PRODUCTS
# =========================


def products(request):

    products = Product.objects.select_related(
        'category'
    ).all().order_by('-id')

    return render(
        request,
        'products.html',
        {
            'products': products
        }
    )


def add_product(request):

    categories = Category.objects.all()

    if request.method == 'POST':

        name = request.POST.get('brand_name2')
        category_id = request.POST.get('category')
        price = request.POST.get('Price2')
        stock = request.POST.get('quantity2')
        discount = request.POST.get('discount2')
        description = request.POST.get('about')
        brand = request.POST.get('brand')
        image = request.FILES.get('images[]')

        expiry_date = request.POST.get('expiry_date')

        # Check required fields
        if not name:
            messages.error(request, 'Product name is required.')
            return render(
                request,
                'add_product.html',
                {'categories': categories}
            )

        if not category_id:
            messages.error(request, 'Please select a category.')
            return render(
                request,
                'add_product.html',
                {'categories': categories}
            )

        if not price:
            messages.error(request, 'Price is required.')
            return render(
                request,
                'add_product.html',
                {'categories': categories}
            )

        if not stock:
            messages.error(request, 'Quantity is required.')
            return render(
                request,
                'add_product.html',
                {'categories': categories}
            )

        # Get category
        category = Category.objects.get(
            id=category_id
        )

        # Create product
        Product.objects.create(
            name=name,
            category=category,
            brand=brand,
            price=price,
            stock=stock,
            discount=discount or 0,
            description=description or '',
            expiry_date=expiry_date or None,
            image=image
            
        )

        messages.success(
            request,
            'Product added successfully.'
        )

        return redirect('products')

    return render(
        request,
        'add-product.html',
        {
            'categories': categories
        }
    )



def delete_product(request, id):

    product = get_object_or_404(Product, id=id)

    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully.')

    return redirect('products')


from django.shortcuts import render

from django.utils import timezone


def outstock(request):

    products = Product.objects.select_related('category').filter(
        stock__lte=5
    ).order_by('stock')

    return render(
        request,
        'outstock.html',
        {
            'products': products,
            'today': timezone.localdate(),
        }
    )



def categories(request):
    category_list = Category.objects.all().order_by('-id')

    return render(
        request,
        'categories.html',
        {
            'categories': category_list
        }
    )


def add_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')

        if not name:
            messages.error(request, 'Category name is required.')
            return redirect('categories')

        if Category.objects.filter(name=name).exists():
            messages.error(request, 'Category already exists.')
            return redirect('categories')

        Category.objects.create(name=name)

        messages.success(request, 'Category added successfully.')
        return redirect('categories')

    return redirect('categories')


def edit_category(request, id):
    category = get_object_or_404(Category, id=id)

    if request.method == 'POST':
        name = request.POST.get('name')

        if not name:
            messages.error(request, 'Category name is required.')
            return redirect('categories')

        if Category.objects.filter(name=name).exclude(id=id).exists():
            messages.error(request, 'Category already exists.')
            return redirect('categories')

        category.name = name
        category.save()

        messages.success(request, 'Category updated successfully.')
        return redirect('categories')

    return redirect('categories')


def delete_category(request, id):
    category = get_object_or_404(Category, id=id)

    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully.')

    return redirect('categories')