# views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from api.models.category_model import Category
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from api.serializers.serializers import CategorySerializer
from django.core.exceptions import ObjectDoesNotExist

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    ##permission_classes = [IsAuthenticated]

    def list_categories(self, request):
        page = request.GET.get('page', 1)
        per_page = request.GET.get('per_page', 10)
        categories = Category.objects.all().order_by('id')
        paginator = Paginator(categories, per_page)
        try:
            categories_page = paginator.page(page)
        except PageNotAnInteger:
            categories_page = paginator.page(1)
        except EmptyPage:
            categories_page = paginator.page(paginator.num_pages)
        serializer = CategorySerializer(categories_page, many=True)
        return Response({
            "categories": serializer.data,
            "page": categories_page.number,
            "pages": paginator.num_pages,
            "has_next": categories_page.has_next(),
            "has_previous": categories_page.has_previous(),
        })

    def get_category_by_id(self, request, pk=None):
        try:
            category = Category.objects.get(id=pk)
            serializer = CategorySerializer(category)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            return Response({"error": "Category not found."}, status=status.HTTP_404_NOT_FOUND)

    def create_category(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update_category(self, request, pk=None):
        try:
            category = Category.objects.get(id=pk)
            serializer = CategorySerializer(category, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response({"error": "Category not found."}, status=status.HTTP_404_NOT_FOUND)

    def delete_category(self, request, pk=None):
        try:
            category = Category.objects.get(id=pk)
            category.delete()
            return Response({"message": "Category deleted."}, status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            return Response({"error": "Category not found."}, status=status.HTTP_404_NOT_FOUND)