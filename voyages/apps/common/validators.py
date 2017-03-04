from django.core.validators import RegexValidator
import re

date_csv_field_validator = RegexValidator(
    re.compile(r"^(\d{1,2}|),(\d{1,2}|),(\d{4}|)$"),
    message='Please type a date in the format MM,DD,YYYY (individual entries may be blank)',
    code='invalid')