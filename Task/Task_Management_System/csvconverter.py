import csv

from django.http import HttpResponse


def export_to_csv(tasks):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="task_report.csv"'
    writer = csv.writer(response)
    writer.writerow(['Sr No', 'Title', 'Description', 'Start Date', 'End Date', 'Priority', 'Status'])
    for index, task in enumerate(tasks, start=1):
        writer.writerow([
            index,
            task.title,
            task.description,
            task.start_date,
            task.end_date,
            task.get_priority_display(),
            task.get_status_display(),])
    return response
