from django.urls import path, include,re_path
from rest_framework import routers
from app_roll import views

router = routers.DefaultRouter()

router.register(r'mesa',views.MesaViewSet)
router.register(r'rol',views.MesaHasUsuarioViewSet)
router.register(r'personaje',views.PersonajeViewSet)
router.register(r'pjconocido',views.PjConocidoViewSet)
router.register(r'atributo',views.AtributoViewSet)
router.register(r'equipamiento',views.EquipamientoViewSet)
router.register(r'habilidades',views.HabilidadViewSet)




urlpatterns = [
    path('', include(router.urls)),
    re_path('login',views.login),
    re_path('register',views.register),
    re_path('profile',views.profile),
    path('mesas/gamemaster/<int:user_id>/', views.mesas_gamemaster, name='mesas_gamemaster'),
    path('mesas/create/', views.MesaCreateView.as_view(), name='mesa-create'),
    path('mesas/<int:mesa_id>/crear_personaje_basico/', views.crear_personaje_basico, name='crear_personaje_basico'),
    path('mesas/<int:mesa_id>/personajes/', views.listar_personajes_mesa, name='listar_personajes_mesa'),

]
