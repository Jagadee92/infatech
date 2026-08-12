from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render

from .models import Company


def find_company(keyword):
    """
    Find the best matching company/record.
    Exact match is checked first.
    """

    company = Company.objects.filter(
        Q(ticker__iexact=keyword)
        | Q(docid__iexact=keyword)
        | Q(orgid__iexact=keyword)
        | Q(docname__iexact=keyword)
    ).order_by("id").first()

    if company is None:
        company = Company.objects.filter(
            Q(ticker__icontains=keyword)
            | Q(docid__icontains=keyword)
            | Q(orgid__icontains=keyword)
            | Q(docname__icontains=keyword)
        ).order_by("id").first()

    return company


def peers(request):

    query = request.GET.get("company", "").strip()
    record_id = request.GET.get("record", "").strip()

    active_tab = request.GET.get("tab", "company")
    page_number = request.GET.get("page", 1)

    selected_company = None
    error_message = ""

    # Only allow these two tabs
    if active_tab not in ["company", "peers"]:
        active_tab = "company"

    # --------------------------------------------------
    # DEFAULT: SHOW ALL RECORDS
    # --------------------------------------------------

    companies = Company.objects.all().order_by("id")

    # --------------------------------------------------
    # CASE 1: OPEN EXACT DATABASE RECORD
    # --------------------------------------------------

    if record_id:

        try:
            selected_company = Company.objects.get(id=record_id)

        except (Company.DoesNotExist, ValueError):
            companies = Company.objects.none()
            error_message = f'Record "{record_id}" was not found.'

        else:

            # COMPANY TAB
            # Show ONLY the clicked record
            if active_tab == "company":

                companies = Company.objects.filter(
                    id=selected_company.id
                )

            # ALL DATA TAB
            # Show all records with same ticker
            else:

                companies = Company.objects.filter(
                    ticker__iexact=selected_company.ticker
                ).order_by("id")

    # --------------------------------------------------
    # CASE 2: SEARCH BAR
    # --------------------------------------------------

    elif query:

        selected_company = find_company(query)

        if selected_company:

            # Search result / Company tab
            if active_tab == "company":

                companies = Company.objects.filter(
                    id=selected_company.id
                )

            # All Data tab
            else:

                companies = Company.objects.filter(
                    ticker__iexact=selected_company.ticker
                ).order_by("id")

        else:

            companies = Company.objects.none()

            error_message = (
                f'Company "{query}" was not found.'
            )

    # --------------------------------------------------
    # PAGINATION
    # --------------------------------------------------

    paginator = Paginator(companies, 10)

    page_obj = paginator.get_page(page_number)

    # --------------------------------------------------
    # CONTEXT
    # --------------------------------------------------

    context = {
        "query": query,
        "record_id": record_id,
        "active_tab": active_tab,
        "selected_company": selected_company,
        "companies": page_obj,
        "page_obj": page_obj,
        "error_message": error_message,
    }

    return render(
        request,
        "companies/peers.html",
        context
    )


# ======================================================
# SEARCH SUGGESTIONS
# ======================================================

def search_suggestions(request):

    keyword = request.GET.get("q", "").strip()

    results = []

    if keyword:

        matches = Company.objects.filter(
            Q(ticker__icontains=keyword)
            | Q(docid__icontains=keyword)
            | Q(orgid__icontains=keyword)
            | Q(docname__icontains=keyword)
        ).order_by("id")[:10]

        for company in matches:

            results.append({
                "id": company.id,
                "name": company.docname or "",
                "ticker": company.ticker or "",
                "docid": company.docid or "",
                "orgid": company.orgid or "",
            })

    return JsonResponse({
        "results": results
    })