import seaborn as sns
import requests
import pandas as pd
import matplotlib.pyplot as plt

# Hacker News API endpoints
TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
STORY_DETAILS_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"
COMMENTS_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"

# Function to fetch data from a URL


def fetch_data(url):
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for error responses
    return response.json()

# Function to fetch details for a specific story


def fetch_story_details(story_id):
    url = STORY_DETAILS_URL.format(story_id)
    data = fetch_data(url)
    if not data:  # Handle cases where story is deleted
        return None
    return {
        "*title*": data.get("title"),
        "*url*": data.get("url"),
        "*score*": data.get("score"),
        "*author*": data.get("by"),
        "*time*": data.get("time"),
        # Use descendants for comments count
        "*comments*": data.get("descendants", 0)
    }

# Function to fetch top level comments for a story


def fetch_comments(story_id):
    url = COMMENTS_URL.format(story_id)
    data = fetch_data(url)
    if not data.get('kids'):  # Handle cases with no comments
        return []
    comments = []
    for comment_id in data.get('kids')[:5]:
        comment_data = fetch_data(STORY_DETAILS_URL.format(comment_id))
        if comment_data:
            comments.append({
                "author": comment_data.get("by"),
                "text": comment_data.get("text"),
                "time": comment_data.get("time"),
                "parent": story_id
            })
    return comments


# Fetch top story IDs
top_stories_ids = fetch_data(TOP_STORIES_URL)[:15]  # Get top 20 stories
# Fetch details and save to CSV
stories_data = []
for story_id in top_stories_ids:
    story_details = fetch_story_details(story_id)
    if story_details:
        stories_data.append(story_details)
# print(stories_data)
df_stories = pd.DataFrame(stories_data)
df_stories.to_csv("top_stories.csv", index=False)

# Fetch and save comments to CSV
all_comments = []
for story_id in top_stories_ids:
    comments = fetch_comments(story_id)
    all_comments.extend(comments)
df_comments = pd.DataFrame(all_comments)
df_comments.to_csv("top_stories_comments.csv", index=False)

# Analyze and plot data
average_score = df_stories["*score*"].mean()
average_comments = df_stories["*comments*"].mean()


# Grades and corresponding percentages (replace with your data if available)
grades = []
percentages = []  # Percentages should sum to 100

for grade in df_stories["*title*"][:15]:
    grades.append(grade)

for a in df_stories["*score*"][:15]:
    percentages.append(a)

# Create a pie chart
plt.figure(figsize=(8, 6))
plt.pie(percentages, labels=grades, autopct="%1.1f%%", startangle=140)
plt.title("GPA \naverage_score = df_stories[""*score*""].mean()")
plt.axis('equal')  # Equal aspect ratio ensures a circular pie chart

# Display the pie chart
plt.show()

comment = []
percentages = []  # Percentages should sum to 100

for grade in df_stories["*title*"][:15]:
    comment.append(grade)

for a in df_stories["*comments*"][:15]:
    percentages.append(a)

# Create a pie chart
plt.figure(figsize=(8, 6))
plt.pie(percentages, labels=grades, autopct="%1.1f%%", startangle=140)
plt.title("Average responses \naverage responses = df_stories[""*score*""].mean()")
plt.axis('equal')  # Equal aspect ratio ensures a circular pie chart

# Display the pie chart
plt.show()