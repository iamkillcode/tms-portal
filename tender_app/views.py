from django.shortcuts import render
from datetime import datetime
from .models import TenderTracker, Department

def tender_generator_view(request):
    tender_number = None
    error = None

    if request.method == "POST":
        try:
            department_code = request.POST.get("department_code")  # e.g., PSD
            category_code = request.POST.get("category_code")  # e.g., A.4.1
            procurement_type = request.POST.get("procurement_type")  # e.g., SIS

            prefix = "FDA"
            year = datetime.now().year

            # Check if an entry exists for the year and procurement type
            tracker, created = TenderTracker.objects.get_or_create(
                year=year,
                procurement_type=procurement_type,
                defaults={'last_sequence': 0}
            )

            # Increment the sequence
            tracker.last_sequence += 1
            tracker.save()

            # Generate the tender number
            sequential_number = f"{tracker.last_sequence:04}"  # Zero-padded to 4 digits
            tender_number = f"{prefix}/{department_code}/{year}/{category_code}/{procurement_type}-{sequential_number}"

        except Exception as e:
            error = str(e)
            
             # Fetch department codes from the database
    department_codes = Department.objects.values_list('code', flat=True)

    return render(request, "tender_generator.html", {
        "tender_number": tender_number,
        "error": error,
        "department_codes": department_codes
    })

    # context = {
    #     "tender_number": tender_number,
    #     "error": error,
    # }
    # return render(request, "tender_generator.html", context)