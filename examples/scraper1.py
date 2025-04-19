from crewai_tools import ScrapeWebsiteTool

# To enable scrapping any website it finds during it's execution
tool = ScrapeWebsiteTool()

# Initialize the tool with the website URL, 
# so the agent can only scrap the content of the specified website
tool = ScrapeWebsiteTool(website_url='https://www.amazon.in/product-reviews/B0CY2377YW/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews')

# Extract the text from the site
text = tool.run()
print(text)