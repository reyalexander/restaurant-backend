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
            ticket_id = request.data["ticket_id"]
            total = request.data["new_total"]
            final = request.data["new_final"]
            ticket = Ticket.objects.get(id=ticket_id)
            ticket.priceTotal = total
            ticket.priceFinal = final
            ticket.save()
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED, headers=headers
            )

    def update(self, request, *args, **kwargs):
        ticket_id = request.data["ticket_id"]
        total = request.data["new_total"]
        final = request.data["new_final"]
        ticket = Ticket.objects.get(id=ticket_id)
        ticket.priceTotal = total
        ticket.priceFinal = final
        ticket.save()
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        ticket_id = instance.ticket_id.id

        new_total = request.data["new_total"]
        new_final = request.data["new_final"]
        print(new_total)
        print(instance.price_total)
        print("entre a eliminar el price")
        if new_total is not None:
            print("entre a editar el price")
            ticket = Ticket.objects.get(id=ticket_id)
            ticket.priceTotal = new_total
            ticket.priceFinal = new_final
            ticket.save()

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


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


from django.db.models import Count, Q


class StatisticsViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        # Calcula la fecha hace 6 días desde hoy
        six_days_ago = datetime.now() - timedelta(days=6)

        # Filtra TicketDetails por ticket_id__created_at desde hace 6 días hasta hoy
        queryset = TicketDetail.objects.filter(ticket_id__created_at__gte=six_days_ago)

        # Generar un rango de fechas desde hace 6 días hasta hoy
        date_range = [six_days_ago + timedelta(days=i) for i in range(7)]

        # Inicializar diccionarios para almacenar las estadísticas
        product_type_stats = {"MENU": 0}
        daily_total_price = {}

        # Calcular estadísticas por tipo de producto y por día
        for day in date_range:
            day_str = day.strftime("%Y-%m-%d")

            # Estadísticas de precio total diario
            total_price = 0
            unique_ticket_ids = set()

            for ticket_detail in queryset.filter(
                ticket_id__created_at__date=day.date()
            ):
                if ticket_detail.ticket_id.id not in unique_ticket_ids:
                    unique_ticket_ids.add(ticket_detail.ticket_id.id)
                    total_price += ticket_detail.ticket_id.priceFinal

            daily_total_price[day_str] = total_price

            # Estadísticas por tipo de producto
            for ticket_detail in queryset.filter(
                ticket_id__created_at__date=day.date()
            ):
                if ticket_detail.is_menu:
                    product_type_stats["MENU"] += ticket_detail.quantity
                else:
                    try:
                        product = Product.objects.get(id=ticket_detail.product_id)
                        product_type = product.id_typeproduct.name
                        if product_type not in product_type_stats:
                            product_type_stats[product_type] = 0
                        product_type_stats[product_type] += ticket_detail.quantity
                    except Product.DoesNotExist:
                        continue

        # Preparar la respuesta en el formato solicitado
        response_data = {
            "combined_stats": [],
            "daily_total_price": daily_total_price,
            "product_type_stats": product_type_stats,
        }

        # Formato para combined_stats
        for product_type, quantity in product_type_stats.items():
            data_points = []
            for day in date_range:
                day_str = day.strftime("%Y-%m-%d")
                data_points.append({"x": day_str, "y": 0})
            response_data["combined_stats"].append(
                {"name": product_type, "data": data_points}
            )

        # Llenar datos reales en combined_stats
        for day_index, day in enumerate(date_range):
            for ticket_detail in queryset.filter(
                ticket_id__created_at__date=day.date()
            ):
                if ticket_detail.is_menu:
                    response_data["combined_stats"][0]["data"][day_index][
                        "y"
                    ] += ticket_detail.quantity
                else:
                    try:
                        product = Product.objects.get(id=ticket_detail.product_id)
                        product_type = product.id_typeproduct.name
                        for stat in response_data["combined_stats"]:
                            if stat["name"] == product_type:
                                stat["data"][day_index]["y"] += ticket_detail.quantity
                                break
                    except Product.DoesNotExist:
                        continue

        return Response(response_data)
