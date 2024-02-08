from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from .models import File, Permission, Folder
from .forms import SignUpForm, FolderForm, UploadFileForm

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def home(request):
    print("Requested userid - ", request.user)
    recent_files = File.objects.filter(owner=request.user).order_by('-created_at')[:5]

    # Получение недавно полученных доступов к файлам для текущего пользователя
    recent_permissions = Permission.objects.filter(permitted_user=request.user).order_by('-id')[:5]

    context = {
        'recent_files': recent_files,
        'recent_permissions': recent_permissions,
    }
    return render(request, 'yayd/home.html', context)


@login_required
def folders_view(request, folder_id=None):
    if folder_id:
        current_folder = get_object_or_404(Folder, id=folder_id, owner=request.user)
    else:
        current_folder = None

    folders = Folder.objects.filter(parent=current_folder, owner=request.user)
    files = File.objects.filter(folder=current_folder, owner=request.user)
    return render(request, 'yayd/folders.html', {
        'folders': folders,
        'files': files,
        'current_folder': current_folder
    })

@login_required
def explorer_view(request):
    folders = Folder.objects.filter(owner=request.user)
    files = File.objects.filter(owner=request.user)
    
    # Здесь могут быть добавлены формы для создания папок и загрузки файлов
    # context = {'folders': folders, 'files': files, 'form_folder': form_folder, 'form_file': form_file}

    context = {'folders': folders, 'files': files}
    return render(request, 'yayd/explorer.html', context)

@login_required
def create_folder(request):
    if request.method == 'POST':
        form = FolderForm(request.POST)
        if form.is_valid():
            new_folder = form.save(commit=False)
            new_folder.owner = request.user
            new_folder.save()
            return redirect('explorer') 
    else:
        form = FolderForm()
    return render(request, 'yayd/create_folder.html', {'form': form})

@login_required
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            new_file = form.save(commit=False)
            new_file.owner = request.user
            new_file.save()
            return redirect('explorer')
    else:
        form = UploadFileForm()
    return render(request, 'yayd/upload_file.html', {'form': form})

@login_required
def view_file(request, file_id):
    file = get_object_or_404(File, id=file_id, owner=request.user)
    
    # choose file type
    if file.file.url.lower().endswith((".jpg", ".jpeg", ".png", ".gif")):
        content, file_type = None, 'image'
    elif file.file.url.lower().endswith(".pdf"):
        content, file_type = None, 'pdf'
    else:
        try:
            with open(file.file.path, 'r') as f:
                content = f.read()
            file_type = 'text'
        except Exception as e:
            content = f"Ошибка при чтении файла: {e}"
            file_type = 'error'

    return render(request, 'yayd/file_view.html', {'file': file, 'content': content, 'file_type': file_type})

@login_required
def edit_file(request, file_id):
    file = get_object_or_404(File, id=file_id, owner=request.user)
    if request.method == "POST":
        content = request.POST.get("content")
        with open(file.file.path, 'w') as f:
            f.write(content)
        return redirect('folders_detail', folder_id=file.folder.id if file.folder else None)
    else:
        try:
            with open(file.file.path, 'r') as f:
                content = f.read()
        except Exception as e:
            content = f"Ошибка при чтении файла: {e}"

    return render(request, 'yayd/edit_file.html', {'file': file, 'content': content})

@login_required
def delete_file(request, file_id):
    file = get_object_or_404(File, id=file_id, owner=request.user)
    if request.method == "POST":
        file.delete()
        return redirect('folders')
    else:
        return HttpResponseForbidden()

@login_required
def delete_folder(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id, owner=request.user)
    if request.method == "POST":
        folder.delete()
        return redirect('folders')
    else:
        return HttpResponseForbidden()