from django.contrib import admin
from .models import (
    MachineTest,
    SoftGMUBefore,
    SoftGMUAfter,
    ProgressiveBefore,
    ProgressiveAfter,
    BetWin,
    TestParameters
)


class SoftGMUBeforeInline(admin.StackedInline):
    model = SoftGMUBefore
    extra = 0  # No extra blank forms


class SoftGMUAfterInline(admin.StackedInline):
    model = SoftGMUAfter
    extra = 0  # No extra blank forms


class ProgressiveBeforeInline(admin.TabularInline):
    model = ProgressiveBefore
    extra = 0  # No extra blank forms


class ProgressiveAfterInline(admin.TabularInline):
    model = ProgressiveAfter
    extra = 0  # No extra blank forms


class BetWinInline(admin.TabularInline):
    model = BetWin
    extra = 0  # No extra blank forms


class TestParametersInline(admin.StackedInline):
    model = TestParameters
    extra = 0  # No extra blank forms


@admin.register(MachineTest)
class MachineTestAdmin(admin.ModelAdmin):
    list_display = ('maintenance_form', )
    search_fields = ('maintenance_form__name',)  # Adjust based on maintenance_form fields
    raw_id_fields = ('maintenance_form','machine')
    inlines = [
        SoftGMUBeforeInline,
        SoftGMUAfterInline,
        ProgressiveBeforeInline,
        ProgressiveAfterInline,
        BetWinInline,
        TestParametersInline
    ]