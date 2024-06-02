from django.http import HttpResponse, JsonResponse, Http404
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from core.forms import ProductForm, BrandForm, CategoryForm
from core.models import Product, Brand, Category
from core.forms import SupplierForm
from core.models import Supplier
from django.db import IntegrityError  # Importación de IntegrityError
from django.contrib.auth.decorators import login_required

# Create your views here.
def signup(request):
    if request.method == "GET":
        return render(request, 'signup.html', {'form':UserCreationForm})
    else:
        if(request.POST['password1'] == request.POST['password2']):
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('home')
            except IntegrityError:
                return render(request, 'signup.html', {'form': UserCreationForm, 'error': 'El usuario ya existe'})
        return render(request, 'signup.html', {'form':UserCreationForm, 'error': 'Contraseñas no coinciden'})

def signout(request):
    logout(request)
    return redirect('home')

def signin(request):
    if request.method == "GET":
        return render(request, 'signin.html', {'form': AuthenticationForm})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {'form': AuthenticationForm, 'error': 'Usuario o contraseña incorrecta'})
        else:
            login(request, user)
            return redirect('home')

#Vista de Productos
def home(request):
   data = {
        "title1":"Autor | TeacherCode",
        "title2":"BIENVENIDO",
        'title3':"ENCUENTRA LOS MEJORES PRODUCTOS AL MEJOR PRECIO"
   }
   return render(request,'core/home.html',data)

@login_required
def product_List(request):
    data = {
        "title1": "Productos",
        "title2": "Consulta De Productos"
    }
    products = Product.objects.all() # select * from Product
    data["products"]=products
    return render(request,"core/products/list.html",data)

