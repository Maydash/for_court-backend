from django.db import models
from decimal import Decimal

class Logos(models.Model):
    image = models.ImageField(upload_to='logo')

    class Meta:
        verbose_name = ("logo")
        verbose_name_plural = ("logolar")

class MustPay(models.Model):
    name_and_lastname = models.CharField(verbose_name='Bergidaryň ady we familiýasy:', max_length=200)
    birthday = models.DateField(verbose_name='Doglan senesi:')
    phone_number = models.CharField(max_length=12, verbose_name='Telefon belgisi 1:')
    phone_number2 = models.CharField(max_length=12, verbose_name='Telefon belgisi 2:', null=True, blank=True) 
    address = models.CharField(max_length=200, verbose_name='Öý salgysy:')
    document_scan = models.FileField(verbose_name='Passport nusgasy', upload_to=f"files/", blank=True, null=True) #atlyfayl
    job_status = models.CharField(max_length=100, verbose_name='Işleýän ýeri:')

    # recipient = models.ForeignKey(...) bu inniki modele baglanmaly.
    # alimony = models.ForeignKey(...) munam bashga bir modele baglamakchy bolyan.

    #bu modele slug gerek bolmazmyka diyyan.

    #api lerini ertir chykarmakchy.
    def __str__(self):
        return self.name_and_lastname

    @property
    def receipt_total(self):
        total = Decimal(0)
        for i in self.mustpayreceipt_set.all():
            total += i.payment
        return total                                      

    class Meta:
        verbose_name = "Bergidar"
        verbose_name_plural = "Bergidarlar"
