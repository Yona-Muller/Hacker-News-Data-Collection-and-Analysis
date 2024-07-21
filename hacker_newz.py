import seaborn as sns
import requests
import pandas as pd
import matplotlib.pyplot as plt

# Hacker News API endpoints
TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
STORY_DETAILS_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"
COMMENTS_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"


class HackerNewsAnalyzer:
    """
    This class fetches, analyzes, and visualizes data from Hacker News.
    """

    def __init__(self):
        self.top_stories_ids = None
        self.stories_data = None
        self.df_stories = None
        self.df_comments = None

    def fetch_data(self, url):
        """
        Fetches data from a URL and handles errors.

        Args:
            url (str): The URL to fetch data from.

        Returns:
            dict: The JSON data fetched from the URL.
        """
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for error responses
        return response.json()

    def fetch_story_details(self, story_id):
        """
        Fetches details for a specific story.

        Args:
            story_id (int): The ID of the story to fetch details for.

        Returns:
            dict: A dictionary containing story details, or None if not found.
        """
        url = STORY_DETAILS_URL.format(story_id)
        data = self.fetch_data(url)
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

    def fetch_comments(self, story_id):
        """
        Fetches top level comments for a story.

        Args:
            story_id (int): The ID of the story to fetch comments for.

        Returns:
            list: A list of dictionaries containing comment details.
        """
        url = COMMENTS_URL.format(story_id)
        data = self.fetch_data(url)
        if not data.get('kids'):  # Handle cases with no comments
            return []
        comments = []
        for comment_id in data.get('kids')[:5]:
            comment_data = self.fetch_data(STORY_DETAILS_URL.format(comment_id))
            if comment_data:
                comments.append({
                    "author": comment_data.get("by"),
                    "text": comment_data.get("text"),
                    "time": comment_data.get("time"),
                    "parent": story_id
                })
        return comments

    def analyze_and_plot_data(self):
        """
        Analyzes and plots data from fetched stories.
        """

        # Fetch top story IDs
        self.top_stories_ids = self.fetch_data(TOP_STORIES_URL)[:15]

        # Fetch and store story details
        self.stories_data = []
        for story_id in self.top_stories_ids:
            story_details = self.fetch_story_details(story_id)
            if story_details:
                self.stories_data.append(story_details)
        self.df_stories = pd.DataFrame(self.stories_data)
        self.df_stories.to_csv("top_stories.csv", index=False)

        # Analyze and plot average score
        average_score = self.df_stories["*score*"].mean()

        # Create pie chart for average score
        grades = []
        percentages = []  # Percentages should sum to 100

        for grade in self.df_stories["*title*"][:15]:
            grades.append(grade)

        for score in self.df_stories["*score*"][:15]:
            percentages.append(score)

        
        # Create a pie chart
        plt.figure(figsize=(8, 6))
        plt.pie(percentages, labels=grades, autopct="%1.1f%%", startangle=140)
        plt.title("GPA \naverage_score = {:.2f}".format(average_score))
        plt.axis('equal')  # Equal aspect ratio ensures a circular pie chart

        # Display the pie chart
        plt.show()

        # Fetch and store comments
        all_comments = []
        for story_id in self.top_stories_ids:
            comments = self.fetch_comments(story_id)
            all_comments.extend(comments)
        self.df_comments = pd.DataFrame(all_comments)
        self.df_comments.to_csv("top_stories_comments.csv", index=False)

        # Analyze and plot average comments
        average_comments = self.df_stories["*comments*"].mean()

        # Create pie chart for average comments
        grades = []
        percentages = []  # Percentages should sum to 100

        for grade in self.df_stories["*title*"][:15]:
            grades.append(grade)

        for comment_count in self.df_stories["*comments*"][:15]:
            percentages.append(comment_count)

        # Create a pie chart
        plt.figure(figsize=(8, 6))
        plt.pie(percentages, labels=grades, autopct="%1.1f%%", startangle=140)
        plt.title("Average responses \naverage responses = {:.2f}".format(average_comments))
        plt.axis('equal')  # Equal aspect ratio ensures a circular pie chart

        # Display the pie chart
        plt.show()


if __name__ == "__main__":
    analyzer = HackerNewsAnalyzer()
    analyzer.analyze_and_plot_data()

