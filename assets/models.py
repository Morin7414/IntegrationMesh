from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Model(models.Model):
    CABINET_TYPES = [
        ('Slant Video', 'Slant Video'),
        ('Upright Video', 'Upright Video'),
    ]
    MOVE_RISK_CHOICES = [
        ('High', 'High'),
        ('Medium', 'Medium'),
        ('Low', 'Low'),
    ]
    VENDOR_CHOICES = [
        ('Konami', 'Konami'),
        ('IGT', 'IGT'),
        ('Bally', 'Bally'),
        ('WMS', 'WMS'),
        ('Ainsworth', 'Ainsworth'),
        ('Aristocrat', 'Aristocrat'),
        ('Sci Games', 'Sci Games'),
        ('Everi', 'Everi'),
        ('Spielo', 'Spielo'),
        ('AGS', 'AGS'),
        ('Aruze', 'Aruze'),
        ('LnW', 'LnW'),
        ('Incredible Technologies', 'Incredible Technologies'),
    ]
    model_name = models.CharField(max_length=255,primary_key=True)
    vendor = models.CharField(max_length=50, choices=VENDOR_CHOICES)
    machine_move_risk = models.CharField(max_length=20, choices=MOVE_RISK_CHOICES)
    cabinet_type = models.CharField(max_length=20, choices=CABINET_TYPES)
    current_amps = models.FloatField()
    def __str__(self):
        return self.model_name

class MachineMaster(models.Model):
    serial_number = models.CharField(max_length=255, primary_key=True)
    asset_number = models.CharField(max_length=255)
    model_name = models.ForeignKey(Model, on_delete=models.PROTECT, null=True)
    game_theme = models.CharField(max_length=255)
    date_PM = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Asset Number: {self.asset_number} Model: {self.model_name} Game Theme: {self.game_theme}"




  








  
    