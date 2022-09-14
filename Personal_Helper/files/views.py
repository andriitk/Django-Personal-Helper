from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UploadFileForm
from .models import Files
from django.http import FileResponse
from django.views.generic import ListView
from django.contrib import messages
from django.db.models import Q
import os


class FilesByUser(ListView):
    login_required(login_url='home')
    model = Files
    template_name = 'files/files_view.html'
    context_object_name = 'files_data'

    def get_queryset(self):
        return Files.objects.filter(user=self.request.user)


@login_required(login_url='home')
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)

        if form.is_valid():
            filename = request.FILES['uploadfile'].name
            form.instance.user = request.user
            form.save()
            messages.success(request, 'Success added')
            return redirect('upload_file')

    else:
        form = UploadFileForm()
        return render(request, "files/upload_file.html", {"form": form})


@login_required(login_url='home')
def delete_file(request, file_id):
    file = Files.objects.get(pk=file_id)
    file.delete()
    os.remove(f'./media/{file.uploadfile}')

    return redirect('files')


@login_required(login_url='home')
def download_file(request, file_id):
    file = Files.objects.get(pk=file_id)

    filepath = f'./media/{file.uploadfile}'
    filename = filepath.split('/')[6]

    path = open(filepath, 'rb')
    return FileResponse(path, as_attachment=True, filename=filename,
                        content_type=f'application/{filename.split(".")[1]}')


class Search(ListView):
    login_required(login_url='home')
    model = Files
    template_name = 'files/files_view.html'
    context_object_name = 'files_data'

    def get_queryset(self):
        if self.request.GET.get('q') is None:
            return None
        return Files.objects.filter(title__icontains=self.request.GET.get('q'), user=self.request.user)


class ImagesFiles(ListView):
    login_required(login_url='home')
    model = Files
    template_name = 'files/files_view.html'
    context_object_name = 'files_data'

    def get_queryset(self):
        return Files.objects.filter(
            Q(uploadfile__endswith='.jpeg', user=self.request.user) |
            Q(uploadfile__endswith='.png', user=self.request.user) |
            Q(uploadfile__endswith='.jpg', user=self.request.user) |
            Q(uploadfile__endswith='.svg', user=self.request.user))


class DocsFiles(ListView):
    login_required(login_url='home')
    model = Files
    template_name = 'files/files_view.html'
    context_object_name = 'files_data'

    def get_queryset(self):
        return Files.objects.filter(
            Q(uploadfile__endswith='.doc', user=self.request.user) |
            Q(uploadfile__endswith='.docx', user=self.request.user) |
            Q(uploadfile__endswith='.txt', user=self.request.user) |
            Q(uploadfile__endswith='.rtf', user=self.request.user))


class PDFFiles(ListView):
    login_required(login_url='home')
    model = Files
    template_name = 'files/files_view.html'
    context_object_name = 'files_data'

    def get_queryset(self):
        return Files.objects.filter(
            Q(uploadfile__endswith='.pdf', user=self.request.user) |
            Q(uploadfile__endswith='.pptx', user=self.request.user))
