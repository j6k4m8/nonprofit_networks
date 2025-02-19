# propublica_sdk.py

import os
import json
import time
import httpx
import zipfile
import pandas as pd
from io import BytesIO
from pathlib import Path
from datetime import datetime
import xml.etree.ElementTree
from typing import Optional, Dict, Any, List, Union
from pydantic import BaseModel, Field
import xmltodict
from .response_types import FullFiling

_DEFAULT_CONFIG_PATH = os.path.expanduser(
    "~/.propublica_sdk_files/nonprofit-explorer/cache"
)


class Organization(BaseModel):
    ein: int
    name: str
    city: str
    state: str
    ntee_code: Optional[str] = None
    score: Optional[float] = None


class Filing(BaseModel):
    tax_prd_yr: int
    tax_prd: int
    pdf_url: Optional[str] = None
    formtype: int
    updated: str


class SearchResponse(BaseModel):
    total_results: int
    organizations: list[Organization]
    num_pages: int
    cur_page: int
    per_page: int
    search_query: Optional[str] = None


class ProPublicaClient:
    BASE_URL = "https://projects.propublica.org/nonprofits/api/v2"
    IRS_BASE_URL = "https://apps.irs.gov/pub/epostcard/990/xml"

    def __init__(
        self,
        cache_directory: Optional[str] = None,
        download_xml_indices: bool = False,
        debug: bool = False,
    ):
        """
        Initializes the ProPublica SDK instance.

        Arguments:
            cache_directory (Optional[str]): The directory path where cache files will be stored.
                                          If not provided, defaults to ~/.propublica_sdk_files/nonprofit-explorer/cache.
                                          The directory will be created if it does not exist.
            download_xml_indices (bool): Whether to download IRS XML indices during initialization.
                                      If False, indices can be downloaded later using download_irs_indices().
            debug (bool): Whether to enable debug mode for the SDK.
        """
        self.cache_directory = cache_directory or _DEFAULT_CONFIG_PATH
        os.makedirs(self.cache_directory, exist_ok=True)
        self._index_cache = {}  # Cache for loaded indices
        if download_xml_indices:
            self.download_irs_indices()
        self.debug = debug

    def _debug(self, *args, **kwargs):
        if self.debug:
            print(*args, **kwargs)

    def download_irs_indices(self, years: Optional[List[int]] = None) -> None:
        """
        Downloads IRS index files if they don't exist in the cache.

        Args:
            years: Optional list of years to download. If None, checks from current year back to 2019.
        """
        if years is None:
            current_year = datetime.now().year
            years = range(2019, current_year + 1)

        index_dir = os.path.join(self.cache_directory, "irs_indices")
        os.makedirs(index_dir, exist_ok=True)

        for year in years:
            index_file = os.path.join(index_dir, f"index_{year}.csv")
            if not os.path.exists(index_file):
                try:
                    url = f"{self.IRS_BASE_URL}/{year}/index_{year}.csv"
                    self._debug(f"Downloading IRS index for {year} at {url}")
                    response = httpx.get(url)
                    if response.status_code == 200:
                        with open(index_file, "wb") as f:
                            f.write(response.content)
                except httpx.RequestError:
                    self._debug(f"Failed to download IRS index for {year}")
                    # Skip if the file doesn't exist (e.g., future year)
                    continue

    def _get_index_data(self, year: int) -> pd.DataFrame:
        """
        Get the index data for a specific year, loading from cache if available.
        """
        if year in self._index_cache:
            return self._index_cache[year]

        index_file = os.path.join(
            self.cache_directory, "irs_indices", f"index_{year}.csv"
        )
        if not os.path.exists(index_file):
            self._debug(f"Index file not found for {year}, downloading...")
            self.download_irs_indices([year])

        if os.path.exists(index_file):
            df = pd.read_csv(index_file)
            # Ensure consistent string types for matching
            df["EIN"] = df["EIN"].astype(str)
            df["OBJECT_ID"] = df["OBJECT_ID"].astype(str)
            df["TAX_PERIOD"] = df["TAX_PERIOD"].astype(int)
            self._index_cache[year] = df
            return df
        return pd.DataFrame()  # Return empty DataFrame if file doesn't exist

    def _normalized_ein_pattern(self, ein: str | int, hyphenate: bool = False) -> str:
        """Normalize EIN pattern to XXXXXXXXX or XX-XXXXXXX format."""
        ein = str(ein).replace("-", "")
        if hyphenate:
            return f"{ein[:2]}-{ein[2:]}"
        return ein

    def _download_xml_batch(
        self, year: int, object_id: str, batch_id: Optional[str] = None
    ) -> Optional[str]:
        """
        Downloads and extracts an XML batch file if it doesn't exist in cache.
        Will retry failed downloads and attempt to repair corrupted zip files.

        Args:
            year: The year of the filing
            object_id: The object ID of the filing
            batch_id: Optional batch ID to download a specific XML file batch

        Returns:
            Path to the extracted directory or specific XML file if object_id is provided
        """
        batch_id = batch_id.upper() if batch_id else None
        if not batch_id:
            raise ValueError("batch_id is required to download XML files for now")

        batch_dir = os.path.join(self.cache_directory, "xml_files", str(year), batch_id)
        # Check if the file already exists
        if object_id:
            extracted_file = os.path.join(batch_dir, f"{object_id}.xml")
            self._debug(f"Checking for existing XML file at {extracted_file}")
            if os.path.exists(extracted_file):
                return extracted_file
            self._debug(f"XML file not found at {extracted_file}")
            # Try also the version suffixed with _public.xml
            extracted_file = os.path.join(batch_dir, f"{object_id}_public.xml")
            if os.path.exists(extracted_file):
                return extracted_file
            self._debug(f"XML file not found at {extracted_file}")

        # See if the zip file already exists
        zip_file = os.path.join(batch_dir, f"{batch_id}.zip")
        if os.path.exists(zip_file):
            self._debug(f"Found existing ZIP file at {zip_file}")
            with zipfile.ZipFile(zip_file) as zf:
                if object_id:
                    try:
                        xml_file = next(f for f in zf.namelist() if object_id in f)
                        zf.extract(xml_file, batch_dir)
                        extracted_file = os.path.join(batch_dir, xml_file)
                        with open(extracted_file, "r", encoding="utf-8") as f:
                            xmltodict.parse(f.read())
                        return extracted_file
                    except (StopIteration, xml.etree.ElementTree.ParseError):
                        pass
                else:
                    return batch_dir

        # Use longer timeout for large zip files
        timeout = httpx.Timeout(30.0, connect=30.0, read=None)

        # Try multiple times with exponential backoff
        max_retries = 5
        for attempt in range(max_retries):
            try:
                # Calculate backoff delay: 2^attempt seconds (1, 2, 4, 8, 16)
                if attempt > 0:
                    time.sleep(min(2 ** (attempt - 1), 16))

                zip_url = f"{self.IRS_BASE_URL}/{year}/{batch_id}.zip"
                self._debug(
                    f"Downloading XML batch from {zip_url} with timeout {timeout}, attempt {attempt + 1}"
                )
                response = httpx.get(zip_url, timeout=timeout, follow_redirects=True)

                if response.status_code == 200:
                    os.makedirs(batch_dir, exist_ok=True)
                    with open(zip_file, "wb") as f:
                        f.write(response.content)

                    with zipfile.ZipFile(BytesIO(response.content)) as zf:
                        if object_id:
                            try:
                                xml_file = next(
                                    f for f in zf.namelist() if object_id in f
                                )
                                zf.extract(xml_file, batch_dir)
                                extracted_file = os.path.join(batch_dir, xml_file)
                                with open(extracted_file, "r", encoding="utf-8") as f:
                                    xmltodict.parse(f.read())
                                return extracted_file
                            except (StopIteration, xml.etree.ElementTree.ParseError):
                                continue
                        else:
                            zf.extractall(batch_dir)
                            return batch_dir
                elif response.status_code in {
                    429,
                    503,
                    502,
                }:  # Rate limit or service unavailable
                    self._debug(
                        f"Received status code {response.status_code}, retrying..."
                    )
                    continue  # Retry with backoff
                else:
                    return None  # Don't retry on other status codes

            except (
                httpx.RequestError,
                zipfile.BadZipFile,
                xml.etree.ElementTree.ParseError,
                IOError,
                httpx.TimeoutException,
            ) as e:
                self._debug(f"Failed to download XML batch: {e}")
                if attempt == max_retries - 1:
                    return None
                continue

        return None

    def get_full_filing(
        self,
        ein: str,
        year: Union[int, str],
        month: Union[int, str],
        as_json: bool = False,
    ) -> Optional[Dict]:
        """
        Get the complete filing data for an organization, including the full XML content.
        Will attempt to download data if not found in cache.

        Args:
            ein: The Employer Identification Number
            year: year (YYYY) to retrieve. Can be provided as string or integer.
            month: month (MM) to retrieve. Can be provided as string or integer.

        Returns:
            Dict containing the parsed XML data
        """
        year = int(year) if isinstance(year, str) else year
        month = int(month) if isinstance(month, str) else month

        if year < 2021:
            raise ValueError(
                "Only filings from 2021 and later are available through this API at the moment. In 2021 the IRS switched to a new batch storage system which is currently supported."
            )

        ein = self._normalized_ein_pattern(ein)
        # Get the index data for the year
        # IRS index data is listed the year after the filings
        index_data = self._get_index_data(year + 1)
        if index_data.empty:
            raise ValueError(f"No index data found for {year}")

        # Filter by EIN, year, and month:
        filings = index_data[
            (index_data.TAX_PERIOD == int(f"{year}{month:02d}"))
            & (index_data.EIN == ein)
        ]
        if filings.empty:
            available_qtrs = index_data[(index_data.EIN == ein)]
            raise ValueError(
                f"No filings found for EIN {ein} in {year}-{month:02d}. Available quarters: {available_qtrs.TAX_PERIOD.unique()}"
            )

        # Get the first filing object ID
        object_id = filings.iloc[0]["OBJECT_ID"]
        # There may also be XML_BATCH_ID, if the column exists:
        batch_id = filings.iloc[0].get("XML_BATCH_ID")

        # Download the XML file
        extracted_file = self._download_xml_batch(year + 1, object_id, batch_id)

        if extracted_file:
            with open(extracted_file, "r", encoding="utf-8") as f:
                results = xmltodict.parse(f.read())
                if as_json:
                    return results
                return FullFiling(**results)
        raise KeyError(
            f"Failed to download XML file for EIN {ein} in {year}-{month:02d}"
        )

    def _get_cache_path(self, endpoint: str, params: Dict[str, Any]) -> str:
        filename = f"{endpoint}_{hash(frozenset(params.items()))}.json"
        return (
            os.path.join(self.cache_directory, filename)
            if self.cache_directory
            else filename
        )

    def _get(self, endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
        if self.cache_directory:
            cache_path = self._get_cache_path(endpoint, params)
            if os.path.exists(cache_path):
                with open(cache_path, "r") as f:
                    return json.load(f)

        response = httpx.get(f"{self.BASE_URL}/{endpoint}", params=params)
        response.raise_for_status()
        data = response.json()

        if self.cache_directory:
            with open(cache_path, "w") as f:
                json.dump(data, f)

        return data

    def search(self, query: str, page: int = 0) -> SearchResponse:
        """
        Search for a query in the ProPublica database.

        Args:
            query (str): The search query string.
            page (int, optional): The page number of results to retrieve. Defaults to 0.

        Returns:
            SearchResponse: An object containing the search results.
        """
        params = {"q": query, "page": page}
        data = self._get("search.json", params)
        return SearchResponse(**data)

    def get_filings(self, ein: str) -> list[Filing]:
        """
        Get a list of tax filings for an organization by EIN.

        Args:
            ein (str): The Employer Identification Number of the organization

        Returns:
            list[Filing]: A list of Filing objects containing information about each tax filing
        """
        params = {}
        data = self._get(f"organizations/{ein}.json", params)
        filings = data.get("filings_with_data", [])
        print(filings)
        return [Filing(**filing) for filing in filings]
