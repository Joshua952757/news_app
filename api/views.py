from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import ArticleSerializer
from bronewsapp.models import Profile, Article


@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def subscribed_journalist_articles_api(request):
    """
    API endpoint for retrieving articles from journalists that the
    authenticated client (reader) has subscribed to.
    """
    if not (hasattr(request.user, 'profile') and request.user.profile.role == Profile.Role.READER):
        return Response(
            {"detail": "Access denied. Only authenticated readers can retrieve subscribed articles via this API."},
            status=status.HTTP_403_FORBIDDEN
        )

    user_profile = request.user.profile
    subscribed_journalists = user_profile.sub_journalist.all()

    articles = Article.objects.filter(
        author__in=subscribed_journalists,
        is_approved=True
    )

    serializer = ArticleSerializer(articles, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)
