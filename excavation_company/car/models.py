from django.db import models
from django_jalali.db import models as jmodels


class Car(models.Model):
    plaque = models.CharField(max_length=6, db_column='پلاک', unique=True)
    Contractor = models.CharField(max_length=100, db_column='پیمانکار')
    car_type = models.CharField(max_length=10, choices=[('تک', 'تک'), ('ده چرخ', 'ده چرخ')], db_column='نوع')

    def __str__(self):
        return f'{self.plaque} - {self.Contractor}'

    class Meta:
        db_table = 'ماشین'


class CarService(models.Model):
    objects = jmodels.jManager()
    car = models.ForeignKey(Car, on_delete=models.CASCADE, db_column='ماشین')
    date = jmodels.jDateField(db_column='تاریخ')
    amount = models.IntegerField(db_column='تعداد سرویس')
    loading = models.CharField(max_length=100, db_column='بارگیری')
    discharge = models.CharField(max_length=100, db_column='تخلیه')
    description = models.CharField(max_length=1000, db_column='توضیحات', null=True, blank=True)

    def __str__(self):
        return f'{self.car.plaque} - {self.date} - {self.amount}'

    class Meta:
        db_table = 'سرویس'
