from django.contrib import admin


from .models import BankedProgressive, BankedLevel, BEPS, BEPSLevel, StandAloneLevel, Progressive

# Inline for BankedLevel
class BankedLevelInline(admin.TabularInline):
    model = BankedLevel
    extra = 1  # Number of empty forms displayed

# Admin for BankedProgressive
@admin.register(BankedProgressive)
class BankedProgressiveAdmin(admin.ModelAdmin):
    list_display = ('progressive_name', 'casino', 'machine_model_name')
    search_fields = ('progressive_name', 'casino__name', 'machine_model_name__model_name')
    inlines = [BankedLevelInline]

# Inline for BEPSLevel
class BEPSLevelInline(admin.TabularInline):
    model = BEPSLevel
    extra = 1

# Admin for BEPS
@admin.register(BEPS)
class BEPSAdmin(admin.ModelAdmin):
    list_display = ('progressive_name',)
    search_fields = ('progressive_name',)
    inlines = [BEPSLevelInline]

# Inline for StandAloneLevel
class StandAloneLevelInline(admin.TabularInline):
    model = StandAloneLevel
    extra = 1

# Admin for StandAloneLevel
@admin.register(StandAloneLevel)
class StandAloneLevelAdmin(admin.ModelAdmin):
    list_display = ('stand_alone_progressive', 'progressive_pool', 'current_amount', 'max_amount')
    search_fields = ('stand_alone_progressive__progressive_name', 'progressive_pool')
    list_filter = ('stand_alone_progressive__progressive_type',)

# Admin for Progressive
@admin.register(Progressive)
class ProgressiveAdmin(admin.ModelAdmin):
    list_display = ('progressive_name', 'progressive_type')
    search_fields = ('progressive_name', 'progressive_type')
    inlines = [StandAloneLevelInline]

# Note: Add additional configurations if required based on your use case.