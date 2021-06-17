import logging

from rest_framework import permissions
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.response import Response

logger = logging.getLogger(__name__)


@api_view(["GET", "HEAD"])
@permission_classes([permissions.AllowAny])
@authentication_classes([])
def healthz(request, *args, **kwargs):
    logger.error("error example")
    return Response(status=200)
