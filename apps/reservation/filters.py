from datetime import datetime, timedelta
from functools import reduce

from django.db.models import Q
from rest_framework import filters


class ReservationViewFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        # parametros especiales del Modelo
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
            queryset = queryset.filter(date=specific_date)

        if year_date:
            queryset = queryset.filter(date__year=year_date)

        if start_date and end_date:
            # Filtro por rango de fecha
            queryset = queryset.filter(date__range=(start_date, end_date))

        elif start_date:
            # Filtro por fecha de inicio
            queryset = queryset.filter(date__gte=start_date)

        elif end_date:
            # Filtro por fecha de fin
            queryset = queryset.filter(date__lte=end_date)

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
            queryset = queryset.filter(date__range=(end_date, today))

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
