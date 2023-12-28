from django.views import generic
from .models import Car, Category, Brand
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Car
from .forms import ReviewForm

class HomeView(generic.TemplateView):
    template_name = 'home.html'

class CarListView(generic.ListView):
    model = Car
    template_name = 'car_list.html'
    context_object_name = 'cars'

class CarDetailView(generic.DetailView):
    model = Car
    template_name = 'car_detail.html'
    context_object_name = 'car'

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

@login_required
def car_detail(request, car_id):
    car = get_object_or_404(Car, pk=car_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.car = car
            review.user = request.user
            review.save()
            return redirect('car_detail', car_id=car_id)
    else:
        form = ReviewForm()
    return render(request, 'car_detail.html', {'car': car, 'form': form})