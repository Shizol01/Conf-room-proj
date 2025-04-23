from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.views import View
from main.models import Room
from django.utils.timezone import now

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


class RoomsDisplayView(View):
    def get(self,request):
        rooms = Room.objects.all()
        today = now().date()
        room_data = []

        for room in rooms:
            is_reserved_today = room.reservations.filter(date=today).exists()
            room_data.append({
                'room': room,
                'is_reserved_today': is_reserved_today,
            })
        return render(request, 'room_list.html', {'room_data': room_data})

def delete_room_view(request, id):
    room = get_object_or_404(Room, id=id)
    if room:
        room.delete()
    return redirect('list_rooms')

class EditRoomView(View):
    def get(self, request, id):
        room = get_object_or_404(Room, id=id)
        return render(request, 'edit_room.html', {'room': room})

    def post(self, request, id):
        room = get_object_or_404(Room, id=id)
        name = request.POST['name']
        capacity = int(request.POST['capacity'])
        projector = request.POST.get('projector') == 'on'

        if Room.objects.exclude(id=room.id).filter(name=name).exists():
            message = f'Room {name} already exists'
            return render(request, 'edit_room.html',
                          {'message': message, 'room': room}, status=400)

        if capacity <= 0:
            message = 'Capacity cannot be lower or equal 0'
            return render(request, 'edit_room.html',
                          {'message': message, 'room': room}, status=400)

        room.name = name
        room.capacity = capacity
        room.projector = projector
        room.save()

        return redirect('list_rooms')








