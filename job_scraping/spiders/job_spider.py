import scrapy


class JobSpider(scrapy.Spider):
    name = "jobspider"

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
            role_type = job_info[2]
            company = job_info[3]
            job_details = job.css("p.detail::text").get()

            yield {
                "title": job_title,
                "location": job_location,
                "date_added": date_added,
                "company": company,
                "role_type": role_type,
                "details": job_details,
            }
