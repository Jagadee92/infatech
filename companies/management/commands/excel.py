import pandas as pd

from django.core.management.base import BaseCommand
from companies.models import Company


class Command(BaseCommand):
    help = "Import company data from Excel into the database"

    def handle(self, *args, **options):

        excel_file = "companies/company.xlsx"

        try:
            df = pd.read_excel(
                excel_file,
                engine="openpyxl"
            )

            # Remove completely empty rows
            df = df.dropna(how="all")

            # Replace NaN values
            df = df.fillna(0)

            imported = 0
            updated = 0

            for _, row in df.iterrows():

                ticker = str(row["ticker"]).strip()

                company, created = Company.objects.update_or_create(
                    ticker=ticker,
                    defaults={
                        "name": row["name"],
                        "industry": row["industry"],
                        "website": row.get("website", ""),
                        "bse_code": row.get("bse_code", ""),
                        "nse_code": row.get("nse_code", ""),

                        "current_price": row["current_price"],
                        "price_change": row.get("price_change", 0),
                        "high_price": row.get("high_price", 0),
                        "low_price": row.get("low_price", 0),

                        "pe_ratio": row["pe_ratio"],
                        "market_cap": row["market_cap"],
                        "book_value": row.get("book_value", 0),
                        "face_value": row.get("face_value", 0),
                        "dividend_yield": row["dividend_yield"],
                        "roce": row["roce"],
                        "roe": row.get("roe", 0),

                        "quarterly_profit": row["quarterly_profit"],
                        "profit_change": row["profit_change"],
                        "quarterly_sales": row["quarterly_sales"],
                        "sales_change": row["sales_change"],
                    },
                )

                if created:
                    imported += 1
                else:
                    updated += 1

            self.stdout.write(
                self.style.SUCCESS(
                    f"Import completed! New: {imported}, Updated: {updated}"
                )
            )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(
                    f"Import failed: {e}"
                )
            )