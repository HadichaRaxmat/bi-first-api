from django.urls import path
from .views import JuryViewSet

urlpatterns = [
    # --- Login ---
    path('login/juri/', JuryViewSet.as_view({"post": "login"}), name="login"),

    # --- Profile ---
    path('profile/', JuryViewSet.as_view({"get": "profile", "patch": "profile"}), name="profile"),

    # --- Competitions list ---
    path('competitions/', JuryViewSet.as_view({"get": "competitions"}), name="competitions"),

    # --- Competition detail ---
    path('competitions/<int:pk>/competition/', JuryViewSet.as_view({"get": "competition_detail"}), name="competition-detail"),

    # --- Competition participants ---
    path('competitions/<int:pk>/participants/', JuryViewSet.as_view({"get": "competition_participants"}), name="competition-participants"),

    # --- Participant detail with grade POST ---
    path(
        'competitions/<int:competition_pk>/participant/<int:pk>/participant/',
        JuryViewSet.as_view({"get": "participant_detail", "post": "participant_detail"}),
        name="participant-detail"
    ),

    # --- Security (change password) ---
    path('security/', JuryViewSet.as_view({"post": "security"}), name="security"),

    # --- Logout ---
    path('logout/', JuryViewSet.as_view({"post": "logout"}), name="logout"),

    # --- Danger Zone (delete account) ---
    path('danger-zone/', JuryViewSet.as_view({"delete": "danger_zone"}), name="danger-zone"),
]
