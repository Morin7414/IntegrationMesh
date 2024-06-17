from django.db.models import Count
from workorder.models import WorkOrder

def get_maintenance_ticket_counts():
    counts = WorkOrder.objects.values('maintenance_ticket').annotate(count=Count('maintenance_ticket'))
    return {item['maintenance_ticket']: item['count'] for item in counts}