import tomli
import itertools
import concurrent

import scripthelper
import logging

logger = scripthelper.bootstrap()
logging.getLogger("httpx").setLevel(scripthelper.WARNING)
logging.getLogger("httpcore").setLevel(scripthelper.WARNING)
logging.getLogger("hpack").setLevel(scripthelper.WARNING)

from azure_requests import AzureRequests

with open("example.toml", "rb") as f:
    CONFIG = tomli.load(f)

azure_requests = AzureRequests(
    pat=CONFIG["pat"],
    organization=CONFIG["organization"],
    project=CONFIG["project"],
)

def fetch_wi(counter):
    work_item = azure_requests.api(
        # Copy-pasted from https://learn.microsoft.com/en-us/rest/api/azure/devops/wit/work-items/get-work-item?view=azure-devops-rest-7.0
        "GET https://dev.azure.com/{organization}/{project}/_apis/wit/workitems/{id}?api-version=7.0",
        # custom URL parameters
        id=432226,
    ).request()
    return counter

with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
    future_to_url = (executor.submit(fetch_wi, counter) for counter in range(100))
    for future in concurrent.futures.as_completed(future_to_url):
        try:
            print(future.result())
        except Exception as ex:
            print(ex)