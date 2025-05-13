from django.db import models
from django.utils.text import slugify

class Categories(models.Model):
    id  = models.IntegerField(primary_key=True)
    name =  models.CharField(max_length=100,unique=True)
    description = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.name

# Create your models here.
class BooksLibrary(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    category = models.ForeignKey(Categories,on_delete=models.CASCADE,related_name="book_library")
    decription_book = models.TextField(max_length=1000,blank=True, null=True)
    image = models.ImageField(upload_to='')
    pdf_file = models.FileField(upload_to='',blank=True, null=True)
    epub_file = models.FileField(upload_to='', blank=True, null=True)
    publication_date = models.DateField()
    book_language =  models.CharField(max_length=50,blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=250,unique=True,blank=True,null=True)
    price  = models.DecimalField(max_digits=10,decimal_places=2,default=0.00)
    # is_free = models.BooleanField(default=False)  # New field


    def is_free(self):
        return self.price == 0.00 
    
    def save(self, *args, **kwargs):
        if not self.slug and self.title:
            self.slug = slugify(self.title)
        super(BooksLibrary, self).save(*args, **kwargs)


   
    
    def __str__(self):
        return self.title


class topbar_changes(models.Model):
    logo  = models.ImageField(upload_to='',blank=True, null=True)
    menu_name = models.CharField(max_length=30,null=True,blank=True)
    background_image = models.ImageField(upload_to='',blank=True, null=True)
    background_color = models.CharField(max_length=10,blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.menu_name
    
class social_links(models.Model):
    name = models.CharField(max_length=50,blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
    

#contect model

class Contact(models.Model):
    name = models.CharField(max_length=100,blank=True, null=True)
    email = models.EmailField(max_length=100,blank=True, null=True)
    message = models.TextField(max_length=1000,blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.name} - {self.email}"