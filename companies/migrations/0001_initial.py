from decimal import Decimal

from django.db import migrations, models


SAMPLE_COMPANIES = [
    ("Larsen & Toubro", "LT", Decimal("4037.40"), Decimal("31.62"), Decimal("557069.17"), Decimal("0.94"), Decimal("4988.03"), Decimal("13.98"), Decimal("67941.74"), Decimal("6.69"), Decimal("14.57")),
    ("Rail Vikas", "RVNL", Decimal("230.00"), Decimal("53.35"), Decimal("47992.91"), Decimal("0.74"), Decimal("159.52"), Decimal("18.46"), Decimal("4321.23"), Decimal("10.55"), Decimal("10.80")),
    ("NBCC", "NBCC", Decimal("93.80"), Decimal("37.09"), Decimal("25379.52"), Decimal("0.58"), Decimal("158.01"), Decimal("17.18"), Decimal("2259.53"), Decimal("-5.51"), Decimal("30.95")),
    ("IRB Infra.Devel.", "IRB", Decimal("19.56"), Decimal("24.00"), Decimal("23612.48"), Decimal("0.79"), Decimal("306.27"), Decimal("51.26"), Decimal("2137.27"), Decimal("1.82"), Decimal("7.48")),
    ("Kalpataru Projects", "KPIL", Decimal("1347.70"), Decimal("20.69"), Decimal("22988.80"), Decimal("0.82"), Decimal("311.53"), Decimal("45.15"), Decimal("6407.97"), Decimal("3.84"), Decimal("18.28")),
    ("Cemindia Projects", "CEMPRO", Decimal("1274.60"), Decimal("36.35"), Decimal("21868.42"), Decimal("0.24"), Decimal("140.83"), Decimal("2.62"), Decimal("2720.92"), Decimal("5.61"), Decimal("32.76")),
    ("Central Mine Planning", "CMPDI", Decimal("250.09"), Decimal("27.83"), Decimal("17898.48"), Decimal("0.42"), Decimal("116.27"), Decimal("53.88"), Decimal("481.37"), Decimal("17.62"), Decimal("38.06")),
    ("NCC", "NCC", Decimal("144.76"), Decimal("12.57"), Decimal("9082.50"), Decimal("1.52"), Decimal("228.90"), Decimal("12.63"), Decimal("5811.83"), Decimal("12.22"), Decimal("16.80")),
]


def add_sample_companies(apps, schema_editor):
    Company = apps.get_model("companies", "Company")
    for company in SAMPLE_COMPANIES:
        Company.objects.create(
            name=company[0],
            ticker=company[1],
            industry="Civil Construction",
            current_price=company[2],
            pe_ratio=company[3],
            market_cap=company[4],
            dividend_yield=company[5],
            quarterly_profit=company[6],
            profit_change=company[7],
            quarterly_sales=company[8],
            sales_change=company[9],
            roce=company[10],
        )


def remove_sample_companies(apps, schema_editor):
    Company = apps.get_model("companies", "Company")
    Company.objects.filter(ticker__in=[item[1] for item in SAMPLE_COMPANIES]).delete()


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Company",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=150)),
                ("ticker", models.CharField(max_length=30, unique=True)),
                ("industry", models.CharField(max_length=100)),
                ("current_price", models.DecimalField(decimal_places=2, max_digits=12)),
                ("pe_ratio", models.DecimalField(decimal_places=2, max_digits=10)),
                ("market_cap", models.DecimalField(decimal_places=2, max_digits=15)),
                ("dividend_yield", models.DecimalField(decimal_places=2, max_digits=8)),
                ("quarterly_profit", models.DecimalField(decimal_places=2, max_digits=15)),
                ("profit_change", models.DecimalField(decimal_places=2, max_digits=8)),
                ("quarterly_sales", models.DecimalField(decimal_places=2, max_digits=15)),
                ("sales_change", models.DecimalField(decimal_places=2, max_digits=8)),
                ("roce", models.DecimalField(decimal_places=2, max_digits=8)),
            ],
            options={"ordering": ["-market_cap"]},
        ),
        migrations.RunPython(add_sample_companies, remove_sample_companies),
    ]
