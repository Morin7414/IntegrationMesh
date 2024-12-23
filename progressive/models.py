from django.db import models
from casinos.models import Casino
from machine_models.models import MachineModel


# Create your models here.
class BankedProgressive(models.Model):
    progressive_name = models.CharField(max_length=100)
    casino = models.ForeignKey(Casino, on_delete=models.SET_NULL, null=True, related_name='banked_progressive')  # Ensure 'Casino' is the correct model name
    machine_model_name = models.ForeignKey(MachineModel, to_field="model_name", on_delete=models.SET_NULL, null=True, related_name='banked_progressive')  # Use a unique related_name

    def __str__(self):
        return f"{self.progressive_name}"


# BankedLevel model
class BankedLevel(models.Model):
    banked_progressive = models.ForeignKey(BankedProgressive, on_delete=models.CASCADE, related_name='banked_levels')
    seed_level = models.DecimalField(max_digits=10, decimal_places=2, help_text="Initial seed amount for the level")
    max_amount= models.DecimalField(
        max_digits=10, decimal_places=2, default=99999999.00, help_text="Overflow amount exceeding the max level"
    )
    progressive_increment_percent = models.DecimalField(max_digits=5, decimal_places=2, help_text="Increment percentage for the progressive")
    current_amount = models.DecimalField(max_digits=10, decimal_places=2, help_text="Current amount of the level")
    overflow_amount = models.DecimalField(max_digits=10, decimal_places=2, help_text="Overflow amount exceeding the max level")

    def __str__(self):
        return f"Level for {self.banked_progressive.progressive_name} - Current: {self.current_amount}"
    

class BEPS(models.Model):
    progressive_name = models.CharField(max_length=100)
   
    def __str__(self):
        return f"{self.progressive_name}"
    
# BEPSLevel model
class BEPSLevel(models.Model):
    beps = models.ForeignKey(BEPS, on_delete=models.CASCADE, related_name='beps_levels')
    seed_level = models.DecimalField(max_digits=10, decimal_places=2, help_text="Initial seed amount for the level")
    max_amount= models.DecimalField(
        max_digits=10, decimal_places=2, default=99999999.00, help_text="Overflow amount exceeding the max level"
    )
    progressive_increment_percent = models.DecimalField(max_digits=5, decimal_places=2, help_text="Increment percentage for the progressive")
    current_amount = models.DecimalField(max_digits=10, decimal_places=2, help_text="Current amount of the level")
    overflow_amount = models.DecimalField(max_digits=10, decimal_places=2, help_text="Overflow amount exceeding the max level")

    def __str__(self):
        return f"Level for {self.beps.progressive_name} - Current: {self.current_amount}"
    

    
class Progressive(models.Model):
    PROGRESSIVE_TYPES = [
        ('BANKED', 'Banked Progressive'),
        ('BEPS', 'BEPS Progressive'),
        ('STANDALONE', 'Standalone Progressive'),
    ]

    progressive_name = models.CharField(max_length=255)
    progressive_type = models.CharField(max_length=50, choices=PROGRESSIVE_TYPES)

    banked_progressive = models.ForeignKey(
        BankedProgressive,  # Lazy reference to avoid circular import
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name="progressive_banked"
    )

    beps = models.ForeignKey(
        BEPS,  # Lazy reference to avoid circular import
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name="progressive_banked"
    )


    def __str__(self):
        return f"{self.progressive_name} ({self.get_progressive_type_display()})"
    

#StandAlone
class StandAloneLevel(models.Model):
    stand_alone_progressive= models.ForeignKey(Progressive, on_delete=models.CASCADE, related_name='stand_alone_levels')
    progressive_pool = models.CharField(
        max_length=100,
        null =True, 
        blank = True,
        help_text="Identifier for the progressive pool, e.g., denomination or game theme"
    )
    seed_level = models.DecimalField(max_digits=10, decimal_places=2, help_text="Initial seed amount for the level")
    max_amount= models.DecimalField(
        max_digits=10, decimal_places=2, default=99999999.00, help_text="Overflow amount exceeding the max level"
    )
    progressive_increment_percent = models.DecimalField(max_digits=5, decimal_places=2, help_text="Increment percentage for the progressive")
    current_amount = models.DecimalField(max_digits=10, decimal_places=2, help_text="Current amount of the level")
    overflow_amount = models.DecimalField(max_digits=10, decimal_places=2, help_text="Overflow amount exceeding the max level")

    def __str__(self):
        return (
            f"Level for {self.stand_alone_progressive} "
            f"(Pool: {self.progressive_pool}) - Current: {self.current_amount}"
        )
    