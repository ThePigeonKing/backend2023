from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseForbidden, Http404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import File, Permission, Folder
from .forms import SignUpForm, FolderForm, UploadFileForm, ShareForm
import os

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
    user = request.user
    
    if folder_id:
        current_folder = get_object_or_404(Folder, Q(id=folder_id) & (Q(owner=user) | Q(permissions__permitted_user=user)))
    else:
        current_folder = None

    folders = Folder.objects.filter(Q(parent=current_folder), Q(owner=user) | Q(permissions__permitted_user=user)).distinct()

    files = File.objects.filter(Q(folder=current_folder), Q(owner=user) | Q(permissions__permitted_user=user)).distinct()

    editable_extensions = ['.txt', '.md', '.py', '.c', '.go']
    for file in files:
        _, ext = os.path.splitext(file.file.name)
        file.is_editable = ext in editable_extensions


    return render(request, 'yayd/folders.html', {
        'current_folder': current_folder,
        'folders': folders,
        'files': files,
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
def create_folder(request, folder_id=None):
    parent_folder = None
    if folder_id:
        parent_folder = get_object_or_404(Folder, id=folder_id, owner=request.user)

    if request.method == 'POST':
        form = FolderForm(request.POST, user=request.user)
        if form.is_valid():
            new_folder = form.save(commit=False)
            new_folder.parent = parent_folder
            new_folder.owner = request.user
            new_folder.save()
            return redirect('folders_detail', folder_id=new_folder.id) if parent_folder else redirect('folders')
    else:
        form = FolderForm(user=request.user)

    return render(request, 'yayd/create_folder.html', {'form': form, 'parent_folder': parent_folder})


@login_required
def upload_file(request, folder_id=None):
    folder = None
    if folder_id and folder_id != 'root':
        folder = get_object_or_404(Folder, id=folder_id, owner=request.user)

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            new_file = form.save(commit=False)
            new_file.folder = folder
            new_file.owner = request.user
            new_file.save()
            return redirect('folders')
    else:
        form = UploadFileForm(user=request.user)

    return render(request, 'yayd/upload_file.html', {'form': form, 'folder': folder})


@login_required
def view_file(request, file_id):
    try:
        file = File.objects.get(id=file_id)
    except File.DoesNotExist:
        raise Http404("Файл не найден.")

    if file.owner != request.user:
        has_permission = Permission.objects.filter(file=file, permitted_user=request.user).exists()
        if not has_permission:
            messages.error(request, "У вас нет доступа к этому файлу.")
            return redirect('folders') 

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
    # Получаем файл, убедившись, что он существует
    file = get_object_or_404(File, id=file_id)

    # Проверяем, имеет ли пользователь право на редактирование файла
    has_edit_permission = file.owner == request.user or \
                          Permission.objects.filter(file=file, permitted_user=request.user, permission_type=Permission.EDIT).exists()

    # Проверяем, поддерживается ли расширение файла для редактирования
    _, ext = os.path.splitext(file.file.name)
    editable_extensions = ['.txt', '.md', '.py', '.c', '.go']
    is_editable_extension = ext.lower() in editable_extensions

    if not has_edit_permission or not is_editable_extension:
        messages.error(request, "У вас нет прав для редактирования этого файла или его формат не поддерживается.")
        return redirect('folders')

    if request.method == "POST":
        # Обработка формы редактирования
        content = request.POST.get("content")
        try:
            with open(file.file.path, 'w') as f:
                f.write(content)
            messages.success(request, "Файл успешно обновлён.")
        except IOError as e:
            messages.error(request, f"Ошибка при сохранении файла: {e}")
        return redirect('folders') if file.folder else redirect('folders')

    else:
        try:
            with open(file.file.path, 'r') as f:
                content = f.read()
        except IOError as e:
            content = f"Ошибка при чтении файла: {e}"
            messages.error(request, content)
            return redirect('folders') if file.folder else redirect('folders')

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
    
@login_required
def share_access(request, object_id, type):
    # Определение объекта, к которому предоставляется доступ
    if type == 'folder':
        obj = get_object_or_404(Folder, id=object_id, owner=request.user)
        # Получаем все файлы внутри папки
        files_in_folder = File.objects.filter(folder=obj)
    elif type == 'file':
        obj = get_object_or_404(File, id=object_id, owner=request.user)
        files_in_folder = []
    else:
        messages.error(request, "Некорректный тип объекта.")
        return redirect('error_page')  # или другой URL

    if request.method == "POST":
        form = ShareForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            permission_type = form.cleaned_data['permission_type']

            try:
                shared_with = User.objects.get(username=username)

                if shared_with == request.user:
                    messages.error(request, "Вы не можете выдать доступ самому себе.")
                    return redirect('folders')

                Permission.objects.update_or_create(
                    user=request.user,
                    permitted_user=shared_with,
                    folder=obj if type == 'folder' else None,
                    file=obj if type == 'file' else None,
                    defaults={'permission_type': permission_type},
                )

                if type == 'folder':
                    for file in files_in_folder:
                        Permission.objects.update_or_create(
                            user=request.user,
                            permitted_user=shared_with,
                            file=file,
                            defaults={'permission_type': permission_type},
                        )

                messages.success(request, "Доступ успешно предоставлен.")
                return redirect('folders')

            except User.DoesNotExist:
                messages.error(request, "Пользователь не найден.")
                return redirect('folders')

    else:
        form = ShareForm()

    return render(request, 'yayd/share_access.html', {'form': form, 'object': obj, 'type': type})

@login_required
def shared_access(request):
    permissions = Permission.objects.filter(permitted_user=request.user)
    
    folders = [perm.folder for perm in permissions if perm.folder]
    files = [perm.file for perm in permissions if perm.file]

    editable_files = [perm.file for perm in permissions if perm.file and perm.permission_type == Permission.EDIT]

    return render(request, 'yayd/shared_access.html', {
        'folders': folders,
        'files': files,
        'editable_files': editable_files,
    })