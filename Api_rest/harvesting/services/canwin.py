import requests
from datetime import datetime
from harvesting.models import Dataset, Organization, Ressource, Tag
from django.utils.timezone import make_aware


def fetch_canwin_data(query="sea ice melt", limit=1000):
    """
    Fetch datasets from the CanWin CKAN API and normalize them.
    """
    url = "https://canwin-datahub.ad.umanitoba.ca/data/api/3/action/package_search"
    params = {"q": query, "rows": limit}

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f" Error fetching CanWin data: {e}")
        return []

    if not data.get("success"):
        print(" API returned success=false")
        return []

    results = data.get("result", {}).get("results", [])
    datasets = []

    for item in results:
        organization = item.get("organization") or {}
        resources = item.get("resources", [])
        tags = item.get("tags", [])

        # Convert string dates safely
        def parse_date(date_str):
            try:
                return make_aware(datetime.fromisoformat(date_str.replace("Z", "+00:00")))
            except Exception:
                return None

        datasets.append({
            "source": "CanWin",
            "source_id": item.get("id"),
            "title": item.get("title"),
            "description": item.get("notes", ""),
            "author_email": item.get("author_email", ""),
            "organization": organization,
            "tags": tags,
            "resources": resources,
            "created_at": parse_date(item.get("metadata_created", "")),
            "updated_at": parse_date(item.get("metadata_modified", "")),
        })

    print(f" Fetched {len(datasets)} datasets from CanWin.")
    return datasets


def save_canwin_data(query="sea ice melt"):
    """
    Save normalized CanWin data into Django models.
    """
    data = fetch_canwin_data(query=query)

    created_count, updated_count = 0, 0

    for item in data:
        dataset_obj, created = Dataset.objects.update_or_create(
            source_id=item["source_id"],
            defaults={
                "source": item["source"],
                "title": item["title"],
                "description": item["description"],
                "author_email": item["author_email"],
                "created_at": item["created_at"],
                "updated_at": item["updated_at"],
            },
        )

        if created:
            created_count += 1
        else:
            updated_count += 1

        #  Organization (many-to-one)
        org = item["organization"]
        if org and org.get("id"):
            Organization.objects.update_or_create(
                organization_id=org.get("id"),
                defaults={
                    "name": org.get("name", ""),
                    "title": org.get("title", ""),
                    "description": org.get("description", ""),
                    "image_url": org.get("image_url", ""),
                    "created_at": item["created_at"],
                },
            )
            # Associate dataset with organization
            org_obj = Organization.objects.get(organization_id=org["id"])
            dataset_obj.organization = org_obj
            dataset_obj.save()

        # Tags
        for tag in item["tags"]:
            if tag.get("id"):
                Tag.objects.update_or_create(
                    tag_id=tag["id"],
                    defaults={
                        "name": tag.get("name", ""),
                        "dataset": dataset_obj,
                    },
                )

        #  Resources
        for res in item["resources"]:
            if res.get("id"):
                Ressource.objects.update_or_create(
                    ressource_id=res["id"],
                    defaults={
                        "created_at": res.get("created"),
                        "updated_at": res.get("last_modified"),
                        "description": res.get("description", ""),
                        "format": res.get("format", ""),
                        "name": res.get("name", ""),
                        "url": res.get("url", ""),
                        "url_type": res.get("url_type", ""),
                        "dataset": dataset_obj,
                    },
                )

    print(f"{created_count} datasets created, {updated_count} updated.")
    print(" All CanWin datasets saved successfully.")