# crear un producto
@login_required
def product_create(request):
    data = {"title1": "Productos","title2": "Ingreso De Productos"}
    if request.method == "POST":
        #print(request.POST)
        form = ProductForm(request.POST,request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.save()
            return redirect("core:product_list")

    else:
        data["form"] = ProductForm() # controles formulario sin datos

    return render(request, "core/products/form.html", data)

# editar un producto
@login_required
def product_update(request,id):
    data = {"title1": "Productos","title2": "Edicion De Productos"}
    product = Product.objects.get(pk=id)
    if request.method == "POST":
      form = ProductForm(request.POST,request.FILES, instance=product)
      if form.is_valid():
            form.save()
            return redirect("core:product_list")
    else:
        form = ProductForm(instance=product)
        data["form"]=form
    return render(request, "core/products/form.html", data)

# eliminar un producto
@login_required
def product_delete(request,id):
    product = Product.objects.get(pk=id)
    data = {"title1":"Eliminar","title2":"Eliminar Un Producto","product":product}
    if request.method == "POST":
        product.delete()
        return redirect("core:product_list")
 
    return render(request, "core/products/delete.html", data)

# vistas de marcas: Listar marcas
@login_required
def brand_List(request):
    data = {
        "title1": "Marcas",
        "title2": "Consulta De Marcas De Productos"
    }
    brands = Brand.objects.all()
    data['brands'] = brands
    return render(request,"core/brands/list.html",data)

@login_required
def brand_create(request):
    data = {"title1": "Marcas", "title2": "Crear Nueva Marca"}
    if request.method == "POST":
        form = BrandForm(request.POST)
        if form.is_valid():
            brand = form.save(commit=False)
            if brand.description.isdigit():
                form.add_error("description", "El Marca no puede ser un número")
                data["form"] = form
                return render(request, "core/brands/form.html", data)
            brand.user = request.user
            brand.save()
            return redirect("core:brand_list")
    else:
        form = BrandForm()
    data["form"] = form
    return render(request, "core/brands/form.html", data)

@login_required
def brand_update(request, id):
    data = {"title1": "Marcas", "title2": "Editar Marca"}
    
    # Obtener la marca o devolver un error 404 si no existe
    brand = get_object_or_404(Brand, pk=id)
    
    if request.method == "POST":
        form = BrandForm(request.POST, instance=brand)
        if form.is_valid():
            brand = form.save(commit=False)
            if brand.description.isdigit():
                form.add_error("description", "La Marca no puede ser un número")
                data["form"] = form
                return render(request, "core/brands/form.html", data)
            brand.save()
            return redirect("core:brand_list")
    else:
        form = BrandForm(instance=brand)
    
    data["form"] = form
    return render(request, "core/brands/form.html", data)

@login_required
def brand_delete(request, id):
    data = {"title1": "Eliminar", "title2": "Eliminar Una Marca"}
    try:
        brand = Brand.objects.get(pk=id)
    except Brand.DoesNotExist:
        raise Http404("Marca no encontrada")
    if request.method == "POST":
        brand.delete()
        return redirect("core:brand_list")
    data["brand"] = brand
    return render(request, "core/brands/delete.html", data)

#Provedor
@login_required

#------------PROOVEDOR-------------------------  
@login_required
def supplier_List(request):
    data = {
        "title1": "Proveedores",
        "title2": "Consulta De proveedores"
    }
    suppliers = Supplier.objects.all() # select * from Product
    data["suppliers"]=suppliers
    return render(request,"core/suppliers/list.html",data)
    
@login_required
def supplier_list(request):
    proveedores = Supplier.objects.all()
    return render(request, 'supplier_list.html', {'proveedores': proveedores, 'title': 'Lista de Proveedores'})

@login_required
def add_supplier(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('core:supplier_list')
    else:
        form = SupplierForm()
    return render(request, 'core/suppliers/form.html', {'form': form, 'title': 'Agregar Proveedor'})

@login_required
def edit_supplier(request, pk):
    suppliers = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=suppliers)
        if form.is_valid():
            form.save()
            return redirect('core:supplier_list')
    else:
        form = SupplierForm(instance=suppliers)
        
    return render(request, 'core/suppliers/form.html', {'form': form, 'title': 'Editar Proveedor'})

@login_required
def delete_supplier(request, pk):
    suppliers = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        suppliers.delete()
        return redirect('core:supplier_list')
    return render(request, 'core/suppliers/delete.html', {'suppliers': suppliers, 'title': 'Eliminar Proveedor', 'title2': 'Eliminar Un Proveedor'})

# vista de categorias
def category_List(request):
    data = {
        "title1": "Categorías",
        "title2": "Consulta De Categorías"
    }
    categories = Category.objects.all()         # Obtiene todas las categorías de la base de datos
    data["categories"] = categories             # Agrega las categorías al diccionario de datos
    return render(request, "core/categories/list.html",data)     # Renderiza el template con los datos

def category_create(request):
    data = {"title1": "Categorías", "title2": "Ingreso de categorías"}
    if request.method == "POST":
        form = CategoryForm(request.POST)        # Crea una instancia del formulario CategoryForm con los datos enviados en la solicitud POST.
        if form.is_valid():
            category = form.save(commit=False)   # Guarda el formulario en una instancia del modelo Category pero no lo guarda en la base de datos todavía (commit=False).
            if category.description.isdigit():
                form.add_error("description", "La Categoría no puede ser un número")
                data["form"] = form    #Añade el formulario con el error al diccionario data.
                return render(request, "core/categories/form.html", data)
            category.user = request.user
            category.save()
            return redirect("core:category_list")
    else:
        form = CategoryForm()    # Si el método no es POST, crea una instancia vacía del formulario CategoryForm.
    data["form"] = form
    return render(request, "core/categories/form.html", data)    

def category_update(request,id):
    data = {"title1": "Categorías","title2": "Edicion De Categorías"}
    # Obtener la categoría por su ID o devolver un error 404 si no existe
    category = get_object_or_404(Category, pk=id)
    
    if request.method == "POST":
      form = CategoryForm(request.POST, instance=category)
      if form.is_valid():
            category = form.save(commit=False)
            if category.description.isdigit():
                form.add_error("description", "La Categoría no puede ser un número")
                data["form"] = form
                return render(request, "core/categories/form.html", data)
            category.save()
            return redirect("core:category_list")
    else:
        form = CategoryForm(instance=category)
    data["form"]=form
    return render(request, "core/categories/form.html", data)

def category_delete(request, id):
    data = {"title1": "Eliminar", "title2": "Eliminar Una Categoría"}
    category = get_object_or_404(Category, pk=id)    
    if request.method == "POST":
        category.delete()
        return redirect("core:category_list")
    data["category"] = category
    return render(request, "core/categories/delete.html", data)
