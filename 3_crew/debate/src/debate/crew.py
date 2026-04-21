import os
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task, before_kickoff
from crewai.agents.agent_builder.base_agent import BaseAgent

@CrewBase
class Debate():
    """Debate crew"""

    agents: list[BaseAgent]
    tasks: list[Task]

    @before_kickoff
    def ensure_output_directory(self, inputs):
        """Ensure the output directory exists."""
        if not os.path.exists('output'):
            os.makedirs('output')
        return inputs

    @agent
    def debater(self) -> Agent:
        return Agent(
            config=self.agents_config['debater'], # type: ignore[index]
            llm=LLM(model="openai/gpt-4o-mini"),
            verbose=True
        )

    @agent
    def judge(self) -> Agent:
        return Agent(
            config=self.agents_config['judge'], # type: ignore[index]
            llm=LLM(model="openai/gpt-4o"),
            verbose=True
        )

    @task
    def propose_task(self) -> Task:
        return Task(
            config=self.tasks_config['propose_task'], # type: ignore[index]
            output_file='output/propose.md'
        )

    @task
    def oppose_task(self) -> Task:
        return Task(
            config=self.tasks_config['oppose_task'], # type: ignore[index]
            output_file='output/oppose.md'
        )

    @task
    def decide_task(self) -> Task:
        return Task(
            config=self.tasks_config['decide_task'], # type: ignore[index]
            output_file='output/decide.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Debate crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
