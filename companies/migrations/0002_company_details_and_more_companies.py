from decimal import Decimal

from django.db import migrations, models


COMPANY_COLUMNS = [
    "name",
    "industry",
    "website",
    "bse_code",
    "nse_code",
    "current_price",
    "price_change",
    "high_price",
    "low_price",
    "pe_ratio",
    "market_cap",
    "book_value",
    "face_value",
    "dividend_yield",
    "roce",
    "roe",
    "quarterly_profit",
    "profit_change",
    "quarterly_sales",
    "sales_change",
]

COMPANY_ROWS = {
    "LT": ("Larsen & Toubro", "Civil Construction", "larsentoubro.com", "500510", "LT", "4037.40", "0.85", "4592.00", "3200.00", "31.62", "557069.17", "700.50", "2.00", "0.94", "14.57", "15.20", "4988.03", "13.98", "67941.74", "6.69"),
    "RVNL": ("Rail Vikas Nigam Ltd", "Civil Construction", "rvnl.org", "542649", "RVNL", "230.00", "-1.20", "647.00", "213.00", "53.35", "47992.91", "32.40", "10.00", "0.74", "10.80", "17.10", "159.52", "18.46", "4321.23", "10.55"),
    "NBCC": ("NBCC (India) Ltd", "Civil Construction", "nbccindia.in", "534309", "NBCC", "93.80", "0.42", "139.00", "70.00", "37.09", "25379.52", "11.20", "1.00", "0.58", "30.95", "22.30", "158.01", "17.18", "2259.53", "-5.51"),
    "IRB": ("IRB Infrastructure Developers Ltd", "Civil Construction", "irb.co.in", "532947", "IRB", "19.56", "-0.61", "34.00", "17.00", "24.00", "23612.48", "30.80", "1.00", "0.79", "7.48", "5.10", "306.27", "51.26", "2137.27", "1.82"),
    "KPIL": ("Kalpataru Projects International Ltd", "Civil Construction", "kalpataruprojects.com", "522287", "KPIL", "1347.70", "1.14", "1449.00", "900.00", "20.69", "22988.80", "405.20", "2.00", "0.82", "18.28", "12.60", "311.53", "45.15", "6407.97", "3.84"),
    "CEMPRO": ("Cemindia Projects Ltd", "Civil Construction", "cemindia.com", "544356", "CEMPRO", "1274.60", "-0.35", "1450.00", "700.00", "36.35", "21868.42", "210.50", "10.00", "0.24", "32.76", "24.80", "140.83", "2.62", "2720.92", "5.61"),
    "CMPDI": ("Central Mine Planning & Design Institute Ltd", "Civil Construction", "cmpdi.co.in", "544401", "CMPDI", "250.09", "2.05", "300.00", "180.00", "27.83", "17898.48", "55.30", "10.00", "0.42", "38.06", "27.40", "116.27", "53.88", "481.37", "17.62"),
    "NCC": ("NCC Ltd", "Civil Construction", "ncclimited.com", "500294", "NCC", "144.76", "-1.15", "225.00", "130.00", "12.57", "9082.50", "125.00", "2.00", "1.52", "16.80", "9.19", "228.90", "12.63", "5811.83", "12.22"),

    "TATASTEEL": ("Tata Steel Ltd", "Iron & Steel", "tatasteel.com", "500470", "TATASTEEL", "188.00", "-1.05", "224.00", "153.00", "19.90", "235237.00", "81.80", "1.00", "2.12", "12.50", "11.70", "3618.00", "25.40", "56000.00", "4.30"),
    "JSWSTEEL": ("JSW Steel Ltd", "Iron & Steel", "jsw.in", "500228", "JSWSTEEL", "1045.00", "0.62", "1180.00", "850.00", "45.20", "255600.00", "320.10", "1.00", "0.35", "11.20", "9.40", "1500.00", "30.10", "44000.00", "5.20"),
    "SAIL": ("Steel Authority of India Ltd", "Iron & Steel", "sail.co.in", "500113", "SAIL", "128.00", "-0.78", "150.00", "99.00", "24.60", "52900.00", "137.40", "10.00", "1.20", "7.90", "5.60", "500.00", "15.60", "27000.00", "3.10"),
    "JINDALSTEL": ("Jindal Steel & Power Ltd", "Iron & Steel", "jindalsteelpower.com", "532286", "JINDALSTEL", "985.00", "1.32", "1097.00", "723.00", "28.40", "100400.00", "380.60", "1.00", "0.20", "13.10", "10.80", "1200.00", "18.20", "13500.00", "6.80"),

    "TCS": ("Tata Consultancy Services Ltd", "IT - Software", "tcs.com", "532540", "TCS", "3150.00", "-0.45", "4592.00", "3056.00", "24.80", "1139000.00", "260.40", "1.00", "1.85", "64.30", "51.20", "12400.00", "6.40", "64500.00", "5.10"),
    "INFY": ("Infosys Ltd", "IT - Software", "infosys.com", "500209", "INFY", "1520.00", "0.28", "2006.00", "1307.00", "24.10", "631000.00", "220.30", "5.00", "2.90", "39.80", "31.80", "6800.00", "11.30", "42000.00", "7.60"),
    "HCLTECH": ("HCL Technologies Ltd", "IT - Software", "hcltech.com", "532281", "HCLTECH", "1580.00", "0.51", "2011.00", "1303.00", "25.30", "428000.00", "200.80", "2.00", "3.55", "32.60", "25.10", "4600.00", "8.10", "30500.00", "6.30"),
    "WIPRO": ("Wipro Ltd", "IT - Software", "wipro.com", "507685", "WIPRO", "245.00", "-0.92", "324.00", "228.00", "19.60", "256000.00", "88.70", "2.00", "2.45", "21.40", "16.90", "3300.00", "9.80", "22300.00", "2.10"),
    "TATAELXSI": ("Tata Elxsi Ltd", "IT - Software", "tataelxsi.com", "500408", "TATAELXSI", "5100.00", "-1.85", "8000.00", "4700.00", "40.20", "31700.00", "355.20", "10.00", "1.35", "33.80", "25.60", "145.00", "-12.40", "900.00", "-2.10"),
    "TATATECH": ("Tata Technologies Ltd", "IT - Software", "tatatechnologies.com", "544028", "TATATECH", "660.00", "0.74", "1044.00", "595.00", "45.60", "26800.00", "90.60", "2.00", "1.90", "25.40", "19.30", "155.00", "-4.20", "1300.00", "1.50"),

    "TATAPOWER": ("Tata Power Company Ltd", "Power Generation", "tatapower.com", "500400", "TATAPOWER", "385.00", "1.05", "494.00", "326.00", "32.40", "123000.00", "105.40", "1.00", "0.52", "12.80", "11.60", "1200.00", "15.30", "15800.00", "8.20"),
    "NTPC": ("NTPC Ltd", "Power Generation", "ntpc.co.in", "532555", "NTPC", "335.00", "-0.34", "448.00", "292.00", "15.80", "324800.00", "165.20", "10.00", "2.40", "10.60", "13.50", "5000.00", "12.10", "45000.00", "4.60"),
    "ADANIPOWER": ("Adani Power Ltd", "Power Generation", "adanipower.com", "533096", "ADANIPOWER", "590.00", "2.15", "896.00", "430.00", "15.20", "227600.00", "105.80", "10.00", "0.00", "25.30", "30.20", "3200.00", "-8.50", "14200.00", "9.10"),

    "TATACOMM": ("Tata Communications Ltd", "Telecom Services", "tatacommunications.com", "500483", "TATACOMM", "1650.00", "-1.42", "2175.00", "1355.00", "60.50", "47000.00", "40.20", "10.00", "1.30", "18.60", "45.30", "210.00", "-15.20", "5900.00", "6.10"),
    "BHARTIARTL": ("Bharti Airtel Ltd", "Telecom Services", "airtel.in", "532454", "BHARTIARTL", "1890.00", "0.88", "2045.00", "1250.00", "42.60", "1130000.00", "155.60", "5.00", "0.42", "15.20", "20.10", "5500.00", "120.40", "45100.00", "15.30"),

    "TATACONSUM": ("Tata Consumer Products Ltd", "Packaged Foods", "tataconsumer.com", "500800", "TATACONSUM", "1085.00", "-0.56", "1254.00", "882.00", "78.40", "107300.00", "195.30", "1.00", "0.80", "8.60", "7.20", "290.00", "18.60", "4500.00", "12.40"),
    "NESTLEIND": ("Nestle India Ltd", "Packaged Foods", "nestle.in", "500790", "NESTLEIND", "2280.00", "0.33", "2778.00", "2110.00", "68.20", "219800.00", "30.20", "1.00", "1.20", "105.40", "88.60", "700.00", "-5.20", "5100.00", "4.10"),
    "BRITANNIA": ("Britannia Industries Ltd", "Packaged Foods", "britannia.com", "500825", "BRITANNIA", "5600.00", "0.47", "6470.00", "4506.00", "60.10", "134900.00", "145.80", "1.00", "1.40", "48.20", "55.60", "580.00", "8.20", "4600.00", "6.30"),

    "TATAINVEST": ("Tata Investment Corporation Ltd", "Investment Company", "tatainvestment.com", "501301", "TATAINVEST", "6800.00", "-1.15", "8074.00", "5300.00", "95.20", "34400.00", "900.50", "10.00", "0.40", "4.20", "3.80", "90.00", "12.30", "100.00", "15.20"),
    "TATACAPITAL": ("Tata Capital Ltd", "Investment Company", "tatacapital.com", "544483", "TATACAPITAL", "320.00", "0.95", "375.00", "290.00", "55.60", "136000.00", "65.40", "10.00", "0.15", "9.80", "12.20", "1000.00", "10.50", "7200.00", "22.40"),
    "BAJAJHLDNG": ("Bajaj Holdings & Investment Ltd", "Investment Company", "bhil.in", "500490", "BAJAJHLDNG", "12800.00", "0.22", "14000.00", "9500.00", "15.40", "142400.00", "4200.30", "10.00", "1.10", "3.60", "12.80", "1800.00", "9.60", "200.00", "8.10"),

    "TATAMOTORS": ("Tata Motors Ltd", "Automobiles", "tatamotors.com", "500570", "TATAMOTORS", "680.00", "-1.65", "1179.00", "535.00", "10.20", "250400.00", "280.50", "2.00", "0.90", "18.60", "22.40", "5500.00", "-12.30", "105000.00", "2.10"),
    "MARUTI": ("Maruti Suzuki India Ltd", "Automobiles", "marutisuzuki.com", "532500", "MARUTI", "12500.00", "0.65", "13680.00", "10725.00", "28.40", "393000.00", "3100.20", "5.00", "1.00", "17.20", "16.80", "3700.00", "8.40", "38000.00", "6.20"),
    "M&M": ("Mahindra & Mahindra Ltd", "Automobiles", "mahindra.com", "500520", "M&M", "3150.00", "1.42", "3270.00", "2350.00", "32.10", "391800.00", "780.40", "5.00", "0.70", "15.80", "18.20", "3100.00", "15.60", "30000.00", "14.30"),
}


