from django.db import models

# Create your models here.
class MachineModel(models.Model):
    MOVE_RISK_CHOICES = [('High', 'High'), ('Medium', 'Medium'), ('Low', 'Low')]
    model_name = models.CharField(max_length=255, primary_key=True)
    manufacturer = models.CharField(max_length=255, blank=True, null=True)
    model_type = models.CharField(max_length=255, blank=True, null=True)
    machine_move_risk = models.CharField(max_length=20, choices=MOVE_RISK_CHOICES, blank=True, null=True, help_text="Risk associated with moving this machine")
    current_amps = models.FloatField(blank=True, null=True, help_text="Current (in amps) required by the machine")
    is_depreciated = models.BooleanField(default=False, help_text="Indicates if the model is depreciated")
    depreciated_since = models.DateField(blank=True, null=True, help_text="Date when the model was marked as depreciated")
    dimensions = models.JSONField(blank=True, null=True, help_text="Cabinet dimensions as {'height': , 'width': , 'depth': }")
    weight = models.FloatField(blank=True, null=True, help_text="Weight of the machine in lb")
    screen_size = models.FloatField(blank=True, null=True, help_text="Screen size in inches")
    model_image = models.ImageField(upload_to='model_pics/', blank=True, null=True, help_text="Image of the model")

    def __str__(self):
        return f"{self.model_name} - {self.model_type or 'Unknown Type'}"

    def get_dimension_str(self):
        if self.dimensions:
            return f"{self.dimensions.get('height', 'N/A')} x {self.dimensions.get('width', 'N/A')} x {self.dimensions.get('depth', 'N/A')} cm"
        return "Dimensions not specified"

    class Meta:
        verbose_name = "Slot Machine Model"
        verbose_name_plural = "Slot Machine Models"