# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json
from itemadapter import ItemAdapter
from urllib.parse import urljoin
from scrapy.exceptions import DropItem


class JobScrapingPipeline:
    def process_item(self, item, spider):
        return item


class JobTitlePipeline(object):
    """
    Select Only Python Jobs
    """

    def process_item(self, item, spider):
        if item.get("job_title"):
            if "Python" not in item["job_title"]:
                raise DropItem(item)
        return item


class MetaDataPipeline(object):
    """
    Assigns Metadata if it exists
    """

    def process_item(self, item, spider):
        if item.get("metadata"):
            if len(item["metadata"]) == 3:
                item["salary_range"] = item["metadata"][0]
                item["contract"] = item["metadata"][1]
                item["hours_per_week"] = item["metadata"][2]

        del item["metadata"]
        return item

        # else:
        #     del item["metadata"]
        #     return item


class UrlPipeline(object):
    """
    join job url to base url
    """

    def process_item(self, item, spider):
        base_uri = "https://au.indeed.com/jobs?q=python"
        if item.get("url"):
            item["url"] = urljoin(base_uri, item["url"])

        return item


class CompanyPipeline(object):
    """
    Checks and chooses the appropriate company
    """

    def process_item(self, item, spider):
        if item.get("company2"):
            item["company"] = item["company2"]
        del item["company2"]

        return item


class JsonWritePipeline(object):
    def process_item(self, item, spider):
        jobs = json.dumps(dict(item)) + "\n"
        with open("jobs.json", "a") as f:
            f.write(jobs)
        return item
