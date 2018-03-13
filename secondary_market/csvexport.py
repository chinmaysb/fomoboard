import csv
from django.utils.encoding import smart_str
from django.http import HttpResponse

def export_csv(request, queryset):

    response = HttpResponse()
    response['Content-Type'] = 'text/csv'
    response['Content-Disposition'] = 'attachment; filename=mymodel.csv'
    writer = csv.writer(response, csv.excel)
    response.write(u'\ufeff'.encode('utf8')) # BOM (optional...Excel needs it to open UTF-8 file properly)
    row = []
    for field in queryset.model._meta.fields:
        row.append(smart_str(field.name))
    print(row)
    writer.writerow(row)
    for obj in queryset:
        row = []
        for field in queryset.model._meta.fields:
            row.append(getattr(obj, field.name))
        writer.writerow(row)
        print(row)
    return response