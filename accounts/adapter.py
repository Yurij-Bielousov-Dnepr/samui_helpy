from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from .models import Visitor


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form=form)
        data = sociallogin.account.extra_data

        # Создаем модель Visitor на основе данных социальной сети
        visitor, created = Visitor.objects.get_or_create(
            userNick=data.get("username", ""),
            category="Customer",  # По умолчанию
            is_sponsor=False,  # По умолчанию
            phone_number=data.get("phone", ""),
            email=data.get("email", ""),
        )

        # Добавляем в модель Visitor социальную сеть
        social_network = sociallogin.account.provider
        visitor.social_networks.add(social_network)

        return user
