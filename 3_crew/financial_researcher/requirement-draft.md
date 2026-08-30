
The goal of this project is to create a financial researcher.
The scaffolding have been created by running the following command:
```
crewai create crew financial_researcher
```
So examine the project structure to have a better understanding of the project.

### Project Structure

```text
financial_researcher/
├── .gitignore
├── pyproject.toml
├── README.md
├── requirement-draft.md
├── knowledge/
│   └── user_preference.txt
├── src/
│   └── financial_researcher/
│       ├── __init__.py
│       ├── crew.py
│       ├── main.py
│       ├── config/
│       │   ├── agents.yaml
│       │   └── tasks.yaml
│       └── tools/
│           ├── __init__.py
│           └── custom_tool.py
└── tests/
```
The researcher is a senior financial researcher for a company called {company} 
The goal of the researcher is to find the most relevant information about the company {company} and its competitors.
The researcher should be able to find the most relevant information and present it in a clear and concise manner.
So agent #1 is the researcher. 

Agent #2 is a market analyst and report writer for the company (same company {company}). 
The goal is to analyze the company and create a comprehensive, well structured report that presents insights in a clear and engaging way. 

use llm openai/gpt-4o-mini. 



