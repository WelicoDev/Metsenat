from django.db import models
from django.core.exceptions import ValidationError
from shared.models import BaseModel
import re


UZB_PHONE_REGEX = r"^\+998( ?94| ?[3-9]\d) ?\d{3} ?\d{2} ?\d{2}$"

def validate_uzb_phone(value):
    if not re.match(UZB_PHONE_REGEX, value):
        raise ValidationError("Noto‘g‘ri telefon raqam formati! (+998 XX XXX XX XX)")

INDIVIDUAL = 'individual'
LEGAL_ENTITY = 'legal_entity'

class Sponsor(BaseModel):
    INDIVIDUAL = 'individual'
    LEGAL_ENTITY = 'legal_entity'

    PAYMENT_TYPE_CHOICES = [
        (INDIVIDUAL, 'Jismoniy shaxs'),
        (LEGAL_ENTITY, 'Yuridik shaxs'),
    ]
    STATUS_NEW = 'new'
    STATUS_PENDING = 'pending'
    STATUS_CONFIRMED = 'confirmed'
    STATUS_REJECTED = 'rejected'

    STATUS_CHOICES = [
        (STATUS_NEW, 'Yangi'),
        (STATUS_PENDING, 'Moderatsiyada'),
        (STATUS_CONFIRMED, 'Tasdiqlangan'),
        (STATUS_REJECTED, 'Bekor qilingan'),
    ]

    TRANSFER = 'transfer'
    CASH = 'cash'
    CARD = 'card'

    PAYMENT_METHOD_CHOICES = [
        (TRANSFER, 'Pul o‘tkazmalari'),
        (CASH, 'Naqd pul'),
        (CARD, 'Plastik karta'),
    ]

    payment_type = models.CharField(
        max_length=20,
        choices=PAYMENT_TYPE_CHOICES,
        default=INDIVIDUAL
    )
    full_name = models.CharField(max_length=255, verbose_name="F.I.SH.")
    phone_number = models.CharField(max_length=20, verbose_name="Telefon raqam", validators=[validate_uzb_phone])
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_NEW,
        verbose_name="Holati"
    )
    amount = models.DecimalField(
        max_digits=16,
        decimal_places=2,
        verbose_name="Homiylik summasi"
    )
    payment_method = models.CharField(
        max_length=32,
        choices=PAYMENT_METHOD_CHOICES,
        default=CARD,
        verbose_name="To‘lov turi"
    )
    company_name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Tashkilot nomi"
    )

    comment = models.TextField(blank=True, null=True)



    def save(self, *args, **kwargs):
        if self.payment_type == self.INDIVIDUAL:
            self.company_name = None  # Jismoniy shaxs uchun bu joyni bo'sh qoldiramiz
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.full_name} - {self.amount} UZS"


class University(BaseModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Student(BaseModel):
    DEGREE_CHOICES = [
        ('Bakalavr', 'Bakalavr'),
        ('Magistr', 'Magistr'),
    ]

    full_name = models.CharField(max_length=255, verbose_name="F.I.Sh.")
    phone_number = models.CharField(max_length=20, verbose_name="Telefon raqam", validators=[validate_uzb_phone])
    degree_type = models.CharField(max_length=10, choices=DEGREE_CHOICES, verbose_name="Talabalik turi")
    university = models.ForeignKey(University, on_delete=models.CASCADE, verbose_name="OTM")
    contract_amount = models.PositiveIntegerField(verbose_name="Kontrakt miqdori", default=0)


    def __str__(self):
        return f"{self.full_name} - {self.university}"


class AllocatedAmount(BaseModel):
    sponsor_id = models.ForeignKey(Sponsor, on_delete=models.CASCADE)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    money = models.BigIntegerField()

    def __str__(self):
        return self.money
