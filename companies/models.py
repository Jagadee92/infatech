from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=150)
    ticker = models.CharField(max_length=30, unique=True)
    industry = models.CharField(max_length=100)
    website = models.CharField(max_length=200, blank=True, default="")
    bse_code = models.CharField(max_length=20, blank=True, default="")
    nse_code = models.CharField(max_length=20, blank=True, default="")

    current_price = models.DecimalField(max_digits=12, decimal_places=2)
    price_change = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    high_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    low_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    pe_ratio = models.DecimalField(max_digits=10, decimal_places=2)
    market_cap = models.DecimalField(max_digits=15, decimal_places=2)
    book_value = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    face_value = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    dividend_yield = models.DecimalField(max_digits=8, decimal_places=2)
    roce = models.DecimalField(max_digits=8, decimal_places=2)
    roe = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    quarterly_profit = models.DecimalField(max_digits=15, decimal_places=2)
    profit_change = models.DecimalField(max_digits=8, decimal_places=2)
    quarterly_sales = models.DecimalField(max_digits=15, decimal_places=2)
    sales_change = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        ordering = ["-market_cap"]
        verbose_name_plural = "companies"

    def __str__(self):
        return f"{self.name} ({self.ticker})"

    @property
    def short_name(self):
        """Shorter company name used on the tab bar."""
        words = self.name.replace(" Ltd", "").replace(" (India)", "").split()
        return " ".join(words[:3])
