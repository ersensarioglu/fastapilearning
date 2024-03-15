from django.shortcuts import render

rooms = [
    {'id': 1, 'name': 'Lets learn python'},
    {'id': 2, 'name': 'Design with me'},
    {'id': 3, 'name': 'Front end developers'},
]

def home(request):
    context = {'rooms': rooms}
    return render(request, 'base/home.html', context)
def room(request):
    return render(request, 'room.html')