def load_companies(apps, schema_editor):
    Company = apps.get_model("companies", "Company")

    for ticker, values in COMPANY_ROWS.items():
        details = {}
        for column, value in zip(COMPANY_COLUMNS, values):
            if column in ("name", "industry", "website", "bse_code", "nse_code"):
                details[column] = value
            else:
                details[column] = Decimal(value)

        Company.objects.update_or_create(ticker=ticker, defaults=details)


class Migration(migrations.Migration):
    dependencies = [
        ("companies", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="company",
            options={"ordering": ["-market_cap"], "verbose_name_plural": "companies"},
        ),
        migrations.AddField(
            model_name="company",
            name="website",
            field=models.CharField(blank=True, default="", max_length=200),
        ),
        migrations.AddField(
            model_name="company",
            name="bse_code",
            field=models.CharField(blank=True, default="", max_length=20),
        ),
        migrations.AddField(
            model_name="company",
            name="nse_code",
            field=models.CharField(blank=True, default="", max_length=20),
        ),
        migrations.AddField(
            model_name="company",
            name="price_change",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8),
        ),
        migrations.AddField(
            model_name="company",
            name="high_price",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
        migrations.AddField(
            model_name="company",
            name="low_price",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
        migrations.AddField(
            model_name="company",
            name="book_value",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
        migrations.AddField(
            model_name="company",
            name="face_value",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8),
        ),
        migrations.AddField(
            model_name="company",
            name="roe",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8),
        ),
        migrations.RunPython(load_companies, migrations.RunPython.noop),
    ]
