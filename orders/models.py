from django.db import models
from users.models import User


# Create your models here.

class Order(models.Model):
    # почему-то имено такая раьота с статусами
    CREATED = 0
    PAID = 1
    ON_WAY = 2
    DELIVERED = 3
    STATUSES = (
        (CREATED, 'Создан'),
        (PAID, 'Оплачен'),
        (ON_WAY, 'В пути'),
        (DELIVERED, 'Доставлен'),
    )
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.EmailField(max_length=256)
    address = models.CharField(max_length=256)
    # связь не возможно с Basket так объекты удалются после покупки
    # связать с product тоже не возможна  так как может меняться цена и другие пармаетры
    basket_history = models.JSONField(default=dict)
    created = models.DateTimeField(auto_now_add=True)
    # user  который делает заказ , если удалился пользователь то его заказы удаться автоматически
    initiator = models.ForeignKey(to=User, on_delete=models.CASCADE)
    status = models.SmallIntegerField(default=CREATED, choices=STATUSES)

    def __str__(self):
        return f'Order #{self.id}. {self.first_name} {self.last_name}'
