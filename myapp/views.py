from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required,permission_required,user_passes_test
from .forms import RegisterForm,PostForm,LabelForm,ImageUploadForm
from django.contrib.auth.models import User, Group
from .models import Post,Label
# Create your views here.
from django.http import HttpResponse

@login_required(login_url="/login")
def home(request):
    posts = Post.objects.all()
    print("ROUND1")
    if request.method == "POST":
        print("ROUND2")
        
        post_id = request.POST.get("post-id")
        user_id = request.POST.get("user-id")

        if post_id:
            post = Post.objects.filter(id=post_id).first()
            if post and (post.author == request.user or request.user.has_perm("myapp.delete_post")):
                post.delete()
        elif user_id:
            user = User.objects.filter(id=user_id).first()
            if user and request.user.is_staff:
                try:
                    group = Group.objects.get(name='consumer')
                    group.user_set.remove(user)
                except:
                    pass

                try:
                    group = Group.objects.get(name='mod')
                    group.user_set.remove(user)
                except:
                    pass
    if request.user.is_superuser:
        print("Print HEREASDFADSFDSAFS")
        return redirect('admin_dashboard')

    return render(request, 'myapp/home.html', {"posts": posts})

@user_passes_test(lambda u: u.is_superuser)
def admin_dashboard(request):
    labels = Label.objects.all()
    posts = Post.objects.all()

    if request.method == "POST":
        # Handling label creation
        label_form = LabelForm(request.POST)
        if label_form.is_valid():
            label_form.save()

        # Handling label deletion
        labels_to_delete = request.POST.getlist('labels_to_delete')
        if labels_to_delete:
            Label.objects.filter(id__in=labels_to_delete).delete()

        # Handling image upload
        image_form = ImageUploadForm(request.POST, request.FILES)
        if image_form.is_valid():
            image_form.save()

    else:
        label_form = LabelForm()
        image_form = ImageUploadForm()

    return render(request, 'myapp/admin_dashboard.html', {"labels": labels, "posts": posts, "label_form": label_form, "image_form": image_form})




@login_required(login_url="/login")
@permission_required("myapp.add_post", login_url="/login", raise_exception=True)
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST,request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("/")
    else:
        form = PostForm()

    return render(request, 'myapp/create_post.html', {"form": form})


def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = RegisterForm()

    return render(request, 'registration/sign_up.html', {"form": form})