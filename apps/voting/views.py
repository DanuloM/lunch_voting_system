from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Count
from datetime import date
from .models import Vote
from .serializers import VoteSerializer
from apps.menus.models import Menu


class VoteCreateView(generics.CreateAPIView):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [IsAuthenticated]


class VoteResultsView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        today = date.today()
        menus = Menu.objects.filter(date=today).annotate(vote_count=Count('votes'))
        
        results = []
        for menu in menus:
            results.append({
                "menu_id": menu.id,
                "restaurant_name": menu.restaurant.name,
                "date": menu.date,
                "vote_count": menu.vote_count
            })
        
        results.sort(key=lambda x: x["vote_count"], reverse=True)
        
        return Response(results, status=status.HTTP_200_OK)


class MyVoteView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        today = date.today()
        try:
            vote = Vote.objects.get(employee=request.user, date=today)
            serializer = VoteSerializer(vote)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Vote.DoesNotExist:
            return Response({"detail": "You have not voted today"}, status=status.HTTP_404_NOT_FOUND)
