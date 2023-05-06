from typing import Any, Dict, List, Tuple

from django.db import models
from django.utils import timezone

from app.common.exceptions import ApplicationError
from app.common.types import DjangoModelType


def model_update(  # type: ignore[misc] # noqa: C901,WPS210,WPS231
    *,
    instance: DjangoModelType,
    fields: List[str],
    user_data: Dict[str, Any],
    auto_updated_at=True,
) -> Tuple[DjangoModelType, bool]:
    """
    Generic update service meant to be reused in local update services.

    Args:
        instance (DjangoModelType): The instance to update.
        fields (List[str]): The fields to update
        user_data (Dict[str, Any]): The user data.
        auto_updated_at (bool, optional): Whether to update the update time. Defaults to True.

    Raises:
        ApplicationError: When model field is none.

    Returns:
        Tuple[DjangoModelType, bool]: Tuple with the following elements:

        1. The instance we updated.
        2. A boolean value representing whether we performed an update or not.
    """
    has_updated = False
    m2m_data = {}
    update_fields = []

    model_fields = {
        field.name: field for field in instance._meta.get_fields()  # noqa: WPS437
    }

    for field in fields:
        # Skip if a field is not present in the actual data
        if field not in user_data:
            continue

        # If field is not an actual model field, raise an error
        model_field = model_fields.get(field)

        if model_field is None:
            raise ApplicationError(
                message=f"{field} is not part of {instance.__class__.__name__} fields.",
            )

        # If we have m2m field, handle differently
        if isinstance(model_field, models.ManyToManyField):
            m2m_data[field] = user_data[field]
            continue

        if getattr(instance, field) != user_data[field]:
            has_updated = True
            update_fields.append(field)
            setattr(instance, field, user_data[field])

    # Perform an update only if any of the fields were actually changed
    if has_updated:
        if auto_updated_at:
            # We want to take care of the `updated_at` field,
            # Only if the models has that field
            # And if no value for updated_at has been provided
            if "updated_at" in model_fields and "updated_at" not in update_fields:
                update_fields.append("updated_at")
                instance.updated_at = timezone.now()  # type: ignore[attr-defined]

        instance.full_clean()
        # Update only the fields that are meant to be updated.
        # Django docs reference:
        # https://docs.djangoproject.com/en/dev/ref/models/instances/#specifying-which-fields-to-save
        instance.save(update_fields=update_fields)

    for field_name, field_value in m2m_data.items():
        related_manager = getattr(instance, field_name)
        related_manager.set(field_value)

        # Still not sure about this.
        # What if we only update m2m relations & nothing on the model? Is this still considered as updated?
        has_updated = True

    return instance, has_updated
