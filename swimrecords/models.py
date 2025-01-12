from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.core.validators import MinValueValidator


def validate_stroke(value):
    if not value in ['front crawl', 'butterfly', 'breast', 'back', 'freestyle']:
        raise ValidationError(f"{value} is not a valid stroke")


def validate_record_date(value):
    if value > timezone.now():
        raise ValidationError("Can't set record in the future.")


class SwimRecord(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    team_name = models.CharField(max_length=255)
    relay = models.BooleanField()
    stroke = models.CharField(max_length=255, validators=[validate_stroke])
    distance = models.IntegerField(validators=[MinValueValidator(
        50, message="Ensure this value is greater than or equal to 50.")])
    record_date = models.DateTimeField(
        default=timezone.now(), validators=[validate_record_date])
    record_broken_date = models.DateTimeField(null=True)

    # need to override the clean methd for the last test case b/c we need to reference other fields besides record_broken_date
    def clean(self):
        super().clean()
        if (self.record_broken_date is not None) and (self.record_broken_date < self.record_date):
            raise ValidationError(
                {'record_broken_date': "Can't break record before record was set."})
