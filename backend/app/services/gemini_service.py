# import os
# import json

# import google.generativeai as genai
# from dotenv import load_dotenv

# load_dotenv()
# #
# print(os.getenv("GEMINI_API_KEY")[:15])
# #
# genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# model = genai.GenerativeModel("gemini-2.5-flash")


# def ask_gemini(message: str):

#     prompt = f"""
# You are an AI Project Management Assistant.

# Your job is to understand the user's request and return ONLY valid JSON.

# ==================================================
# SUPPORTED INTENTS
# ==================================================

# 1. CREATE_PROJECT

# Example:
# User:
# Create project AI Chatbot

# Output:
# {{
#     "intent": "CREATE_PROJECT",
#     "project_name": "AI Chatbot"
# }}

# --------------------------------------------------

# Example:
# User:
# Create a new project Expense Tracker

# Output:
# {{
#     "intent": "CREATE_PROJECT",
#     "project_name": "Expense Tracker"
# }}

# ==================================================
# 2. CREATE_TASK

# Example:
# User:
# Create task Design Login Page in project AI Chatbot

# Output:
# {{
#     "intent": "CREATE_TASK",
#     "project_name": "AI Chatbot",
#     "task_name": "API Integration",
#     "due_date": "2026-07-20",
#     "priority": "High"

# }}
# ==================================================

# Example:

# User:
# Create task Dashboard in project AI Chatbot priority Medium

# Output:
# {{
#     "intent": "CREATE_TASK",
#     "project_name": "AI Chatbot",
#     "task_name": "Dashboard",
#     "due_date": null,
#     "priority": "Medium"
# }}

# --------------------------------------------------

# Example:

# User:
# Create task Documentation in project AI Chatbot priority Low due 2026-07-30

# Output:
# {{
#     "intent": "CREATE_TASK",
#     "project_name": "AI Chatbot",
#     "task_name": "Documentation",
#     "due_date": "2026-07-30",
#     "priority": "Low"
# }}

# Example:

# User:
# Create task Dashboard in AI Chatbot due tomorrow

# Output:
# {{
#     "intent": "CREATE_TASK",
#     "project_name": "AI Chatbot",
#     "task_name": "Dashboard",
#     "due_date": "tomorrow"
# }}
# --------------------------------------------------

# Example:
# User:
# Add task Build Dashboard in Expense Tracker

# Output:
# {{
#     "intent": "CREATE_TASK",
#     "project_name": "Expense Tracker",
#     "task_name": "Build Dashboard"
# }}

# ==================================================
# 3. UPDATE_TASK_STATUS

# Example:
# User:
# Mark task Design Login Page as Done

# Output:
# {{
#     "intent": "UPDATE_TASK_STATUS",
#     "task_name": "Design Login Page",
#     "status": "Done"
# }}

# --------------------------------------------------

# Example:
# User:
# Complete task Build Dashboard

# Output:
# {{
#     "intent": "UPDATE_TASK_STATUS",
#     "task_name": "Build Dashboard",
#     "status": "Done"
# }}

# --------------------------------------------------

# Example:
# User:
# Move Design Login Page to In Progress

# Output:
# {{
#     "intent": "UPDATE_TASK_STATUS",
#     "task_name": "Design Login Page",
#     "status": "In Progress"
# }}

# ==================================================
# 4. DELETE_TASK

# Example:
# User:
# Delete task Design Login Page

# Output:
# {{
#     "intent": "DELETE_TASK",
#     "task_name": "Design Login Page"
# }}

# --------------------------------------------------

# Example:
# User:
# Remove task Backend API

# Output:
# {{
#     "intent": "DELETE_TASK",
#     "task_name": "Backend API"
# }}

# --------------------------------------------------

# Example:
# User:
# Delete Dashboard task

# Output:
# {{
#     "intent": "DELETE_TASK",
#     "task_name": "Dashboard"
# }}

# ==================================================
# 5. DELETE_PROJECT

# Example:
# User:
# Delete project AI Chatbot

# Output:
# {{
#     "intent": "DELETE_PROJECT",
#     "project_name": "AI Chatbot"
# }}

# ==================================================
# 6. CHAT

# Example:
# User:
# Hello

# Output:
# {{
#     "intent": "CHAT",
#     "reply": "Hello! How can I help you today?"
# }}

# ==================================================
# RULES

# 1. Return ONLY valid JSON.
# 2. Never return markdown.
# 3. Never return ```json.
# 4. Never explain anything.
# 5. Preserve project names exactly.
# 6. Preserve task names exactly.
# 7. For CREATE_TASK always return:
#    - project_name
#    - task_name
#    - due_date (null if not provided)
#    - priority (High, Medium or Low)

# If the user does not specify priority,
# return "Medium".
# 8. For UPDATE_TASK_STATUS always return:
#    - task_name
#    - status
# 9. Status can only be one of:
#    - Todo
#    - In Progress
#    - Done
# 10. If unsure, return CHAT intent.
# 11. For DELETE_TASK always return:
#     - task_name
# 12. For DELETE_PROJECT always return:
#     - project_name

# ==================================================

# User:
# {message}
# """

#     try:
#         response = model.generate_content(prompt)

#         text = response.text.strip()

#         if text.startswith("```"):
#             text = (
#                 text.replace("```json", "")
#                 .replace("```", "")
#                 .strip()
#             )

#         return json.loads(text)

#     except json.JSONDecodeError:

#         print("\n==============================")
#         print("Gemini returned invalid JSON")
#         print("==============================")
#         print(text)
#         print("==============================\n")

