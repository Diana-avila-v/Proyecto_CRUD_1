from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from core.models import Product, Brand, Supplier, Category
import re

class ProductForm(forms.ModelForm):
    class Meta:
        model=Product
        fields=['description','price','stock','brand','categories','line','supplier','expiration_date','image','state']

class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['description', 'state']

#------Supplier importado --------------------

# Validación del número de teléfono
phone_regex = RegexValidator(regex=r'^\d{9,15}$', message="El número de teléfono debe contener entre 9 y 15 dígitos.")

# Validación de la cédula (RUC)
def valida_cedula(value):
    cedula = str(value)
    
    # Verificar que la cédula contenga solo números y tenga longitud de 10 dígitos
    if not cedula.isdigit() or len(cedula) != 10:
        raise ValidationError('La cédula debe contener exactamente 10 dígitos numéricos.')

    # Verificar el código de provincia
    provincia = int(cedula[0:2])
    if provincia < 1 or provincia > 24:
        raise ValidationError('El código de provincia (dos primeros dígitos) no es válido.')

    # Coeficientes para el cálculo del dígito verificador
    coeficientes = [2, 1, 2, 1, 2, 1, 2, 1, 2]
    total = 0
    
    # Calcular la suma ponderada de los dígitos
    for i in range(9):
        digito = int(cedula[i])
        coeficiente = coeficientes[i]
        producto = digito * coeficiente
        if producto > 9:
            producto -= 9
        total += producto

    # Calcular el dígito verificador esperado
    digito_verificador = (total % 10)
    if digito_verificador != 0:
        digito_verificador = 10 - digito_verificador

    # Comparar con el dígito verificador de la cédula ingresada
    if digito_verificador != int(cedula[9]):
        raise ValidationError('La cédula no es válida.')

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['description', 'price', 'stock', 'brand', 'categories', 'line', 'supplier', 'expiration_date', 'image', 'state']

#------Supplier importado --------------------

class SupplierForm(forms.ModelForm):
    phone = forms.CharField(validators=[phone_regex])  # Validación del número de teléfono

    class Meta:
        model = Supplier
        fields = ['name', 'ruc', 'address', 'phone', 'user', 'state']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not re.match(r'^[a-zA-Z\s]+$', name):  # Permitir letras y espacios
            raise forms.ValidationError("El nombre solo debe contener letras y espacios.")
        return name

    def clean_ruc(self):
        ruc = self.cleaned_data.get('ruc')
        valida_cedula(ruc)  # Usar la función de validación de cédula
        # Verificar si ya existe un proveedor con este RUC
        if Supplier.objects.filter(ruc=ruc).exists():
            raise forms.ValidationError('Ya existe un proveedor registrado con este RUC.')
        return ruc
    
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['description', 'state']