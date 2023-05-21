from django.db import models
from django.contrib.auth.models import User
from mptt.models import MPTTModel, TreeForeignKey

class Logos(models.Model):
    image = models.ImageField(upload_to='logo')

    class Meta:
        verbose_name = ('logo')
        verbose_name_plural = ('logolar')

class Category(MPTTModel):
    name = models.CharField("Ady", max_length=100, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Bölüm'
        verbose_name_plural = 'Bölümler'   

#algydar
class Recipient(models.Model):
    recipient_adder = models.ForeignKey(User, verbose_name='Admin:', on_delete=models.SET_NULL, null=True, blank=True, to_field='username')
    name_and_lastname = models.CharField(verbose_name='Algydaryň ady we familiýasy:', max_length=200, unique=True)
    birthday = models.DateField(verbose_name='oglan senesi:')
    phone_number = models.CharField(max_length=12, verbose_name='Telefon belgisi:')
    address = models.CharField(max_length=200, verbose_name='Öý salgysy:')
    document_scan = models.FileField(verbose_name='Passport nusgasy:', upload_to="recipient files/", blank=True, null=True)

    def __str__(self):
        return self.name_and_lastname

    class Meta:
        verbose_name = 'Algydar'
        verbose_name_plural = 'Algydarlar'

# algydaryn chagalary.
class RecipientChild(models.Model):
    child_adder = models.ForeignKey(User, verbose_name='Admin:', on_delete=models.SET_NULL, null=True, blank=True, to_field='username')
    recipient = models.ForeignKey(Recipient, to_field='name_and_lastname', on_delete=models.CASCADE, verbose_name='Algydar', related_name='children')
    name_and_lastname = models.CharField(verbose_name='Çaganyň ady we Familiýasy:', max_length=200)
    birthday = models.DateField(verbose_name='Doglan senesi:')
    document_scan = models.FileField(verbose_name='Şahadatnama nusgasy', upload_to="recipient child files/", blank=True, null=True)

    def __str__(self):
        return self.name_and_lastname

    class Meta:
        verbose_name = 'Algydaryň çagasy'
        verbose_name_plural = 'Algydarlaryň çagalary'

# bergidarlar
class MustPay(models.Model):
    name_and_lastname = models.CharField(verbose_name='Bergidaryň ady we familiýasy:', max_length=200, unique=True)
    birthday = models.DateField(verbose_name='Doglan senesi:')
    phone_number = models.CharField(max_length=12, verbose_name='Telefon belgisi 1:')
    phone_number2 = models.CharField(max_length=12, verbose_name='Telefon belgisi 2:', null=True, blank=True) 
    address = models.CharField(max_length=200, verbose_name='Öý salgysy:')
    document_scan = models.FileField(verbose_name='Passport nusgasy:', upload_to='must pay files/', blank=True, null=True) #atlyfayl
    job_status = models.CharField(max_length=100, verbose_name='Işleýän ýeri:')

    def __str__(self):
        return self.name_and_lastname

    class Meta:
        verbose_name = 'Bergidar'
        verbose_name_plural = 'Bergidarlar'

# tolegler
class MustPayReceipt(models.Model):
    must_pay = models.ForeignKey(MustPay, to_field='name_and_lastname', on_delete=models.CASCADE, verbose_name='Bergidar:', related_name='receipts')
    full_assessment = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Tölegiň doly möçberi:')
    payment = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Tölenen möçberi:')
    payment_date = models.DateField(verbose_name='Iň soňky tölenen senesi:')
    currency = models.CharField(max_length=20, verbose_name='Walýuta:')
    document_scan = models.FileField(verbose_name='Tölegi tassyklaýan resminama:', upload_to="must pay receipt files/", blank=True, null=True)
    alimony_percent = models.IntegerField(verbose_name='alimentiň göterimi:')

    def __str__(self):
        return self.currency

    class Meta:
        verbose_name = 'Töleg'
        verbose_name_plural = 'Tölegler'
        get_latest_by = 'id'

# alimentler.
class Alimony(models.Model):
    user = models.ForeignKey(User, verbose_name='Admin:', on_delete=models.SET_NULL, null=True)
    Category = models.ForeignKey(Category, to_field='name', verbose_name='Bölum:', on_delete=models.SET_NULL, null=True, related_name='alimonies')
    ruling = models.CharField(verbose_name='Karary çykaran:', max_length=100)
    ruling_date = models.DateField(verbose_name='Kararyň senesi:')
    began_paying = models.DateField(verbose_name='Alimenti töläp başlan wagty:')
    ruling_scan = models.FileField(verbose_name='Kararyň nusgasy:', upload_to="alimony files/", blank=True, null=True)
    executor = models.CharField(verbose_name='Ýerine ýetirýän:', max_length=100)
    executor_register = models.CharField(verbose_name='Önumçiligiň belgisi:', max_length=100)
    executor_date = models.DateTimeField(verbose_name='Önumciligiň senesi:')
    must_pay = models.ForeignKey(MustPay, verbose_name='Bergidaryň ady we familiýasy:', on_delete=models.CASCADE, related_name='alimonies')
    recipient = models.ForeignKey(Recipient, verbose_name='Algydaryn ady we familiyasy:', on_delete=models.CASCADE, related_name='alimonies')
    note = models.TextField(verbose_name='Bellik:', blank=True)
    status = models.BooleanField(verbose_name='Işiň statusy:', default=False)
    created_at = models.DateTimeField('Işiň döredilen senesi:', auto_now_add=True)


    class Meta:
        verbose_name = 'Aliment'
        verbose_name_plural = 'Alimentlar'
