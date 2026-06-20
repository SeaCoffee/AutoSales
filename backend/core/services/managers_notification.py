from django.contrib.auth import get_user_model

from core.services.email_service import EmailService


class ManagerNotificationService:
    @staticmethod
    def get_managers():
        UserModel = get_user_model()

        return UserModel.objects.filter(
            is_staff=True,
            role__name='manager',
            is_active=True,
        )

    @classmethod
    def send_notification(cls, brand_name, model_name, username):
        managers = cls.get_managers()

        if not managers.exists():
            return 0

        context = {
            'brand_name': brand_name,
            'model_name': model_name,
            'username': username,
        }

        sent_count = 0

        for manager in managers:
            EmailService.send_email(
                to=manager.email,
                template_name='manager_notification_email.html',
                context=context,
                subject='Brand or model review request',
            )
            sent_count += 1

        return sent_count

    @staticmethod
    def send_profanity_notification(description, username, manager):
        context = {
            'description': description,
            'username': username,
        }

        EmailService.send_email(
            to=manager.email,
            template_name='profanity_notification_email.html',
            context=context,
            subject='Profanity alert: review listing',
        )