from django.views import generic
from .models import Car, Category, Brand
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Car
from .forms import ReviewForm
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Avg

class HomeView(generic.TemplateView):
    template_name = 'home.html'

class CarListView(generic.ListView):
    model = Car
    template_name = 'car_list.html'
    context_object_name = 'cars'

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search', '')
        sort_by = self.request.GET.get('sort', '')

        if search_query:
            queryset = queryset.filter(model__icontains=search_query)

        if sort_by == 'price':
            queryset = queryset.order_by('price')
        elif sort_by == 'rating':
            queryset = queryset.annotate(average_rating=Avg('reviews__rating')).order_by('-average_rating')
        elif sort_by == 'brand':
            queryset = queryset.order_by('brand__name')

        return queryset

class CarDetailView(LoginRequiredMixin, generic.DetailView):
    model = Car
    template_name = 'car_detail.html'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.car = self.object
            review.user = request.user
            review.save()
            return HttpResponseRedirect(self.request.path_info)
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ReviewForm()
        return context

class BrandListView(generic.ListView):
    model = Brand
    template_name = 'brand_list.html'
    context_object_name = 'brands'

class BrandDetailView(generic.DetailView):
    model = Brand
    template_name = 'brand_detail.html'
    context_object_name = 'brand'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cars'] = Car.objects.filter(brand=self.get_object())
        return context

class CategoryListView(generic.ListView):
    model = Category
    template_name = 'category_list.html'
    context_object_name = 'categories'

class CategoryDetailView(generic.DetailView):
    model = Category
    template_name = 'category_detail.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cars'] = Car.objects.filter(category=self.get_object())
        return context
