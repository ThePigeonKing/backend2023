from blog.models import Post, Comment
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views import generic

class IndexView(generic.ListView):
    model = Post
    paginate_by = 5
    queryset = Post.objects.prefetch_related('author')


class DetailView(generic.DetailView):
    model = Post
    # прикрепляем comment к посту
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all().order_by('created_at')
        
        return context


class CreateView(LoginRequiredMixin, generic.CreateView):
    model = Post
    fields = ["title", "text"]
    template_name = "blog/post_new.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class UpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Post
    fields = ['title', 'text']
    template_name = "blog/post_edit.html"

class DeleteView(LoginRequiredMixin, generic.DeleteView):
    # post_confirm_delete.html
    model = Post
    success_url = reverse_lazy("blog:index") 


# <---- COMMENTS ----->
class CommentCreateView(LoginRequiredMixin, generic.CreateView):
    model = Comment
    template_name = "blog/comment_create.html"
    fields = ['text', 'is_anonymous']
    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)
    def get_success_url(self):
        return reverse('blog:detail', kwargs={'pk': self.kwargs['pk']})
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']
        return context
    
class CommentMoreView(LoginRequiredMixin, generic.UpdateView):
    model = Comment
    fields = ['text', 'is_anonymous']
    template_name = "blog/comment_more.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment'] = self.object
        context['post'] = self.object.post
        return context
    
class CommentUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Comment
    fields = ['text', 'is_anonymous']
    template_name = "blog/comment_edit.html"
    def get_success_url(self):
        return reverse('blog:comment_more', kwargs={'pk': self.object.pk})
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = self.object.post
        return context
    
class CommentDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Comment
    def get_success_url(self):
        return reverse('blog:detail', kwargs={'pk': self.object.post.pk})   