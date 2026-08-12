from django.db import models

class Company(models.Model):

    docname = models.CharField(max_length=150, blank=True, default="")
    docid = models.CharField(max_length=100, blank=True, default="")
    orgid = models.CharField(max_length=100, blank=True, default="")
    ticker = models.CharField(max_length=200, blank=True, default="", db_index=True)
    fyedate = models.CharField(max_length=50, blank=True, default="")
    tablename = models.CharField(max_length=150, blank=True, default="")
    pageno = models.CharField(max_length=50, blank=True, default="")
    lastitem = models.CharField(max_length=50, blank=True, default="")
    currency = models.CharField(max_length=20, blank=True, default="")
    enddate = models.CharField(max_length=50, blank=True, default="")
    sno = models.CharField(max_length=50, blank=True, default="")
    noteno = models.CharField(max_length=50, blank=True, default="")
    particulars = models.TextField(blank=True, default="")
    amount = models.DecimalField(max_digits=30, decimal_places=2, default=0)

    class Meta:
        ordering = ["ticker"]
        verbose_name = "Company"
        verbose_name_plural = "Companies"

    def __str__(self):
        return self.ticker