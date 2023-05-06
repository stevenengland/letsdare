from typing import Optional

from django.db import transaction

from app.common.services.model_update_service import model_update
from app.users.models import BaseUser


def user_create(
    *,
    email: str,
    is_active: bool = True,
    is_admin: bool = False,
    password: Optional[str] = None,
) -> BaseUser:
    """Create a new user."""
    user = BaseUser.objects.create_user(
        email=email,
        is_active=is_active,
        is_admin=is_admin,
        password=password,
    )  # type: ignore[no-untyped-call]

    return user  # noqa: WPS331


@transaction.atomic
def user_update(*, user: BaseUser, user_data) -> BaseUser:
    """Update an existing user."""
    non_side_effect_fields = ["first_name", "last_name"]

    user, has_updated = model_update(
        instance=user,
        fields=non_side_effect_fields,
        user_data=user_data,
    )

    # Side-effect fields update here (e.g. username is generated based on first & last name)

    # ... some additional tasks with the user ...

    return user  # noqa: WPS331
