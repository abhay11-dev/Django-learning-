from urllib import request

from django.http import HttpResponse
from django.http import JsonResponse
from blogs.models import Blog, Comment
from employees.models import Employee
from students.models import Student
from .serializers import EmployeeSerializer, StudentSerializer
from blogs.serializers import BlogSerializer, CommentSerializer
from rest_framework.response import Response
from rest_framework import status
from employees.models import Employee
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import mixins, generics
from rest_framework import viewsets
from blogs.serializers import CommentSerializer, BlogSerializer


@api_view(['GET','POST'])
def studentsView(request):
    if request.method == 'GET':
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET','PUT','DELETE'])
def studentDetailView(request, id):
    try:
        student = Student.objects.get(id=id)
    except Student.DoesNotExist:
        return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = StudentSerializer(student)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'PUT':
        serializer = StudentSerializer(student, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    













# class EmployeesView(APIView):
#     def get(self, request):
#         employees = Employee.objects.all()
#         serializer = EmployeeSerializer(employees, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def post(self, request):
#         serializer = EmployeeSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    
# class EmployeeDetailView(APIView):
#     def get(self, request, id):
#         try:
#             employee = Employee.objects.get(id=id)
#         except Employee.DoesNotExist:
#             return Response({'error': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)

#         serializer = EmployeeSerializer(employee)
#         return Response(serializer.data, status=status.HTTP_200_OK)
        
#     def put(self, request, id):
#         try:
#             employee = Employee.objects.get(id=id)
#         except Employee.DoesNotExist:
#             return Response({'error': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)

#         serializer = EmployeeSerializer(employee, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, id):
#         try:
#             employee = Employee.objects.get(id=id)
#         except Employee.DoesNotExist:
#             return Response({'error': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)

#         employee.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)











#MIXINS AND GENERIC VIEWS
''' 
class EmployeesView(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)
    
class EmployeeDetailView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def get(self, request,pk):
        return self.retrieve(request, pk)

    def put(self, request, pk):
        return self.update(request, pk)

    def delete(self, request, pk):
        return self.destroy(request, pk)
    
'''


# class EmployeesView(generics.ListCreateAPIView):
#     queryset = Employee.objects.all()
#     serializer_class = EmployeeSerializer

# class EmployeeDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Employee.objects.all()
#     serializer_class = EmployeeSerializer


# class EmployeeViewSet(viewsets.ViewSet):
#     def list(self, request):
#         employees = Employee.objects.all()
#         serializer = EmployeeSerializer(employees, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
    
#     def create(self, request):
#         serializer = EmployeeSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
#     def retrieve(self, request, pk=None):
#         try:
#             employee = Employee.objects.get(id=pk)
#         except Employee.DoesNotExist:
#             return Response({'error': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)

#         serializer = EmployeeSerializer(employee)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def update(self, request, pk=None):
#         try:
#             employee = Employee.objects.get(id=pk)
#         except Employee.DoesNotExist:
#             return Response({'error': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)

#         serializer = EmployeeSerializer(employee, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     def destroy(self, request, pk=None):
#         try:
#             employee = Employee.objects.get(id=pk)
#         except Employee.DoesNotExist:
#             return Response({'error': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)

#         employee.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
    



class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    filterset_fields = ['name']





class BlogView(generics.ListCreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

class CommentView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class BlogDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


