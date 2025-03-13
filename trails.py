import requests

# Define the search query
search_query = "djvulibre-3.5.27+4.10.5_win32.zip"

# Perform a search on GitHub and SourceForge for possible sources
github_url = f"https://api.github.com/search/repositories?q={search_query}"
sourceforge_url = f"https://sourceforge.net/directory/?q={search_query}"

# Try searching GitHub
github_response = requests.get(github_url)
if github_response.status_code == 200:
    github_results = github_response.json()
    github_links = [repo["html_url"] for repo in github_results.get("items", [])]
else:
    github_links = []

# Provide the SourceForge search link
sourceforge_links = [sourceforge_url]

# Combine the results
download_links = github_links + sourceforge_links

# Display results
download_links
