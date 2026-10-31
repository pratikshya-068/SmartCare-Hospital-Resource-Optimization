from datetime import timedelta

import pandas as pd
from sklearn.linear_model import LinearRegression
from django.utils import timezone

from .models import Patient


def predict_patient_flow():
    today = timezone.localdate()
    start_date = today - timedelta(days=30)

    patients = Patient.objects.filter(
        created_at__date__gte=start_date,
        created_at__date__lte=today
    )

    daily_counts = []

    for i in range(31):
        day = start_date + timedelta(days=i)
        count = patients.filter(created_at__date=day).count()
        daily_counts.append(count)

    # Use recent daily average when patient data is limited
    if sum(daily_counts) < 5:
       return max(1, round(sum(daily_counts) / 10))
    df = pd.DataFrame({
        'day': list(range(1, 32)),
        'patients': daily_counts
    })

    model = LinearRegression()
    model.fit(df[['day']], df['patients'])

    next_day = pd.DataFrame({'day': [32]})
    prediction = model.predict(next_day)

    return max(0, round(prediction[0]))