from django import forms
from django.core.validators import RegexValidator


from django import forms
from django.core.validators import RegexValidator

class InputForm(forms.Form):
    age = forms.IntegerField(min_value=1, max_value=115, label="Your Age:")

    sex = forms.ChoiceField(choices=(
        (1, 'Male'),
        (0, 'Female')
    ))

    chest_pain = forms.ChoiceField(choices=(
        ('1', 'Typical Angina'),
        ('2', 'Atypical Angina'),
        ('3', 'Non-Anginal Pain'),
        ('4', 'Asymptomatic')
    ))

    blood_pressure = forms.CharField(
        label='Enter Blood Pressure',
        validators=[
            RegexValidator(
                regex=r'^[0-9]+/[0-9]+$',
                message="Enter blood pressure in the format of 'systolic/diastolic'."
            )
        ]
    )

    average_blood_pressure = None

    def clean(self):
        cleaned_data = super().clean()
        blood_pressure = cleaned_data.get('blood_pressure')

        if blood_pressure:
            systolic, diastolic = blood_pressure.split('/')
            systolic = int(systolic.strip())
            diastolic = int(diastolic.strip())
            self.average_blood_pressure = (systolic + diastolic) / 2  # Save average as class variable

        return cleaned_data

    chol = forms.CharField(
        label="Enter Cholestoral levels in mg/dl",
        validators=[
            RegexValidator(
                regex=r'^[0-9]{2,3}$',
                message="Enter Cholestorl 2 or 3 digits only i.e.(123)"
            )]
    )

    rest_ecg = forms.ChoiceField(label="Electrocardiographic Results", choices=(
        (0, 'Normal'),
        (1, 'ST-T wave abnormality'),
        (2, 'Left Ventricular Hupertrophy'),    
    )
    )

    highest_heart_rate = forms.IntegerField(label="Enter Highest Heart Rate Achived",
                                            min_value=0, max_value=220)
    
    exang = forms.ChoiceField(label="Exercise Induced Angina",
                            choices=(
                                (0, 'No'),
                                (1, 'Yes')
                            ),
                            widget=forms.RadioSelect
                              )
    
    oldpeak = forms.FloatField(label="Enter Oldpeak", min_value=0, max_value=10)

    slp = forms.ChoiceField(label='SLP', choices=(
        (0, 'False'),
        (1, 'True')
    ))

    ca = forms.IntegerField(max_value=3, min_value=0, label="Enter Number of Major Blood Vessels")

    thall = forms.IntegerField(min_value=1, max_value=3, label="Enter THALL value 1-3")