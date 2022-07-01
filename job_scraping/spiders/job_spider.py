import scrapy


class FreePythonJobBoardSpider(scrapy.Spider):
    name = "jb_spider"

    start_urls = [
        "https://pythonjobs.github.io/",
    ]

    def parse(self, response):
        jobs = response.css("div.job")

        for job in jobs:

            job_info = job.css("span.info::text").getall()

            job_title = job.css("h1 a::text").get()
            job_location = job_info[0]
            date_added = job_info[1]
            contract = job_info[2]
            company = job_info[3]
            job_details = job.css("p.detail::text").get()

            yield {
                "title": job_title,
                "location": job_location,
                "date_added": date_added,
                "company": company,
                "contract": contract,
                "details": job_details,
            }


class Indeed(scrapy.Spider):
    name = "id_spider"

    start_urls = [
        "https://au.indeed.com/jobs?q=python",
    ]

    def parse(self, response):
        jobs = response.css("ul.jobsearch-ResultsList li")

        for job in jobs:
            metadata = job.css("div.attribute_snippet::text").getall()
            short_description = job.css("div.jobSnippet ul li::text").getall()
            job_title = job.css("h2.jobTitle a span::text").get()
            company = job.css("span.companyName::text").get()
            location = job.css("div.companyLocation::text").get()

            date_added = job.css("span.date::text").get()
            url = job.css("a::attr(href)").get()

            if job_title is not None:

                yield {
                    "job_title": job_title,
                    "short_description": short_description,
                    "company": company,
                    "location": location,
                    "date_added": date_added,
                    "url": url,
                    "metadata": metadata,
                }
