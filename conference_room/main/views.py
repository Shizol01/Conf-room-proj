from django.shortcuts import render, HttpResponse, redirect
from django.views import View
from main.models import Room

# Create your views here.
class HomePageView(View):
    def get(self,request):
        return render(
            request,
            'base.html'
        )


class RoomAddView(View):
    def get(self, request):
        return render(
            request,
            'add_room.html'
        )
    def post(self, request):
        name = request.POST['name']
        capacity = int(request.POST['capacity'])
        projector = request.POST.get('projector') == 'on'

        if Room.objects.filter(name=name).exists():
            message = f'Room {name} already exists'
            return render(request, 'add_room.html', {'message': message, 'name': name, 'capacity': capacity, 'projector': projector}, status=400)

        if capacity <= 0:
            message = 'Capacity cannot be lower or equal 0'
            return render(request, 'add_room.html', {'message': message, 'name': name, 'capacity': capacity, 'projector': projector}, status=400)

        Room.objects.create(name=name, capacity=capacity, projector=projector)

        return redirect('home')