import json

from django.test import TestCase
from django.urls import reverse

from .models import Company


class PeersPageTests(TestCase):
    def test_home_page_shows_the_grid_with_every_company(self):
        response = self.client.get(reverse("companies:peers"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Mar Cap Rs.Cr.")
        self.assertContains(response, "NCC Ltd")
        self.assertContains(response, "Tata Steel Ltd")
        self.assertEqual(
            response.context["companies"].count(), Company.objects.count()
        )
        self.assertNotContains(response, 'class="tabs"')

    def test_company_tab_shows_details_without_the_grid(self):
        response = self.client.get(reverse("companies:peers"), {"company": "NCC"})

        self.assertEqual(response.context["active_tab"], "company")
        self.assertContains(response, "Book Value")
        self.assertNotContains(response, "Mar Cap Rs.Cr.")

    def test_peers_tab_shows_the_grid_without_the_details(self):
        response = self.client.get(
            reverse("companies:peers"), {"company": "NCC", "tab": "peers"}
        )
        peer_tickers = [company.ticker for company in response.context["companies"]]

        self.assertEqual(response.context["active_tab"], "peers")
        self.assertContains(response, "Mar Cap Rs.Cr.")
        self.assertNotContains(response, "Book Value")
        self.assertIn("LT", peer_tickers)
        self.assertNotIn("TATASTEEL", peer_tickers)

    def test_both_tabs_are_shown_for_a_selected_company(self):
        response = self.client.get(reverse("companies:peers"), {"company": "NCC"})

        self.assertContains(response, "tab=peers")
        self.assertContains(response, ">NCC<")

    def test_search_by_partial_name_picks_a_company(self):
        response = self.client.get(reverse("companies:peers"), {"company": "tata steel"})

        self.assertEqual(response.context["selected_company"].ticker, "TATASTEEL")
        self.assertEqual(response.context["selected_company"].industry, "Iron & Steel")

    def test_grid_names_open_the_company_tab_of_that_company(self):
        listing = self.client.get(
            reverse("companies:peers"), {"company": "NCC", "tab": "peers"}
        )
        self.assertContains(listing, "?company=LT")

        clicked = self.client.get(reverse("companies:peers"), {"company": "LT"})
        self.assertEqual(clicked.context["selected_company"].name, "Larsen & Toubro")
        self.assertEqual(clicked.context["active_tab"], "company")
        self.assertContains(clicked, "Book Value")

    def test_unknown_company_displays_message(self):
        response = self.client.get(
            reverse("companies:peers"), {"company": "Unknown Company"}
        )

        self.assertContains(response, "was not found")


class SearchSuggestionsTests(TestCase):
    def test_keyword_returns_matching_company_names(self):
        response = self.client.get(
            reverse("companies:search_suggestions"), {"q": "tata"}
        )
        names = [item["name"] for item in json.loads(response.content)["results"]]

        self.assertEqual(response.status_code, 200)
        self.assertIn("Tata Steel Ltd", names)
        self.assertNotIn("NCC Ltd", names)

    def test_empty_keyword_returns_no_results(self):
        response = self.client.get(reverse("companies:search_suggestions"), {"q": ""})

        self.assertEqual(json.loads(response.content)["results"], [])

    def test_suggestions_are_limited(self):
        response = self.client.get(reverse("companies:search_suggestions"), {"q": "a"})
        results = json.loads(response.content)["results"]

        self.assertLessEqual(len(results), 8)
        self.assertGreater(Company.objects.count(), len(results))


class ShortNameTests(TestCase):
    def test_short_name_removes_the_suffix_and_extra_words(self):
        company = Company.objects.get(ticker="IRB")

        self.assertEqual(company.short_name, "IRB Infrastructure Developers")
