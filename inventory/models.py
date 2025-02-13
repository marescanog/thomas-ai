from django.db import models
class Products(models.Model):
    product_id = models.IntegerField(primary_key=True, db_column='Product Id')
    product_name = models.CharField(max_length=255) 
    class_index = models.IntegerField()
    class_label_name = models.CharField(max_length=255)      
    made_in = models.CharField(max_length=255)
    made_by = models.CharField(max_length=255)
    sugar_content = models.CharField(max_length=100)   
    varietal = models.CharField(max_length=255)
    alcohol_volume = models.FloatField()
    product_details = models.TextField(blank=True, null=True)
    product_type = models.CharField(max_length=50)
    
    class Meta:
        db_table = 'alcohol_inventory'
        verbose_name = 'Alcohol Product'
        verbose_name_plural = 'Alcohol Products'
    
    def __str__(self):
        return self.class_label_name  

