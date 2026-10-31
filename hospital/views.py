from .prediction import predict_patient_flow
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Patient, HospitalBed
from django.shortcuts import get_object_or_404


def home(request):
    return render(request, 'hospital/home.html')


def register(request):
    if request.method == 'POST':
        try:
            Patient.objects.create(
                patient_name=request.POST.get('name'),
                email=request.POST.get('email'),
                age=request.POST.get('age'),
                gender=request.POST.get('gender'),
                phone=request.POST.get('phone'),
                address=request.POST.get('address'),
                symptoms=request.POST.get('symptoms', '')
            )
            messages.success(request, 'Patient registered successfully!')
            return redirect('register')
        except Exception:
            messages.error(request, 'Registration failed. Please check the details.')

    return render(request, 'hospital/register.html')


def patient_records(request):
    search_query = request.GET.get('search', '').strip()

    patients = Patient.objects.all().order_by('-created_at')

    if search_query:
        patients = patients.filter(
            patient_name__icontains=search_query
        )

    return render(
        request,
        'hospital/patient_records.html',
        {
            'patients': patients,
            'search_query': search_query,
        }
    )


def dashboard(request):
    total_patients = Patient.objects.count()
    recent_patients = Patient.objects.order_by('-created_at')[:5]

    predicted_patients = predict_patient_flow()

    total_beds = HospitalBed.objects.count()
    available_beds = HospitalBed.objects.filter(
        is_occupied=False
    ).count()
    occupied_beds = HospitalBed.objects.filter(
        is_occupied=True
    ).count()

    if total_beds > 0:
        available_percentage = round((available_beds / total_beds) * 100)
        occupied_percentage = round((occupied_beds / total_beds) * 100)
    else:
       available_percentage = 0
       occupied_percentage = 0

    return render(
        request,
        'hospital/dashboard.html',
        {
            'total_patients': total_patients,
            'recent_patients': recent_patients,
            'predicted_patients': predicted_patients,
            'total_beds': total_beds,
            'available_beds': available_beds,
            'occupied_beds': occupied_beds,
            'available_percentage': available_percentage,
            'occupied_percentage': occupied_percentage,
        }
    )

def bed_management(request):
    if request.method == 'POST':
        bed_number = request.POST.get('bed_number', '').strip()
        ward_name = request.POST.get('ward_name', '').strip()

        if not bed_number or not ward_name:
            messages.error(request, 'Please fill in all fields.')
        elif HospitalBed.objects.filter(bed_number=bed_number).exists():
            messages.error(request, 'This bed number already exists.')
        else:
            HospitalBed.objects.create(
                bed_number=bed_number,
                ward_name=ward_name,
                is_occupied=False
            )
            messages.success(request, 'New bed added successfully!')
            return redirect('bed_management')

    beds = HospitalBed.objects.all().order_by('bed_number')

    return render(
        request,
        'hospital/bed_management.html',
        {'beds': beds}
    )

def toggle_bed_status(request, bed_id):
    if request.method == 'POST':
        bed = HospitalBed.objects.get(id=bed_id)
        bed.is_occupied = not bed.is_occupied
        bed.save()

    return redirect('bed_management')

def discharge_patient(request, patient_id):
    if request.method == 'POST':
        patient = get_object_or_404(Patient, id=patient_id)

        if not patient.is_discharged:
            patient.is_discharged = True
            patient.save()

            if patient.bed:
                patient.bed.is_occupied = False
                patient.bed.save()

            messages.success(request, 'Patient discharged successfully!')
        else:
            messages.info(request, 'Patient is already discharged.')

    return redirect('patient_records')

def delete_bed(request, bed_id):
    if request.method == 'POST':
        bed = get_object_or_404(HospitalBed, id=bed_id)

        if bed.is_occupied:
            messages.error(
                request,
                'Occupied beds cannot be deleted. Mark the bed Available first.'
            )
        else:
            bed.delete()
            messages.success(request, 'Bed deleted successfully!')

    return redirect('bed_management')

def edit_patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)

    if request.method == 'POST':
        try:
            patient.patient_name = request.POST.get('name')
            patient.email = request.POST.get('email')
            patient.age = request.POST.get('age')
            patient.gender = request.POST.get('gender')
            patient.phone = request.POST.get('phone')
            patient.address = request.POST.get('address')
            patient.symptoms = request.POST.get('symptoms', '')

            patient.save()

            messages.success(
                request,
                'Patient details updated successfully!'
            )
            return redirect('patient_records')

        except Exception:
            messages.error(
                request,
                'Update failed. Please check the details.'
            )

    return render(
        request,
        'hospital/edit_patient.html',
        {'patient': patient}
    )

def delete_patient(request, patient_id):
    if request.method == 'POST':
        patient = get_object_or_404(Patient, id=patient_id)

        if patient.bed:
            patient.bed.is_occupied = False
            patient.bed.save()

        patient.delete()

        messages.success(
            request,
            'Patient record deleted successfully!'
        )

    return redirect('patient_records')