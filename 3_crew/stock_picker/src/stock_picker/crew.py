from typing import Any

from crewai import Agent, Crew, Process, Task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.project import CrewBase, agent, crew, task
from crewai.tasks.task_output import TaskOutput
from crewai_tools import SerperDevTool

from stock_picker.models import TrendingCompanyList, TrendingCompanyResearchList
from stock_picker.tools.custom_tool import send_push_notification


@CrewBase
class StockPicker:
    """StockPicker crew"""

    agents: list[BaseAgent]
    tasks: list[Task]

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def trending_company_finder(self) -> Agent:
        return Agent(
            config=self.agents_config["trending_company_finder"],  # type: ignore[index]
            tools=[SerperDevTool()],
            verbose=True,
        )

    @agent
    def financial_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config["financial_researcher"],  # type: ignore[index]
            tools=[SerperDevTool()],
            verbose=True,
        )

    @agent
    def stock_picker(self) -> Agent:
        return Agent(
            config=self.agents_config["stock_picker"],  # type: ignore[index]
            tools=[send_push_notification],
            verbose=True,
        )

    def manager(self) -> Agent:
        return Agent(
            config=self.agents_config["manager"],  # type: ignore[index]
            allow_delegation=True,
        )

    def _validate_research_matches_trending(
        self, task_output: TaskOutput
    ) -> tuple[bool, Any]:
        expected = {
            c.ticker.strip().upper()
            for c in self.find_trending_companies().output.pydantic.companies
        }
        actual = {r.ticker.strip().upper() for r in task_output.pydantic.research}
        if actual != expected:
            return False, (
                f"Research tickers {actual} do not match the exact 3 trending tickers {expected}"
            )
        return True, task_output

    @task
    def find_trending_companies(self) -> Task:
        return Task(
            config=self.tasks_config["find_trending_companies"],  # type: ignore[index]
            output_pydantic=TrendingCompanyList,
        )

    @task
    def research_trending_companies(self) -> Task:
        return Task(
            config=self.tasks_config["research_trending_companies"],  # type: ignore[index]
            context=[self.find_trending_companies()],
            output_pydantic=TrendingCompanyResearchList,
            guardrail=self._validate_research_matches_trending,
        )

    @task
    def pick_best_company(self) -> Task:
        return Task(
            config=self.tasks_config["pick_best_company"],  # type: ignore[index]
            context=[self.research_trending_companies()],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the StockPicker crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.hierarchical,
            manager_agent=self.manager(),
            verbose=True,
            memory=True,
            tracing=True,
        )
