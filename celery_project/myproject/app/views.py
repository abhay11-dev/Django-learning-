from urllib import request

from django.shortcuts import render
from myproject.celery import add
from .tasks import sub
from celery.result import AsyncResult

# Create your views here.
# def home(request):
#     print("Home view called")
#     res1 = add.apply_async(args=[4, 6])
#     res2 = add.apply_async(args=[10, 20])
#     print(f"Task ID for add(4, 6): {res1.id}")
#     print(f"Task ID for add(10, 20): {res2.id}")



#     res3 = sub.apply_async(args=[20, 5])
#     print(f"Task ID for sub(20, 5): {res3.id}")

#     # add.delay(4, 6)  # Example of calling the Celery task asynchronously

#     return render(request, 'home.html')



def home(request):
    result = add.delay(4, 6)  # Call the Celery task asynchronously
    return render(request, 'home.html', {'result': result})

def about(request):
    print("About view called")
    return render(request, 'about.html')

def contact(request):
    print("Contact view called")
    return render(request, 'contact.html')


def check_result(request, task_id):
    result = AsyncResult(task_id)  # Get the AsyncResult object for the given task ID
    return render(request, 'result.html', {'result': result})
 
    
