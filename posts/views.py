from django.shortcuts import render , redirect
from .models import Post,Like
from profiles.models import Profile
from .forms import PostForm, CommentForm
from django.views.generic import DeleteView , UpdateView
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

@login_required
def post_comment_create_and_list_view(request):
    qs = Post.objects.all()
    profile = Profile.objects.get(user=request.user)

    # initials
    p_form = PostForm()
    c_form = CommentForm()
    post_added = False

    profile = Profile.objects.get(user=request.user)

    if 'submit_p_form' in request.POST:
        print(request.POST)
        p_form = PostForm(request.POST, request.FILES)
        if p_form.is_valid():
            instance = p_form.save(commit=False)
            instance.author = profile
            instance.save()
            p_form = PostForm()
            post_added = True

    if 'submit_c_form' in request.POST:
        c_form = CommentForm(request.POST)
        if c_form.is_valid():
            instance = c_form.save(commit=False)
            instance.user = profile
            instance.post = Post.objects.get(id=request.POST.get('post_id'))
            instance.save()
            c_form = CommentForm()


    context = {
        'qs': qs,
        'profile': profile,
        'p_form': p_form,
        'c_form': c_form,
        'post_added': post_added,
    }

    return render(request, 'posts/main.html', context)
@login_required
def like_unlike_post(request):
	user = request.user
	if request.method == 'POST':
		post_id = request.POST.get('post_id')
		post_obj = Post.objects.get(id=post_id)
		profile = Profile.objects.get(user=user)

		if profile in post_obj.liked.all():
			post_obj.liked.remove(profile)
		else:
			post_obj.liked.add(profile)

		like, created = Like.objects.get_or_create(user=profile, post_id=post_id)

		if not created:
			if like.value == 'Like':
				like.value = 'Unlike'
			else:
				like.value = 'Like'
		else:
			like.value = 'Like'

			post_obj.save()
			like.save()	
		data = {
		'value': like.value,
		'like': post_obj.liked.all().count()
		}
		return JsonResponse(data, safe=False )
	return redirect ('posts:main-post-view')


#Delete class 
class PostDeleteView(LoginRequiredMixin,DeleteView):
	model = Post
	template_name = 'posts/confirm_del.html'
	success_url = reverse_lazy('posts:main-post-view')

	def get_objects(self, *args, **kwargs):
		pk = self.kwargs.get('pk')
		obj = Post.objects.get(pk=pk)
		if not obj.author.user == self.request.user:
			message.warning(self.request, "You need to be the author of the post in order to delete it")
		return obj


	def form_valid(self, form):
		profile = Profile.objects.get(user=self.request.user)
		if form.instance.author == profile:
			return super().form_valid(form)
		else:
			form.add_error(None,"You need to be the author of the post in order to update it" )
			return super().form_invalid(form)
			
#Update(edit) class 
class PostUpdateView(LoginRequiredMixin,UpdateView):
	form_class = PostForm
	model = Post
	template_name = 'posts/update.html'
	success_url = reverse_lazy("posts:main-post-view")


	def form_valid(self, form):
		profile = Profile.objects.get(user=self.request.user)
		if form.instance.author == profile:
			return super().form_valid(form)
		else:
			form.add_error(None, "You need to be the author of the post in order to update it")
			return super().form_invalid(form)

