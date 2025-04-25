from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.views import View
from main.models import Room, Reservation
from django.utils.timezone import now
from datetime import datetime

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

        return redirect('list_rooms')


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


class ReserveRoom(View):
    def get(self,request, id):
        room = get_object_or_404(Room, id=id)
        today = now().date()
        reservations = room.reservations.filter(date__gte=today).order_by('date')
        return render(request, 'reserve_room.html',{'reservations': reservations})

    def post(self, request, id):
        comment = request.POST['comment']
        date_str = request.POST['date']
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        today = now().date()
        room = get_object_or_404(Room, id=id)
        reservations = room.reservations.filter(date__gte=today).order_by('date')
        if date < today:
            message = 'Date cannot be in the past'
            return render(request, 'reserve_room.html',
                          {'message': message, 'reservations': reservations}, status=400)

        room = get_object_or_404(Room, id=id)
        if room.reservations.filter(date=date).exists():
            message = 'Sorry room is reserved for that date'
            return render(request, 'reserve_room.html',
                          {'message': message, 'reservations': reservations}, status=400)

        Reservation.objects.create(date=date, room=room, comment=comment)

        return redirect('list_rooms')

def room_details(request, id):
    room = get_object_or_404(Room, id=id)
    today = now().date()
    reservations = room.reservations.filter(date__gte=today).order_by('date')
    return render(request, 'room_details.html', {'room': room, 'reservations': reservations})


def search_rooms(request):
    name = request.GET.get('name')
    capacity = request.GET.get('capacity')
    projector = request.GET.get('projector')
    today = now().date()

    rooms = Room.objects.all()

    if name:
        rooms = rooms.filter(name__icontains=name)
    if capacity:
        rooms = rooms.filter(capacity__gte=capacity)
    if projector:
        rooms = rooms.filter(projector=True)

    # Pokaż tylko sale, które nie mają rezerwacji dzisiaj
    reserved_rooms_ids = Room.objects.filter(reservations__date=today).values_list('id', flat=True)
    rooms = rooms.exclude(id__in=reserved_rooms_ids)

    context = {
        'rooms': rooms,
    }
    return render(request, 'search_results.html', context)







