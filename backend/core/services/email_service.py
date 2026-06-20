from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template

from core.services.jwt_service import ActivateToken, JWTService, RecoveryToken


@shared_task(name='core.send_email')
def send_email_task(to: str, template_name: str, context: dict, subject: str = ''):
    template = get_template(template_name)
    html_content = template.render(context)

    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', None) or getattr(
        settings,
        'EMAIL_HOST_USER',
        None,
    )

    if not from_email:
        raise RuntimeError('DEFAULT_FROM_EMAIL or EMAIL_HOST_USER must be configured.')

    message = EmailMultiAlternatives(
        subject=subject,
        body='',
        from_email=from_email,
        to=[to],
    )
    message.attach_alternative(html_content, 'text/html')
    message.send()


class EmailService:
    @staticmethod
    def build_action_url(setting_name: str, token) -> str:
        url_template = getattr(settings, setting_name, None)

        if not url_template:
            raise RuntimeError(f'{setting_name} must be configured.')

        return url_template.format(token=str(token))

    @classmethod
    def send_email(cls, to: str, template_name: str, context: dict, subject: str = ''):
        send_email_task.delay(to, template_name, context, subject)

    @classmethod
    def register(cls, user):
        token = JWTService.create_token(user, ActivateToken)
        url = cls.build_action_url('ACCOUNT_ACTIVATION_URL_TEMPLATE', token)

        profile = getattr(user, 'profile', None)
        name = getattr(profile, 'name', '') or user.username

        cls.send_email(
            to=user.email,
            template_name='register.html',
            context={
                'name': name,
                'url': url,
            },
            subject='Account activation',
        )

    @classmethod
    def recovery_password(cls, user):
        token = JWTService.create_token(user, RecoveryToken)
        url = cls.build_action_url('PASSWORD_RECOVERY_URL_TEMPLATE', token)

        cls.send_email(
            to=user.email,
            template_name='recovery.html',
            context={
                'url': url,
            },
            subject='Password recovery',
        )

    @classmethod
    def account_deletion(cls, user):
        cls.send_email(
            to=user.email,
            template_name='delete_account.html',
            context={
                'name': user.username,
            },
            subject='Account deleted',
        )