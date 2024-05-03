from django.contrib.auth import get_user_model
from django.core.handlers.wsgi import WSGIRequest
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.views import View

from onboarding.forms import OnboardingForm
from onboarding.models import MainSurvey, Survey, SurveyUserStatus

User = get_user_model()


class OnboardingView(View):
    """View онбординга."""

    def _get_surveys(self, request: WSGIRequest) -> list[Survey]:
        """Отдаёт опросники для формы."""
        main_survey = MainSurvey.objects.filter(
            namespace='onboarding:index'
            ).first()
        if not main_survey:
            return
        survey_user_status = SurveyUserStatus.objects.filter(
            main_survey=main_survey.main_survey,
            user=request.user,
            ).order_by('-datetime')
        first_survey_user_status = survey_user_status.first()
        if not first_survey_user_status:
            return (main_survey.main_survey,)
        exclude_survey = (
                    first_survey_user_status.callback_surveys.
                    values_list('id', flat=True)
                    )
        completed_surveys = list(
            Survey.objects.filter(
                id__in=survey_user_status.values_list(
                                            'callback_surveys',
                                            flat=True,
                                            )
                ).exclude(id__in=exclude_survey).values_list(
                    'id', flat=True
                    )
        )
        completed_surveys.append(main_survey.main_survey.id)
        return first_survey_user_status.callback_surveys.all().exclude(
                                                id__in=completed_surveys
                                                )

    def _get_form_onboarding(self, request: WSGIRequest) -> None:
        """Отдаёт форму онбординга."""
        surveys = self._get_surveys(request)
        return OnboardingForm(surveys=surveys)

    def post(self, request: WSGIRequest) -> HttpResponse:
        """Получает опрос онбординга."""
        form: OnboardingForm = self._get_form_onboarding(request)
        form.data = request.POST
        form.is_bound = request.POST
        form.full_clean()
        if not form.is_valid():
            context = {'form': form}
            return render(request, 'onboarding/index.html', context=context)
        namespace = 'onboarding:index'
        main_survey = MainSurvey.objects.filter(namespace=namespace).first(
                                                                ).main_survey
        form.save(request.user, main_survey)
        return redirect(namespace)

    def get(self, request: WSGIRequest) -> HttpResponse:
        """Отдаёт опрос онбординга."""
        if not request.user.is_authenticated:
            return render(request, 'onboarding/index.html')
        form = self._get_form_onboarding(request)
        context = {'form': form}
        return render(request, 'onboarding/index.html', context=context)
