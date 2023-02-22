import tomli

from azure_requests import AzureRequests

with open("example.toml", "rb") as f:
    CONFIG = tomli.load(f)

azure_requests = AzureRequests(
    pat=CONFIG["pat"],
    organization=CONFIG["organization"],
    project=CONFIG["project"],
)

# ----------------------------- create work item -----------------------------

work_item = azure_requests.api(
    # https://learn.microsoft.com/en-us/rest/api/azure/devops/wit/work-items/create?view=azure-devops-rest-7.0
    "POST https://dev.azure.com/{organization}/{project}/_apis/wit/workitems/${type}?api-version=7.0",
    type="Task",
).request(
    json=[
        {
            "op": "add",
            "path": "/fields/System.Title",
            "from": None,
            "value": "Sample task",
        }
    ]
)

WI_ID = work_item["id"]
print(f"Work item created with id {WI_ID}")

# ----------------------------- get work item -----------------------------

work_item = azure_requests.api(
    # Copy-pasted from https://learn.microsoft.com/en-us/rest/api/azure/devops/wit/work-items/get-work-item?view=azure-devops-rest-7.0
    "GET https://dev.azure.com/{organization}/{project}/_apis/wit/workitems/{id}?api-version=7.0",
    # custom URL parameters
    id=WI_ID,
).request()

print(
    f"The work item was changed by "
    + work_item["fields"]["System.ChangedBy"]["displayName"]
    + " at "
    + work_item["fields"]["System.ChangedDate"]
)

# ----------------------------- update work item -----------------------------

work_item = azure_requests.api(
    # Copy-pasted from https://learn.microsoft.com/en-us/rest/api/azure/devops/wit/work-items/update?view=azure-devops-rest-7.0
    "PATCH https://dev.azure.com/{organization}/{project}/_apis/wit/workitems/{id}?api-version=7.0",
    id=WI_ID,
).request(
    json=[
        {"op": "test", "path": "/rev", "value": work_item["rev"]},
        {
            "op": "add",
            "path": "/fields/System.History",
            "value": "This was just a test workitem for <tt>azure_requests</tt> package. Remove from backlog.",
        },
        {
            "op": "add",
            "path": "/relations/-",
            "value": {
                "rel": "Hyperlink",
                "url": "https://pypi.org/project/azure-requests/",
            },
        },
        {"op": "add", "path": "/fields/System.State", "value": "Removed"},
    ]
)

print(
    f"The work item is removed from backlog. See: "
    + work_item["_links"]["html"]["href"]
)

# ----------------------------- delete work item -----------------------------

azure_requests.api(
    # Copy-pasted from https://learn.microsoft.com/en-us/rest/api/azure/devops/wit/work-items/delete?view=azure-devops-rest-7.0
    "DELETE https://dev.azure.com/{organization}/{project}/_apis/wit/workitems/{id}?api-version=7.0",
    id=WI_ID,
).request()
