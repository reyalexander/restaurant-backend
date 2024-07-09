from .models import Product
from .serializers import ProductSerializer
from rest_framework import viewsets, permissions,status, serializers
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from django.db.models import Q
from rest_framework.views import APIView
from django.http import HttpResponse
from django.template.loader import render_to_string
from datetime import datetime
from xhtml2pdf import pisa


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name','description','id_typeproduct']


class ReportsProductAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        return self.render_to_pdf(request)

    def render_to_pdf(self, request):
        #report = Product.objects.filter(company_id__in=request.user.get_companies, deleted=False)  # filter(company_id=request.user.company_id, deleted=False)
        template_path = 'products_report.html'

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="Report.pdf"'
        #serializedProducts = ProductSerializer(report, many=True).data

        data = {
            'filename': "REPORTE-PRODUCTOS",
            'products': "serializedProducts",
            'reportDate': serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S").to_representation(datetime.now()),
            'total': "2033203"
        }
        html = render_to_string(template_path, data)

        pisaStatus = pisa.CreatePDF(html, dest=response)

        return response

