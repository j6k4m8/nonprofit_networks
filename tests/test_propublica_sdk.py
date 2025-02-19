# test_propublica_sdk.py

import pytest
from nonprofit_networks.propublica_sdk import ProPublicaClient, SearchResponse


def test_search():
    client = ProPublicaClient()
    response = client.search(query="propublica")
    assert isinstance(response, SearchResponse)
    assert response.total_results > 0
    assert len(response.organizations) > 0


def test_search_with_cache(tmp_path):
    cache_dir = tmp_path / "cache"
    client = ProPublicaClient(cache_directory=str(cache_dir))
    response = client.search(query="propublica")
    assert isinstance(response, SearchResponse)
    assert response.total_results > 0
    assert len(response.organizations) > 0

    # Check if cache file is created
    cache_files = list(cache_dir.iterdir())
    assert len(cache_files) > 0
    # Perform the search again to ensure it uses the cache
    response_cached = client.search(query="propublica")
    assert isinstance(response_cached, SearchResponse)
    assert response_cached.total_results == response.total_results
    assert len(response_cached.organizations) == len(response.organizations)


def test_get_full_filing(tmp_path):
    cache_dir = tmp_path / "cache"
    client = ProPublicaClient(cache_directory=str(cache_dir))

    # Test with ProPublica's EIN for a recent year
    filing_data = client.get_full_filing("142007220", year=2022)
    assert filing_data is not None
    # Basic structure checks for 990 data
    assert isinstance(filing_data, dict)
    assert "Return" in filing_data or "Return2" in filing_data


def test_get_full_filing_with_yyyy_mm(tmp_path):
    cache_dir = tmp_path / "cache"
    client = ProPublicaClient(cache_directory=str(cache_dir))

    # Test with year and month combinations
    test_cases = [
        ("142007220", "2022", None),  # String year only
        ("142007220", 2022, 12),  # Int year and month
        ("142007220", "2022", "12"),  # String year and month
    ]

    for ein, year, month in test_cases:
        filing = client.get_full_filing(ein, year=year, month=month)
        assert filing is not None

    # Test with invalid month
    filing_invalid = client.get_full_filing("142007220", year=2022, month=13)
    assert filing_invalid is None


def test_selective_index_download(tmp_path):
    cache_dir = tmp_path / "cache"
    client = ProPublicaClient(cache_directory=str(cache_dir))

    # Download only 2022 index
    client.download_irs_indices([2022])

    # Check that only 2022 was downloaded
    index_dir = cache_dir / "irs_indices"
    index_files = list(index_dir.glob("*.csv"))
    assert len(index_files) == 1
    assert "index_2022.csv" in str(index_files[0])
