from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Note
from .serializers import NoteSerializer

class NoteList(APIView):

    def get(self, request):
        notes = Note.objects.all()
        serializer = NoteSerializer(notes, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = NoteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class NoteDetail(APIView):

    def get(self, request, pk):
        note = Note.objects.get(pk=pk)
        serializer = NoteSerializer(note)
        return Response(serializer.data)

    def delete(self, request, pk):
        note = Note.objects.get(pk=pk)
        note.delete()
        return Response({"message":"deleted"})