from rest_framework import permissions, viewsets, status
from rest_framework.response import Response
from .models import *
from .serializers import *
from .filters import *
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend


class TicketDetailViewSet(viewsets.ModelViewSet):
    queryset = TicketDetail.objects.all()
    serializer_class = TicketDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [TicketDetailViewFilter]

    def create(self, request, *args, **kwargs):
        data = request.data
        if isinstance(data, list):
            serializers = [self.get_serializer(data=item) for item in data]
            valid = all(serializer.is_valid() for serializer in serializers)
            if valid:
                ticketdetail = [serializer.save() for serializer in serializers]
                return Response(
                    TicketDetailSerializer(ticketdetail, many=True).data,
                    status=status.HTTP_201_CREATED,
                )
            else:
                errors = [serializer.errors for serializer in serializers]
                return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED, headers=headers
            )

    def update(self, request, *args, **kwargs):
        total = request.data["new_total"]
        return super().update(request, *args, **kwargs)


class MenuProductViewSet(viewsets.ViewSet):
    queryset = []  # Aquí puedes definir un queryset si es necesario
    filter_backends = [MenuProductFilter]
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        queryset = []  # Iniciamos con un queryset vacío ya que no se usará realmente
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(request, queryset, self)

        menu_queryset = [item for item in queryset if isinstance(item, Menu)]
        product_queryset = [item for item in queryset if isinstance(item, Product)]

        menu_serializer = MenuSerializer(menu_queryset, many=True)
        product_serializer = ProductSerializer(product_queryset, many=True)

        return Response(
            {"menus": menu_serializer.data, "products": product_serializer.data}
        )