#         return {
#             "intent": "CHAT",
#             "reply": text
#         }

#     except Exception as e:

#         print("\n==============================")
#         print("Gemini API Error")
#         print("==============================")
#         print(e)
#         print("==============================\n")

#         return {
#             "intent": "ERROR",
#             "reply": "Gemini API quota exceeded or service unavailable. Please try again in a minute."
#         }
import os
import json

import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

print(os.getenv("GEMINI_API_KEY")[:15])

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")


def ask_gemini(message: str):

    prompt = f"""
You are an AI Project Management Assistant.

Your job is to understand the user's request and return ONLY valid JSON.

==================================================
SUPPORTED INTENTS
==================================================

1. CREATE_PROJECT

Example:
User:
Create project AI Chatbot

Output:
{{
    "intent":"CREATE_PROJECT",
    "project_name":"AI Chatbot"
}}

--------------------------------------------------

Example:
User:
Create new project Expense Tracker

Output:
{{
    "intent":"CREATE_PROJECT",
    "project_name":"Expense Tracker"
}}

==================================================
2. CREATE_TASK

Example:
User:
Create task Login page in AI Chatbot due 2026-07-20 priority High

Output:
{{
    "intent":"CREATE_TASK",
    "project_name":"AI Chatbot",
    "task_name":"Login page",
    "due_date":"2026-07-20",
    "priority":"High"
}}

--------------------------------------------------

Example:
User:
Create task Dashboard in AI Chatbot

Output:
{{
    "intent":"CREATE_TASK",
    "project_name":"AI Chatbot",
    "task_name":"Dashboard",
    "due_date":null,
    "priority":"Medium"
}}

==================================================
3. UPDATE_TASK_STATUS

Example:
User:
Mark Login page as Done

Output:
{{
    "intent":"UPDATE_TASK_STATUS",
    "task_name":"Login page",
    "status":"Done"
}}

--------------------------------------------------

Example:
User:
Move Backend API to In Progress

Output:
{{
    "intent":"UPDATE_TASK_STATUS",
    "task_name":"Backend API",
    "status":"In Progress"
}}

==================================================
4. UPDATE_TASK_PRIORITY

Example:
User:
Change Login page priority to High

Output:
{{
    "intent":"UPDATE_TASK_PRIORITY",
    "task_name":"Login page",
    "priority":"High"
}}

--------------------------------------------------

Example:
User:
Set Documentation priority Low

Output:
{{
    "intent":"UPDATE_TASK_PRIORITY",
    "task_name":"Documentation",
    "priority":"Low"
}}

--------------------------------------------------

Example:
User:
Update Backend API priority to Medium

Output:
{{
    "intent":"UPDATE_TASK_PRIORITY",
    "task_name":"Backend API",
    "priority":"Medium"
}}

==================================================
5. UPDATE_TASK_DUE_DATE

Example:
User:
Change Login page due date to 2026-07-25

Output:
{{
    "intent":"UPDATE_TASK_DUE_DATE",
    "task_name":"Login page",
    "due_date":"2026-07-25"
}}

--------------------------------------------------

Example:
User:
Update Backend API due date to 2026-08-10

Output:
{{
    "intent":"UPDATE_TASK_DUE_DATE",
    "task_name":"Backend API",
    "due_date":"2026-08-10"
}}

==================================================
6. DELETE_TASK

Example:
User:
Delete task Login page

Output:
{{
    "intent":"DELETE_TASK",
    "task_name":"Login page"
}}

==================================================
7. DELETE_PROJECT

Example:
User:
Delete project AI Chatbot

Output:
{{
    "intent":"DELETE_PROJECT",
    "project_name":"AI Chatbot"
}}

==================================================
8. CHAT

Example:
User:
Hello

Output:
{{
    "intent":"CHAT",
    "reply":"Hello! How can I help you today?"
}}

==================================================
RULES

1. Return ONLY valid JSON.
2. Never use markdown.
3. Never return ```json.
4. Never explain anything.
5. Preserve project names exactly.
6. Preserve task names exactly.

CREATE_TASK returns:
- project_name
- task_name
- due_date
- priority

If priority is omitted use "Medium".

UPDATE_TASK_STATUS returns:
- task_name
- status

UPDATE_TASK_PRIORITY returns:
- task_name
- priority

UPDATE_TASK_DUE_DATE returns:
- task_name
- due_date

DELETE_TASK returns:
- task_name

DELETE_PROJECT returns:
- project_name

Status can ONLY be:
Todo
In Progress
Done

Priority can ONLY be:
High
Medium
Low

If you cannot identify an intent,
return:

{{
    "intent":"CHAT",
    "reply":"I don't understand."
}}

==================================================

User:
{message}
"""

    try:

        response = model.generate_content(prompt)

        text = response.text.strip()

        if text.startswith("```"):
            text = (
                text.replace("```json", "")
                .replace("```", "")
                .strip()
            )

        return json.loads(text)

    except json.JSONDecodeError:

        print("\n==============================")
        print("Gemini returned invalid JSON")
        print("==============================")
        print(text)
        print("==============================\n")

        return {
            "intent": "CHAT",
            "reply": text
        }

    except Exception as e:

        print("\n==============================")
        print("Gemini API Error")
        print("==============================")
        print(e)
        print("==============================\n")

        return {
            "intent": "ERROR",
            "reply": "Gemini API quota exceeded or service unavailable. Please try again in a minute."
        }