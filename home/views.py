from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from . models import Post, PostImage, Comment, Like
from . forms import PostCreateEditForm, CommentCreateReplyForm
from django.forms import modelformset_factory, BaseModelFormSet
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.text import slugify


class HomeView(View):
    def get(self, request):
        posts = Post.objects.all()
        return render(request,'home/home.html', {'posts':posts})


class PostDetailView(View):
    form_class_comment = CommentCreateReplyForm
    def get(self, request, post_id, post_slug):
        post = Post.objects.get(id=post_id, slug=post_slug)
        if self.request.user.is_authenticated:
            user_has_liked = Like.objects.filter(user=self.request.user, post=post).exists()
        else:
            user_has_liked = False

        comments = post.comment_set.all()
        comment_form = self.form_class_comment()
        return render(request, 'home/post_detail.html', {'post':post, 'comments':comments, 'comment_form':comment_form, 'user_has_liked':user_has_liked})
    
    def post(self, request, post_id, post_slug):
        comment_form = self.form_class_comment(request.POST)
        post = Post.objects.get(id=post_id, slug=post_slug)
        if comment_form.is_valid():
            new_comment_form = comment_form.save(commit=False)
            new_comment_form.post = post
            new_comment_form.user = request.user

            parent_comment = comment_form.cleaned_data['reply']
            if parent_comment:
                new_comment_form.is_reply = True

            new_comment_form.save()
            messages.success(request, 'comment add successfully', 'success')
            return redirect('home:post_detail', post_id=post.id, post_slug=post.slug)
        
        comments = post.comment_set.all()
        return render(request, 'post_detail.html', {
            'post': post,
            'comments': comments,
            'comment_form': comment_form
        })

class PostEditView(LoginRequiredMixin, View):
    form_class = PostCreateEditForm
    def get(self, request, post_id):
        post = Post.objects.get(id=post_id)
        post_form = self.form_class(instance=post)

        ImageFormSet = modelformset_factory(PostImage, fields=('image',), extra=2, can_delete=True)
        formset = ImageFormSet(queryset=post.images.all())


        return render(request, 'home/post_edit.html', {'form':post_form, 'formset': formset, 'post': post})
    
    def post(self, request, post_id):
        post = Post.objects.get(id=post_id)
        post_form = self.form_class(request.POST, instance=post)

        ImageFormSet = modelformset_factory(PostImage, fields=('image',), extra=2, can_delete=True)
        formset = ImageFormSet(request.POST, request.FILES, queryset=post.images.all())
        print(request.POST)
        print(request.FILES)


        

        if post_form.is_valid() and formset.is_valid():
            new_post = post_form.save(commit=False)
            new_post.user = request.user
            body = post_form.cleaned_data['body']
            new_post.slug = slugify(body[:10])

            new_post.save()

            # Handle images in the formset
            print(formset.cleaned_data)
            for form in formset:
                if form.cleaned_data:
                    print(form.cleaned_data)
                    print('pk', form.instance.id)
                    if form.cleaned_data.get('DELETE') and form.instance.pk:
                        print('delete')
                        form.instance.delete()
                    elif not form.cleaned_data.get('DELETE'):
                        print('not delete')
                        image = form.save(commit=False)
                        image.post = new_post
                        image.save()

            messages.success(request,'updated successfully!','success')
            return redirect('home:post_detail', post.id, post.slug)
        
        else:
            # Print errors to the console or log them for debugging
            print("Post form errors:", post_form.errors)
            print("Formset errors:", formset.errors)


        return render(request, 'home/post_edit.html', {'form': post_form, 'formset': formset, 'post': post})

class PostDeleteView(LoginRequiredMixin, View):
    def post(self, request, post_id):
        post = Post.objects.get(id=post_id)
        post.delete()
        messages.success(request, 'post deleted successfully!', 'success')
        return redirect('home:home')
    
    def get(self, request, post_id):
        post = Post.objects.get(id=post_id)
        return render(request, 'home/post_confirm_delete.html', {'post': post})
            

class PostCreateView(LoginRequiredMixin, View):
    form_class = PostCreateEditForm
    def get(self, request):
        form = self.form_class()
        ImageFormSet = modelformset_factory(PostImage, fields=('image',), extra=3)  
        formset = ImageFormSet(queryset=PostImage.objects.none())  
        return render(request, 'home/post_create.html',{'form':form, 'formset': formset})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        ImageFormSet = modelformset_factory(PostImage, fields=('image',), extra=3)
        formset = ImageFormSet(request.POST, request.FILES, queryset=PostImage.objects.none())
        if form.is_valid() and formset.is_valid():
            new_form = form.save(commit=False)
            new_form.user = request.user
            new_form.body = form.cleaned_data['body']
            new_form.slug = slugify(form.cleaned_data['body'][:10])
            new_form.save()
            # Save images from formset
            for form in formset:
                if form.cleaned_data:
                    image = form.save(commit=False)
                    image.post = new_form
                    image.save()


            messages.success(request, 'post created succssfully!', 'success')
            return redirect('home:post_detail', new_form.id, new_form.slug)
        return render(request, 'home/post_create.html', {'form':form, 'formset': formset})
    

class LikePostView(LoginRequiredMixin, View):
    def post(self, request, post_id, *args, **kwargs):
        post = get_object_or_404(Post, id=post_id)
        like, created = Like.objects.get_or_create(user=request.user, post=post)

        if not created:
            
            like.delete()

        return redirect('home:post_detail', post_id=post.id, post_slug=post.slug)