from django.shortcuts import render
from django.shortcuts import render

from .forms import CSVUploadForm
from .models import CSVData
import pandas as pd

def upload_csv(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            df = pd.read_csv(csv_file)

            # iterate over the rows of the CSV file and save them to the database
            for index, row in df.iterrows():
                CSVData.objects.create(
                    image_name=row['image_name'],
                    objects_detected=row['objects_detected'],
                    timestamp=row['timestamp']
                )

            return render(request, 'success.html')
    else:
        form = CSVUploadForm()

    return render(request, 'upload.html', {'form': form})

def search(request):
    if request.method == 'POST':
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']

        # Query the database for CSVData objects within the given date range
        results = CSVData.objects.filter(timestamp__range=[start_date, end_date])

        # Generate the report CSV file
        import csv
        from django.http import HttpResponse

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="report.csv"'

        writer = csv.writer(response)
        writer.writerow(['Image Name', 'Detections'])

        # Iterate over the results and count the total number of detections
        total_detections = 0
        for result in results:
            detections = result.objects_detected.split(',')
            total_detections += len(detections)
            writer.writerow([result.image_name, result.objects_detected])

        writer.writerow(['Total Detections', total_detections])

        return response
    else:
        return render(request, 'search.html')

# Create your views here.
