from django.db import models
from maintenance.models import SlotMachineMaintenanceForm
from slot_importer.models import SlotMachine
# Represents a test performed on a slot machine as part of maintenance
class MachineTest(models.Model):
    maintenance_form = models.ForeignKey(
        SlotMachineMaintenanceForm, 
        on_delete=models.CASCADE, 
        related_name="live_game_test"
    )

    machine = models.ForeignKey(
        SlotMachine, 
        on_delete=models.CASCADE, 
        related_name="machine_tests",
        blank=True, 
        null=True, 
        help_text="The slot machine associated with this test"
    )

    

    def __str__(self):
        return f"Machine Test Record for {self.maintenance_form}"
   

# Records the initial state of various metrics before maintenance
class SoftGMUBefore(models.Model):
    casino_test_record = models.OneToOneField(
        MachineTest, 
        on_delete=models.CASCADE, 
        related_name="soft_gmu_before"
    )
    non_cashable_promo_in = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        blank=True, 
        null=True, 
        help_text="Before value of non-cashable promo in"
    )
    cashable_promo_in = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        blank=True, 
        null=True, 
        help_text="Before value of cashable promo in"
    )
    non_cashable_promo_out = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        blank=True, 
        null=True, 
        help_text="Before value of non-cashable promo out"
    )
    coin_in_bets = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        blank=True, 
        null=True, 
        help_text="Before value of coin-in bets"
    )
    coin_out_wins = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        blank=True, 
        null=True, 
        help_text="Before value of coin-out wins"
    )
    jackpot_handpaid = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        blank=True, 
        null=True, 
        help_text="Before value of jackpot handpaid"
    )
    cash_ticket_in = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        blank=True, 
        null=True, 
        help_text="Before value of cash ticket in"
    )
    cash_ticket_out = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        blank=True, 
        null=True, 
        help_text="Before value of cash ticket out"
    )
    fives = models.IntegerField(blank=True, null=True, help_text="Before value for $5 bills")
    tens = models.IntegerField(blank=True, null=True, help_text="Before value for $10 bills")
    twenties = models.IntegerField(blank=True, null=True, help_text="Before value for $20 bills")
    fifties = models.IntegerField(blank=True, null=True, help_text="Before value for $50 bills")
    hundreds = models.IntegerField(blank=True, null=True, help_text="Before value for $100 bills")
    player_tracking = models.IntegerField(blank=True, null=True, help_text="Player tracking value before")

    def __str__(self):
        return f"Soft GMU Before Record for {self.casino_test_record}"


# Records the final state of various metrics after maintenance
class SoftGMUAfter(models.Model):
    casino_test_record = models.OneToOneField(
        MachineTest, 
        on_delete=models.CASCADE, 
        related_name="soft_gmu_after"
    )
    non_cashable_promo_in = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        blank=True, 
        null=True, 
        help_text="After value of non-cashable promo in"
    )
    cashable_promo_in = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        blank=True, 
        null=True, 
        help_text="After value of cashable promo in"
    )
    non_cashable_promo_out = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        blank=True, 
        null=True, 
        help_text="After value of non-cashable promo out"
    )
    coin_in_bets = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        blank=True, 
        null=True, 
        help_text="After value of coin-in bets"
    )
    coin_out_wins = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        blank=True, 
        null=True, 
        help_text="After value of coin-out wins"
    )
    jackpot_handpaid = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        blank=True, 
        null=True, 
        help_text="After value of jackpot handpaid"
    )
    cash_ticket_in = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        blank=True, 
        null=True, 
        help_text="After value of cash ticket in"
    )
    cash_ticket_out = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        blank=True, 
        null=True, 
        help_text="After value of cash ticket out"
    )
    fives = models.IntegerField(blank=True, null=True, help_text="After value for $5 bills")
    tens = models.IntegerField(blank=True, null=True, help_text="After value for $10 bills")
    twenties = models.IntegerField(blank=True, null=True, help_text="After value for $20 bills")
    fifties = models.IntegerField(blank=True, null=True, help_text="After value for $50 bills")
    hundreds = models.IntegerField(blank=True, null=True, help_text="After value for $100 bills")
    player_tracking = models.IntegerField(blank=True, null=True, help_text="Player tracking value after")

    def __str__(self):
        return f"Soft GMU After Record for {self.casino_test_record}"


class ProgressiveBefore(models.Model):
    casino_test_record = models.ForeignKey(
        'MachineTest',
        on_delete=models.CASCADE,
        related_name="progressive_pools_before"
    )
    pool_name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Name or identifier for the progressive pool before maintenance."
    )
    level = models.PositiveIntegerField(
        blank=True,
        null=True,
        default=1,
        help_text="Level of the progressive meter before maintenance (e.g., 1 for Grand, 2 for Major)."
    )
    value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Dollar amount before maintenance."
    )

    def __str__(self):
        return (
            f"Progressive Pool Before '{self.pool_name or 'Unnamed'}' "
            f"(Level {self.level or 'N/A'}, Value: {self.value})"
        )


class ProgressiveAfter(models.Model):
    casino_test_record = models.ForeignKey(
        'MachineTest',
        on_delete=models.CASCADE,
        related_name="progressive_pools_after"
    )
    pool_name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Name or identifier for the progressive pool after maintenance."
    )
    level = models.PositiveIntegerField(
        blank=True,
        null=True,
        default=1,
        help_text="Level of the progressive meter after maintenance (e.g., 1 for Grand, 2 for Major)."
    )
    value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Dollar amount after maintenance."
    )

    def __str__(self):
        return (
            f"Progressive Pool After '{self.pool_name or 'Unnamed'}' "
            f"(Level {self.level or 'N/A'}, Value: {self.value})"
        )


# Tracks bets and wins recorded during testing
class BetWin(models.Model):
    casino_test_record = models.ForeignKey(
        MachineTest, 
        on_delete=models.CASCADE, 
        related_name="bet_win"
    )
    bet = models.DecimalField(max_digits=10, decimal_places=2)
    won = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Bet: {self.bet}, Won: {self.won} for {self.casino_test_record}"


class TestParameters(models.Model):
    casino_test_record = models.ForeignKey(
        MachineTest, 
        on_delete=models.CASCADE, 
        related_name="test_parameters"
    )
    promo = models.DecimalField(max_digits=5, decimal_places=2, default=5.00)
    points = models.DecimalField(max_digits=5, decimal_places=2, default=5.00)
    denom_5 = models.BooleanField(default=False)
    denom_10 = models.BooleanField(default=False)
    denom_20 = models.BooleanField(default=False)
    denom_50 = models.BooleanField(default=False)
    denom_100 = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Test Parameters for {self.casino_test_record}"
