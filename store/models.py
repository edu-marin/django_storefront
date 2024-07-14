# models.py
from django.db import models
from django.contrib.auth.models import User

# Tabla de Clientes
class Customer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

# Tabla de Categorías
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

# Tabla de Productos
class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def update_cost(self):
        inventory_entries = Inventory.objects.filter(product=self)
        total_cost = inventory_entries.aggregate(total_cost=models.Sum(models.F('cost') * models.F('quantity')))['total_cost']
        total_quantity = inventory_entries.aggregate(total_quantity=models.Sum('quantity'))['total_quantity']

        if total_quantity and total_quantity > 0:
            average_cost = total_cost / total_quantity
            self.cost = average_cost
            self.save()

    def __str__(self):
        return self.name

    def get_stock(self):
        total_stock = Inventory.objects.filter(product=self).aggregate(total=models.Sum('quantity'))['total']
        return total_stock if total_stock else 0

# Tabla de Proveedores
class Supplier(models.Model):
    name = models.CharField(max_length=100)
    contact_info = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

# Tabla de Inventario
class Inventory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    entry_date = models.DateTimeField(auto_now_add=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    batch_number = models.CharField(max_length=100, null=True, blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.product.update_cost()

    def __str__(self):
        return f'{self.product.name} - {self.quantity} units'

# Tabla de Promociones
class Promotion(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return self.name

# Tabla de Órdenes
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def update_total(self):
        self.total_amount = sum(item.final_price * item.quantity for item in self.order_details.all())
        self.save()

    def __str__(self):
        return f'Order {self.id} - {self.customer.first_name} {self.customer.last_name}'

# Tabla de Detalles de Órdenes
class OrderDetail(models.Model):
    order = models.ForeignKey(Order, related_name='order_details', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    final_price = models.DecimalField(max_digits=10, decimal_places=2)
    promotion = models.ForeignKey(Promotion, null=True, blank=True, on_delete=models.SET_NULL)

    def save(self, *args, **kwargs):
        if self.discount:
            self.final_price = self.unit_price - self.discount
        else:
            self.final_price = self.unit_price
        super().save(*args, **kwargs)
        self.order.update_total()

    def __str__(self):
        return f'{self.product.name} - {self.quantity} units at {self.final_price} each'
