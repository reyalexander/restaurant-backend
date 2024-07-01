from datetime import datetime, timedelta
from functools import reduce
from .serializers import *
from django.db.models import Q
from rest_framework import filters


class MenuProductFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        # Parámetros de consulta (query params) del request
        is_publish = request.query_params.get("is_publish", None)
        status = request.query_params.get("status", None)
        searchBy = request.query_params.get("searchBy", None)
        search = request.query_params.get("search", None)
        orderBy = request.query_params.get("orderBy", None)
        order = request.query_params.get("order", None)

        # Filtrado en modelos Menu y Product
        menu_queryset = Menu.objects.all()
        product_queryset = Product.objects.all()

        # Filtro por status
        if status:
            menu_queryset = menu_queryset.filter(status=status)
            product_queryset = product_queryset.filter(status=status)
        if is_publish:
            menu_queryset = menu_queryset.filter(is_publish=is_publish)
            product_queryset = product_queryset.filter(is_publish=is_publish)

        # Filtro por search y searchBy
        if search and searchBy:
            search_by_fields = searchBy.split(
                ","
            )  # Suponiendo que search_by es una cadena separada por comas
            q_objects = Q()

            for field in search_by_fields:
                q_objects |= Q(**{f"{field}__icontains": search})
            menu_queryset = menu_queryset.filter(q_objects)
            product_queryset = product_queryset.filter(q_objects)

        # Filtros adicionales de búsqueda
        search_queries = []
        for i in range(1, len(request.query_params) // 2 + 1):
            search_value = request.query_params.get(f"search{i}")
            search_by = request.query_params.get(f"searchBy{i}")
            if search_value and search_by:
                search_queries.append(Q(**{f"{search_by}__icontains": search_value}))

        if search_queries:
            menu_queryset = menu_queryset.filter(reduce(Q.__and__, search_queries))
            product_queryset = product_queryset.filter(
                reduce(Q.__and__, search_queries)
            )

        # Ordenar resultados
        if orderBy:
            if order == "desc":
                menu_queryset = menu_queryset.order_by("-" + orderBy)
                product_queryset = product_queryset.order_by("-" + orderBy)
            else:
                menu_queryset = menu_queryset.order_by(orderBy)
                product_queryset = product_queryset.order_by(orderBy)
        else:
            menu_queryset = menu_queryset.order_by("id")
            product_queryset = product_queryset.order_by("id")

        # Combinar querysets
        combined_queryset = list(menu_queryset) + list(product_queryset)

        return combined_queryset


class TicketDetailViewFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        # parametros especiales del Modelo
        ticket_id = request.query_params.get("ticket_id", None)
        if ticket_id:
            queryset = queryset.filter(ticket_id=ticket_id)

        product_id = request.query_params.get("product_id", None)
        if product_id:
            queryset = queryset.filter(product_id=product_id)

        is_menu = request.query_params.get("is_menu", None)
        if is_menu:
            queryset = queryset.filter(is_menu=is_menu)

        # Obtiene los parámetros de consulta (query params) del request
        status = request.query_params.get("status", None)
        searchBy = request.query_params.get("searchBy", None)
        search = request.query_params.get("search", None)
        orderBy = request.query_params.get("orderBy", None)
        order = request.query_params.get("order", None)

        # Agregamos filtros por fechas y rangos de fecha
        year_date = request.query_params.get("year_date", None)
        specific_date = request.query_params.get("specific_date", None)
        start_date = request.query_params.get("start_date", None)
        end_date = request.query_params.get("end_date", None)
        interval = request.query_params.get(
            "interval", None
        )  # Puedes usar 'days', 'weeks', 'months', etc.

        search_queries = []
        for i in range(1, len(request.query_params) // 2 + 1):
            search_value = request.query_params.get(f"search{i}")
            search_by = request.query_params.get(f"searchBy{i}")
            if search_value and search_by:
                search_queries.append(Q(**{f"{search_by}__icontains": search_value}))

        if search_queries:
            queryset = queryset.filter(reduce(Q.__and__, search_queries))

        if specific_date:
            queryset = queryset.filter(created_at=specific_date)

        if year_date:
            queryset = queryset.filter(created_at__year=year_date)

        if start_date and end_date:
            # Filtro por rango de fecha
            queryset = queryset.filter(created_at__range=(start_date, end_date))

        elif start_date:
            # Filtro por fecha de inicio
            queryset = queryset.filter(created_at__gte=start_date)

        elif end_date:
            # Filtro por fecha de fin
            queryset = queryset.filter(created_at__lte=end_date)

        elif interval:
            # Filtro por intervalo (días, semanas, meses, etc.)
            if interval == "days":
                delta = timedelta(days=1)
            elif interval == "weeks":
                print("week")
                delta = timedelta(days=7)
            elif interval == "months":
                delta = timedelta(days=30)  # Aproximadamente un mes
            elif interval == "years":
                delta = timedelta(days=365)
            else:
                delta = timedelta(days=1)  # Por defecto, un día

            today = datetime.now().date()
            end_date = today - delta
            queryset = queryset.filter(created_at__range=(end_date, today))

        # Filtra por campos user_name, user_email, user_dni y user_license si se proporciona el parámetro 'search'
        if search and searchBy:
            search_by_fields = searchBy.split(
                ","
            )  # Suponiendo que search_by es una cadena separada por comas
            q_objects = Q()

            for field in search_by_fields:
                q_objects |= Q(**{f"{field}__icontains": search})
            queryset = queryset.filter(q_objects)

        # Filtra por campo 'status' si se proporciona el parámetro 'status'
        if status:
            queryset = queryset.filter(status=status)

        # Ordena por ID de forma predeterminada
        if orderBy:
            if order == "desc":
                queryset = queryset.order_by("-" + orderBy)
            else:
                queryset = queryset.order_by(orderBy)
        else:
            queryset = queryset.order_by("id")

        return queryset
