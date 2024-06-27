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
        total = request.validated_data["editTotal"]
        return super().update(request, *args, **kwargs)


class MenuProductViewSet(viewsets.ViewSet):
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["name", "price", "description"]

    def list(self, request):
        print("entro")
        queryset_menu = Menu.objects.all()
        queryset_product = Product.objects.all()

        name = request.query_params.get("name")
        price = request.query_params.get("price")
        description = request.query_params.get("description")

        if name:
            queryset_menu = queryset_menu.filter(name__icontains=name)
            queryset_product = queryset_product.filter(name__icontains=name)

        if price:
            queryset_menu = queryset_menu.filter(price=price)
            queryset_product = queryset_product.filter(price=price)

        if description:
            queryset_menu = queryset_menu.filter(description__icontains=description)
            queryset_product = queryset_product.filter(
                description__icontains=description
            )

        menu_serializer = MenuSerializer(queryset_menu, many=True)
        product_serializer = ProductSerializer(queryset_product, many=True)

        return Response(
            {"menus": menu_serializer.data, "products": product_serializer.data}
        )
