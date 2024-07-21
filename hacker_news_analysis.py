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
#   print(response.json())
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
      "*comments*": data.get("descendants", 0)  # Use descendants for comments count
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
# print(TOP_STORIES_URL)
# print(top_stories_ids)

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
print(df_stories["*score*"])
print(df_stories["*score*"][1])
average_score = df_stories["*score*"].mean()
average_comments = df_stories["*comments*"].mean()
print(average_score)
print(average_comments)

import seaborn as sns

# Grades and corresponding percentages (replace with your data if available)
grades = []
percentages = []  # Percentages should sum to 100

# Create a pie chart
plt.figure(figsize=(8, 6))
plt.pie(percentages, labels=grades, autopct="%1.1f%%", startangle=140)
plt.title("Grade Distribution")
plt.axis('equal')  # Equal aspect ratio ensures a circular pie chart

# Display the pie chart
plt.show()



# Plot average score
# sns.barplot(x=["Average Score"], y=[average_score], title="Average Score of Top Stories", grid=True)
# plt.tight_layout()
# plt.savefig("average_score.png")
# plt.show()
# plt.close()

# Plot average comments
# sns.barplot(x=["Average Comments"], y=[average_comments], title="Average Comments per Story", grid=True)
# plt.tight_layout()
# plt.savefig("average_comments.png")
# plt.show()
# plt.close()

# Plot average score
# plt.figure(figsize=(8, 6))
# plt.bar(["Average Score"], [average_score])
# plt.xlabel("Metric")
# plt.ylabel("Score")
# plt.title("Average Score of Top Stories")
# plt.grid(axis='y')
# plt.tight_layout()
# plt.savefig("average_score.png")
# plt.show()
# plt.close()

# # Plot average comments
# plt.figure(figsize=(8, 6))
# plt.bar(["Average Comments"], [average_comments])
# plt.xlabel("Metric")
# plt.ylabel("Number of Comments")
# plt.title("Average Comments per Story")
# plt.grid(axis='y')
# plt.tight_layout()
# plt.savefig("average_comments.png")
# plt.show()
# plt.close()

# # Print summary statistics
# print("Summary Statistics:")
# print
