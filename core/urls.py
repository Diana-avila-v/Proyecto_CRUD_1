from django.urls import path
from core import views

app_name='core' # define un espacio de nombre para la aplicacion
urlpatterns = [
   #urls iniciar sesion
   path('signup/', views.signup, name="signup"),
   path('signout/', views.signout, name='signout'),
   path('signin/', views.signin, name='signin'),
   # urls de vistas
   path('product_list/', views.product_List,name='product_list'),
   path('product_create/', views.product_create,name='product_create'),
   path('product_update/<int:id>/', views.product_update,name='product_update'),
   path('product_delete/<int:id>/', views.product_delete,name='product_delete'),
   # urls de marcas
   path('brand_list/', views.brand_List,name='brand_list'),
   path('brand_create/', views.brand_create, name='brand_create'),
   path('brand_update/<int:id>/', views.brand_update, name='brand_update'),
   path('brand_delete/<int:id>/', views.brand_delete, name='brand_delete'),
   # urls de proveedores
   path('supplier_list/', views.supplier_List,name='supplier_list'),
   path('add_supplier/', views.add_supplier, name='add_supplier'),
   path('edit_supplier/<int:pk>/', views.edit_supplier, name='edit_supplier'),
   path('delete_supplier/<int:pk>/', views.delete_supplier, name='delete_supplier'),
   #urls de categorias
   path('category_list/', views.category_List, name='category_list'),
   path('category_create/',views.category_create, name='category_create'),
   path('category_update/<int:id>',views.category_update, name='category_update'),
   path('category_delete/<int:id>',views.category_delete, name='category_delete'),
]