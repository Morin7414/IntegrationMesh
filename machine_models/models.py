from django.db import models


class MachineModel(models.Model):
    MOVE_RISK_CHOICES = [('High', 'High'), ('Medium', 'Medium'), ('Low', 'Low')]
    model_name = models.CharField(max_length=255, primary_key=True)
    manufacturer = models.ForeignKey(
        'Manufacturer',  # Reference the Manufacturer model
        on_delete=models.CASCADE,  # Delete all related MachineModel instances if the Manufacturer is deleted
        related_name='machine_models',  # Allows reverse lookup from Manufacturer to MachineModel
        help_text="Manufacturer of this machine",
        null = True
    )
    model_type = models.CharField(max_length=255, blank=True, null=True)
    machine_move_risk = models.CharField(max_length=20, choices=MOVE_RISK_CHOICES, blank=True, null=True, help_text="Risk associated with moving this machine")
    current_amps = models.FloatField(blank=True, null=True, help_text="Current (in amps) required by the machine")
    is_end_of_life = models.BooleanField(default=False, help_text="Indicates if the model is at the end of its life")
    end_of_life_date = models.DateField(blank=True, null=True, help_text="Date when the model was marked as end of life")
    model_image = models.ImageField(upload_to='model_pics/', blank=True, null=True, help_text="Image of the model")

    def __str__(self):
       # return f"{self.model_name} - {self.model_type or 'Unknown Type'}"
       return f"{self.model_name}"

    class Meta:
        verbose_name = "Slot Machine Model"
        verbose_name_plural = "Slot Machine Models"




class Manufacturer(models.Model):
    name = models.CharField(max_length=255, unique=True, help_text="Name of the manufacturer")
    website = models.URLField(blank=True, null=True, help_text="Official website of the manufacturer")
    logo = models.ImageField(upload_to='manufacturer_logos/', blank=True, null=True, help_text="Logo or picture of the manufacturer")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Manufacturer"
        verbose_name_plural = "Manufacturers"