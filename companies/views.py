from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render

from .models import Company


def find_company(keyword):
    """Return the company that best matches what the user typed."""
    company = Company.objects.filter(
        Q(name__iexact=keyword) | Q(ticker__iexact=keyword)
    ).first()

    if company is None:
        company = Company.objects.filter(
            Q(name__icontains=keyword) | Q(ticker__icontains=keyword)
        ).first()

    return company


def peers(request):
    query = request.GET.get("company", "").strip()
    active_tab = request.GET.get("tab", "company")
    selected_company = None
    companies = Company.objects.all()
    error_message = ""

    if active_tab != "peers":
        active_tab = "company"

    if query:
        selected_company = find_company(query)

        if selected_company:
            companies = Company.objects.filter(
                industry__iexact=selected_company.industry
            )
        else:
            companies = Company.objects.none()
            error_message = f'Company "{query}" was not found.'

    context = {
        "query": query,
        "active_tab": active_tab,
        "selected_company": selected_company,
        "companies": companies,
        "error_message": error_message,
    }
    return render(request, "companies/peers.html", context)


def search_suggestions(request):
    """Send matching company names back to the search box as JSON."""
    keyword = request.GET.get("q", "").strip()
    results = []

    if keyword:
        matches = Company.objects.filter(
            Q(name__icontains=keyword) | Q(ticker__icontains=keyword)
        )[:8]
        results = [
            {
                "name": company.name,
                "ticker": company.ticker,
                "industry": company.industry,
            }
            for company in matches
        ]

    return JsonResponse({"results": results})
