"""
URL configuration for conference_room project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from main.views import (RoomAddView, HomePageView, RoomsDisplayView, delete_room_view, EditRoomView, ReserveRoom, room_details,)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomePageView.as_view(), name='home'),
    path('room/new/', RoomAddView.as_view(), name='new_room'),
    path('room/', RoomsDisplayView.as_view(), name='list_rooms'),
    # path('room/<int:room_id>/', , name='make_reservation'),
    path('room/delete/<int:id>', delete_room_view, name='delete_room'),
    path('room/modify/<int:id>', EditRoomView.as_view(), name='modify_room'),
    path('room/reserve/<int:id>', ReserveRoom.as_view(), name='reserve_room'),
    path('room/<int:id>', room_details),


]
