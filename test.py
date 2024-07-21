# import pandas as pd
# a = [0, 1, 2]
# a.append([[{'sdkf': 'afd', 'a': 'b', 'dfgv':5, 5: 'sgv'}, 5, 7], [{'dc': 'dsc'}]])
# x = pd.DataFrame(a)
# print(a)
# print(x)
# b = x['a'].mean()


# print(b)
import matplotlib.pyplot as plt

a = ['A', 'B', 'C', 'D', 'F']
b = [25, 30, 20, 15, 10]

# Grades and corresponding percentages (replace with your data if available)
grades = []
percentages = []  # Percentages should sum to 100
for grade in a[:2]:
    grades.append(grade)

for a in b[:3]:
    percentages.append(a)

# Create a pie chart
plt.figure(figsize=(8, 6))
plt.pie(percentages, labels=grades, autopct="%1.1f%%", startangle=140)
plt.title("Grade Distribution")
plt.axis('equal')  # Equal aspect ratio ensures a circular pie chart

# Display the pie chart
plt.show()
