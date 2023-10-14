import numpy as np

from django.shortcuts import render
from django.views.generic.edit import FormView
from django.views.generic.base import View


from .forms import InputForm

from joblib import load
# Create your views here.

class MainFormView(FormView):
    template_name = 'main/index.html'
    form_class = InputForm
    success_url = '/results'

    def form_valid(self, form):
        # Process the form data here
        clean_data = form.cleaned_data

        # Compute average blood pressure
        systolic, diastolic = clean_data['blood_pressure'].split('/')
        systolic = int(systolic.strip())
        diastolic = int(diastolic.strip())
        clean_data['average_blood_pressure'] = (systolic + diastolic) / 2

        # Store the cleaned form data in the session
        self.request.session['form_data'] = clean_data
        return super().form_valid(form)



class ResultsView(View):
    template_name = 'main/results.html'
    
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(request, **kwargs)
        self.process(context)
        return render(request, self.template_name, context)

    def get_context_data(self, request, **kwargs):
        context = {}

        # Retrieve the form data from the session
        form_data = request.session.get('form_data', {})

        context['form_data'] = form_data
        return context

    def process(self, context):
        scaler = load('/home/dude/Desktop/Python_Files/Python/heart_attack_webapp/notebooks/scaler_model.joblib')
        model = load('/home/dude/Desktop/Python_Files/Python/heart_attack_webapp/notebooks/random_forest_model.joblib')


        # Access form data from the context
        form_data = context.get('form_data')

        features = np.array([
            form_data['age'],
            form_data['sex'],
            form_data['chest_pain'],
            form_data['average_blood_pressure'],
            form_data['chol'],
            form_data['rest_ecg'],
            form_data['highest_heart_rate'],
            form_data['exang'],
            form_data['oldpeak'],
            form_data['slp'],
            form_data['ca'],
            form_data['thall']
        ])
        features = features.reshape(1, -1)

        scaled_features = scaler.transform(features)

        result = model.predict(scaled_features)

        context['result'] = result

