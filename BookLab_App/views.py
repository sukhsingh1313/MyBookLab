from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.http import Http404
from .models import BooksLibrary, social_links, topbar_changes, Categories
from .forms import contectForm,CustomPasswordResetForm
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

@login_required(login_url="login_view")
def open_book_function(request, slug, format_type):
    try:
        book = get_object_or_404(BooksLibrary,slug = slug)
        if format_type == 'pdf':
            file_path = book.pdf_file.path
            content_type = 'application/pdf'
        elif format_type == 'epub':
            if not book.epub_file:
                raise Http404("EPUB file not available.")
            file_path = book.epub_file.path
            content_type = 'application/epub+zip'
        else:
            raise Http404("Requested format is not supported.")
        
        with open(file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type=content_type)
            response['Content-Disposition'] = f'inline; filename="{book.title}.{format_type}"'
            return response
    except BooksLibrary.DoesNotExist:
        raise Http404("File not found.")
    except Exception as e:
        raise Http404(f"An error occurred: {str(e)}")

@login_required(login_url='login_view')
def purchase_book(request,book_id):
    book = get_object_or_404(BooksLibrary, id = book_id)
    if book.is_free():
        return redirect('view_book', slug=book.slug,format_type= 'pdf' )
    else:
        return HttpResponse('payment getway is not working ...')

def main_book_section(request):
    categorie = Categories.objects.prefetch_related('book_library').all()
    books = BooksLibrary.objects.select_related('category').all()
    social_link = social_links.objects.all()
    bar_name_changes = topbar_changes.objects.all()
    context = {
        'categorie': categorie,
        'books': books,
        'social_link': social_link,
        'bar_name_changes': bar_name_changes

    }
    
    return render(request, 'booklibrary.html',context)



def BookDetail_view(request, slug):
    try:
        bookdetail = get_object_or_404(BooksLibrary, slug=slug)
        return render(request, 'BookDetail.html', {'bookdetail': bookdetail})
    except BooksLibrary.DoesNotExist:
        raise Http404("Book not found.")


def search_books_view(request):
    query = request.GET.get('query', '')
    result = []
    if query:
        result = BooksLibrary.objects.filter(title__icontains=query)
    return render(request, 'search_books.html', {'result': result, 'query': query})

def all_books_view(request):
   books = BooksLibrary.objects.all()
   return render(request, 'all_books.html', {'books': books})


def contect_view(request):
    if request.method == 'POST':
        form = contectForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request,'contect_success.html')
    else:
        form = contectForm
        return render(request, 'contect.html', {'form': form})
    

class CustomPasswordResetView(SuccessMessageMixin, PasswordResetView):
    template_name = 'password_reset.html'
    email_template_name = 'password_reset_email.html'
    success_message = "We've emailed you instructions for resetting your password. If an account exists with the provided email, you should receive an email shortly."
    success_url = reverse_lazy('password_reset_done')
    form_class = CustomPasswordResetForm
    def get_context_data(self, **kwargs):
         context = super().get_context_data(**kwargs)
         context['protocol'] = 'http' if self.request.is_secure() else 'https'
         context['domain'] = self.request.get_host() 
         return context
    

# payment function

    

