from django.http import HttpResponse

def home(request):
    student = [ 
        { 
        'name': 'John Doe',
        'age': 20,
        'grade': 'A'
        },
    ]
    return HttpResponse(student)