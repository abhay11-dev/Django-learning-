from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Room, Message


@login_required
def lobby(request):
    rooms = Room.objects.all()
    return render(request, "chat/lobby.html", {"rooms": rooms})


@login_required
def create_room(request):
    if request.method == "POST":
        room_name = request.POST.get("room_name")

        if not Room.objects.filter(name=room_name).exists():
            Room.objects.create(name=room_name)

    return redirect("chat:lobby")


@login_required
def room(request, room_name):
    room = get_object_or_404(Room, name=room_name)
    messages = Message.objects.filter(room=room)

    return render(request, "chat/room.html", {
        "room": room,
        "messages": messages
    })