from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import get_object_or_404, render, redirect
from api.models.product_model import Product
from api.serializers.serializers import ProductSerializer
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from api.models.category_model import Category

@login_required
def products(request):
    list_products_view = Product.objects.all()
    return render(request, 'main/products/all.html', {
        'products': list_products_view
    })

@swagger_auto_schema(method='get', responses={200: ProductSerializer(many=True)})
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def list_products_view(request):
    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('page_size', 10))
    products = Product.objects.all().order_by('id')
    paginator = Paginator(products, page_size)
    try:
        products_page = paginator.page(page)
    except PageNotAnInteger:
        products_page = paginator.page(1)
    except EmptyPage:
        products_page = paginator.page(paginator.num_pages)
    serializer = ProductSerializer(products_page, many=True)
    return Response({
        "products": serializer.data,
        "page": products_page.number,
        "pages": paginator.num_pages,
        "has_next": products_page.has_next(),
        "has_previous": products_page.has_previous(),
    })

@swagger_auto_schema(method='get', responses={200: ProductSerializer()})
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_product_view(pk=None):
    product = get_object_or_404(Product, pk=pk)
    serializer = ProductSerializer(product)
    return Response(serializer.data)

@swagger_auto_schema(method='post', request_body=ProductSerializer, responses={201: ProductSerializer()})
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_product_view(request):
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(method='put', request_body=ProductSerializer, responses={200: ProductSerializer()})
@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def update_product_view(request, pk=None):
    product = get_object_or_404(Product, pk=pk)
    data = request.data.copy()
    data.update(request.FILES)
    serializer = ProductSerializer(product, data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(method='delete', responses={204: 'No Content'})
@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def delete_product_view(pk=None):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@login_required
def create_product(request):
    if request.method == 'POST':
        data = request.POST.copy()
        data.update(request.FILES)
        serializer = ProductSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            messages.success(request, 'Produto criado com sucesso!')
            return redirect('products')
        else:
            messages.error(request, 'Erro ao criar o produto. Verifique os dados e tente novamente.')
            return render(request, 'main/products/add.html', {
                'isLoggedIn': request.user.is_authenticated,
                'errors': serializer.errors,
                'categories': Category.objects.all()
            })
    return render(request, 'main/products/add.html', {
        'isLoggedIn': request.user.is_authenticated,
        'categories': Category.objects.all()
    })
    
@login_required
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        data = request.POST.copy()
        data.update(request.FILES)
        if 'photo' not in request.FILES:
            data['photo'] = product.photo
        serializer = ProductSerializer(product, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            messages.success(request, 'Produto atualizado com sucesso!')
            return redirect('products')
        else:
            messages.error(request, 'Erro ao atualizar o produto. Verifique os dados e tente novamente.')
            return render(request, 'main/products/edit.html', {
                'product': product,
                'isLoggedIn': request.user.is_authenticated,
                'errors': serializer.errors,
                'categories': Category.objects.all()
            })
    return render(request, 'main/products/edit.html', {
        'product': product,
        'isLoggedIn': request.user.is_authenticated,
        'categories': Category.objects.all()
    })

@login_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Produto excluído com sucesso!')
        return redirect('products')
    return render(request, 'main/products/confirm_delete.html', {'product': product})

@login_required
def list_products_by_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category)
    return render(request, 'main/products/by_category.html', {
        'category': category,
        'products': products,
        'isLoggedIn': request.user.is_authenticated
    })