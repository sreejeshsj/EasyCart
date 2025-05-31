from django.db import models

# Create your models here.

class Category(models.Model):
    category_name=models.CharField(max_length=50,unique=True)
    slug=models.CharField(max_length=100,unique=True)
    description=models.TextField(max_length=200,blank=True)
    cat_image=models.ImageField(upload_to='photos/categorie',blank=True)
    
    class Meta:
        verbose_name='Categorys'
        verbose_name_plural='Categories'
    
    def __str__(self):
        return self.category_name
