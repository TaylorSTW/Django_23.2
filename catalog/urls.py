from django.urls import path
from django.views.decorators.cache import cache_page, never_cache

from catalog.apps import CatalogConfig
from catalog.views import IndexView, contacts, BlogListView, BlogCreateView, \
    BlogDetailView, BlogUpdateView, BlogDeleteView, hidden_blog, \
    ProductCreateView, ProductUpdateView, ProductDetailView, CategoryListView

app_name = CatalogConfig.name

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('contacts/', contacts, name='contacts'),
    path('blog/', BlogListView.as_view(), name='blog_list'),
    path('blog/create/', never_cache(BlogCreateView.as_view()), name='blog_create'),
    path('blog/<int:pk>/', BlogDetailView.as_view(), name='blog_view'),
    path('blog/edit/<int:pk>/', BlogUpdateView.as_view(), name='blog_edit'),
    path('blog/delete/<int:pk>/', BlogDeleteView.as_view(), name='blog_delete'),
    path('blog/hidden/', hidden_blog, name="blog_hidden"),
    path('product/create/', never_cache(ProductCreateView.as_view()), name='product_create'),
    path('product/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('product/<int:pk>/view/', cache_page(60)(ProductDetailView.as_view()), name='product_view'),
    path('categories/', CategoryListView.as_view(), name='category_list'),
]