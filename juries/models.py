from django.db import models
from django.utils.translation import gettext_lazy as _
from core.base import BaseModel
from competition.models import Competition
from children.models import Children

class AddJury(BaseModel):
    email = models.EmailField(unique=True, blank=True, null=True, verbose_name=_("Email"))
    phone_number = models.CharField(max_length=20, unique=True, blank=True, null=True, verbose_name=_("Phone"))
    image = models.ImageField(blank=True, null=True, verbose_name=_("user_Image"))
    first_name = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("First Name"))
    last_name = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Last Name"))
    father_name = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Father Name"))
    birth_date = models.DateField(blank=True, null=True, verbose_name=_("Birth Date"))
    work_place = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Work place"))
    academic_degree = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Academic Degree"))
    profession = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Profession"))
    login = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Login"))
    password = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Password"))

    class Meta:
        verbose_name = _("Jury")
        verbose_name_plural = _("Juries")

    def __str__(self):
        full_name = f"{self.first_name or ''} {self.last_name or ''}".strip()
        return full_name if full_name else "Jury"




class JuryGrade(BaseModel):
    """Оценка жюри для ребёнка в рамках конкурса"""
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, related_name="jury_grades", verbose_name=_("Competition"))
    child = models.ForeignKey(Children, on_delete=models.CASCADE, related_name="jury_grades", verbose_name=_("Child"))
    jury = models.ForeignKey(AddJury, on_delete=models.CASCADE, related_name="grades", verbose_name=_("Jury"))
    score = models.PositiveSmallIntegerField(verbose_name=_("Score"))
    comment = models.TextField(blank=True, null=True, verbose_name=_("Comment"))

    class Meta:
        unique_together = ("competition", "child", "jury")
        verbose_name = _("jury grade")
        verbose_name_plural = _("jury grades")

    def __str__(self):
        return f"{self.jury.login} → {self.child.first_name} ({self.competition.title}): {self.score}"
