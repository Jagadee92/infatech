import json
from django.test import TestCase
from django.urls import reverse
from .models import Company

class PeersPageTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.company = Company.objects.create(
            docname="WIPRO Financial Report",
            docid="DOC001",
            orgid="ORG001",
            ticker="WIPRO.NS",
            fyedate="2025",
            tablename="Balance Sheet",
            pageno="1",
            lastitem="100",
            currency="INR",
            enddate="2025-03-31",
            sno="1",
            noteno="10",
            particulars="Total Assets",
            amount=125000.50,
        )

    def test_home_page_shows_the_grid_with_every_company(self):
        response = self.client.get(reverse("companies:peers"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ticker")
        self.assertContains(response, "Document")
        self.assertContains(response, "Doc ID")
        self.assertContains(response, "Org ID")
        self.assertContains(response, "Particulars")
        self.assertEqual(response.context["companies"].count(), Company.objects.count())
        self.assertNotContains(response, 'class="tabs"')

    def test_company_tab_shows_details_without_the_grid(self):
        response = self.client.get(reverse("companies:peers"), {"company": self.company.ticker})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["active_tab"], "company")
        self.assertContains(response, self.company.docname)
        self.assertContains(response, self.company.docid)
        self.assertContains(response, self.company.orgid)
        self.assertContains(response, self.company.particulars)
        self.assertContains(response, str(self.company.amount))
        self.assertNotContains(response, "<th>Ticker</th>")

    def test_peers_tab_shows_the_grid_without_the_details(self):
        response = self.client.get(reverse("companies:peers"), {"company": self.company.ticker, "tab": "peers"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["active_tab"], "peers")
        self.assertContains(response, "Ticker")
        self.assertContains(response, "Document")
        self.assertContains(response, "Doc ID")
        self.assertContains(response, "Org ID")
        self.assertNotContains(response, "Financial Year End")

    def test_both_tabs_are_shown_for_a_selected_company(self):
        response = self.client.get(reverse("companies:peers"), {"company": self.company.ticker})
        self.assertContains(response, "tab=peers")
        self.assertContains(response, f">{self.company.ticker}<")

    def test_search_by_ticker_picks_a_company(self):
        response = self.client.get(reverse("companies:peers"), {"company": self.company.ticker})
        self.assertEqual(response.context["selected_company"].ticker, self.company.ticker)

    def test_search_by_docid_picks_a_company(self):
        response = self.client.get(reverse("companies:peers"), {"company": self.company.docid})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["selected_company"].docid, self.company.docid)

    def test_search_by_orgid_picks_a_company(self):
        response = self.client.get(reverse("companies:peers"), {"company": self.company.orgid})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["selected_company"].orgid, self.company.orgid)

    def test_search_by_docname_picks_a_company(self):
        response = self.client.get(reverse("companies:peers"), {"company": self.company.docname})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["selected_company"].docname, self.company.docname)

    def test_grid_names_open_the_company_tab_of_that_company(self):
        listing = self.client.get(reverse("companies:peers"), {"company": self.company.ticker, "tab": "peers"})
        self.assertContains(listing, f"?company={self.company.ticker}")
        clicked = self.client.get(reverse("companies:peers"), {"company": self.company.ticker})
        self.assertEqual(clicked.context["selected_company"].ticker, self.company.ticker)
        self.assertEqual(clicked.context["active_tab"], "company")

    def test_unknown_company_displays_message(self):
        response = self.client.get(reverse("companies:peers"), {"company": "Unknown Company"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Company "Unknown Company" was not found.')

class SearchSuggestionsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.company = Company.objects.create(
            docname="WIPRO Financial Report",
            docid="DOC001",
            orgid="ORG001",
            ticker="WIPRO.NS",
            fyedate="2025",
            tablename="Balance Sheet",
            pageno="1",
            lastitem="100",
            currency="INR",
            enddate="2025-03-31",
            sno="1",
            noteno="10",
            particulars="Total Assets",
            amount=125000.50,
        )

    def test_keyword_returns_matching_company(self):
        response = self.client.get(reverse("companies:search_suggestions"), {"q": self.company.ticker})
        self.assertEqual(response.status_code, 200)
        results = json.loads(response.content)["results"]
        tickers = [item["ticker"] for item in results]
        self.assertIn(self.company.ticker, tickers)

    def test_search_by_docid_returns_company(self):
        response = self.client.get(reverse("companies:search_suggestions"), {"q": self.company.docid})
        self.assertEqual(response.status_code, 200)
        results = json.loads(response.content)["results"]
        docids = [item["docid"] for item in results]
        self.assertIn(self.company.docid, docids)

    def test_search_by_orgid_returns_company(self):
        response = self.client.get(reverse("companies:search_suggestions"), {"q": self.company.orgid})
        self.assertEqual(response.status_code, 200)
        results = json.loads(response.content)["results"]
        orgids = [item["orgid"] for item in results]
        self.assertIn(self.company.orgid, orgids)

    def test_search_by_docname_returns_company(self):
        response = self.client.get(reverse("companies:search_suggestions"), {"q": self.company.docname})
        self.assertEqual(response.status_code, 200)
        results = json.loads(response.content)["results"]
        names = [item["name"] for item in results]
        self.assertIn(self.company.docname, names)

    def test_empty_keyword_returns_no_results(self):
        response = self.client.get(reverse("companies:search_suggestions"), {"q": ""})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)["results"], [])

    def test_suggestions_are_limited(self):
        response = self.client.get(reverse("companies:search_suggestions"), {"q": "WIPRO"})
        self.assertEqual(response.status_code, 200)
        results = json.loads(response.content)["results"]
        self.assertLessEqual(len(results), 8)

class CompanyFieldTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.company = Company.objects.create(
            docname="WIPRO Financial Report",
            docid="DOC001",
            orgid="ORG001",
            ticker="WIPRO.NS",
            fyedate="2025",
            tablename="Balance Sheet",
            pageno="1",
            lastitem="100",
            currency="INR",
            enddate="2025-03-31",
            sno="1",
            noteno="10",
            particulars="Total Assets",
            amount=125000.50,
        )

    def test_company_has_excel_fields(self):
        company = Company.objects.first()
        self.assertIsNotNone(company)
        self.assertIsNotNone(company.ticker)
        self.assertIsNotNone(company.docname)
        self.assertIsNotNone(company.docid)
        self.assertIsNotNone(company.orgid)
        self.assertIsNotNone(company.fyedate)
        self.assertIsNotNone(company.tablename)
        self.assertIsNotNone(company.pageno)
        self.assertIsNotNone(company.lastitem)
        self.assertIsNotNone(company.currency)
        self.assertIsNotNone(company.enddate)
        self.assertIsNotNone(company.sno)
        self.assertIsNotNone(company.noteno)
        self.assertIsNotNone(company.particulars)
        self.assertIsNotNone(company.amount)