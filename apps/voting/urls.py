from django.urls import path
from .views import VoteCreateView, VoteResultsView, MyVoteView

urlpatterns = [
    path("", VoteCreateView.as_view(), name="vote-create"),
    path("results/", VoteResultsView.as_view(), name="vote-results"),
    path("my-vote/", MyVoteView.as_view(), name="my-vote"),
]

