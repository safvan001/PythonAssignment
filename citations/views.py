from django.shortcuts import render
import requests


API_URL = "https://devapi.beyondchats.com/api/get_message_with_sources"

def fetch_data(api_url):
    data = []
    page = 1

    while True:
        response = requests.get(f"{api_url}?page={page}")
        if response.status_code != 200:
            print("Failed to fetch data:", response.status_code)
            break
        page_data = response.json().get('data', {}).get('data', [])
        if not page_data:
            break
        data.extend(page_data)
        page += 1

    return data

from difflib import SequenceMatcher


def identify_citations(data):
    results = []

    for item in data:
        response_text = item.get('response', '')
        sources = item.get('source', [])
        citations = []

        for source in sources:
            context = source.get('context', '')
            link = source.get('link', '')

            matcher = SequenceMatcher(None, response_text, context)
            match_ratio = matcher.ratio()

            if match_ratio > 0.5:
                citation = {
                    "id": source.get("id"),
                    "link": link
                }
                citations.append(citation)

        results.append({
            "response": response_text,
            "citations": citations
        })

    return results
def index(request):
    data = fetch_data(API_URL)
    results = identify_citations(data) 
    return render(request, 'base.html', {'results': results})

