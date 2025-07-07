from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai_tools import FileReadTool, CodeInterpreterTool
from typing import List
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

file_tool = FileReadTool(file_path="knowledge/carrier_data.csv")
code_tool = CodeInterpreterTool()

@CrewBase
class Logi():
    """Logi crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    
    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def rfq_creator(self) -> Agent:
        return Agent(
            config=self.agents_config['rfq_creator'], # type: ignore[index]
            verbose=True,
        )

    @agent
    def carrier_evaluator(self) -> Agent:
        return Agent(
            config=self.agents_config['carrier_evaluator'], # type: ignore[index]
            verbose=True,
            tools=[file_tool, code_tool],
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def create_rfq_task(self) -> Task:
        return Task(
            config=self.tasks_config['create_rfq_task'], # type: ignore[index]
        )

    @task
    def evaluate_carrier_task(self) -> Task:
        return Task(
            config=self.tasks_config['evaluate_carrier_task'], # type: ignore[index]
            output_file='carrier_report.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Logi crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
