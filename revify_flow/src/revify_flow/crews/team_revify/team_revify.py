from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List

# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class TeamRevify():
    """TeamRevify crew for product review analysis"""

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def manager_agent(self) -> Agent:
        """Creates the manager agent that orchestrates the workflow"""
        return Agent(
            config=self.agents_config['manager_agent'],
            verbose=True
        )

    @agent
    def feature_extractor(self) -> Agent:
        """Creates the feature extraction agent"""
        return Agent(
            config=self.agents_config['feature_extractor'],
            verbose=True
        )

    @agent
    def review_scraper(self) -> Agent:
        """Creates the review scraping agent"""
        return Agent(
            config=self.agents_config['review_scraper'],
            verbose=True
        )

    @agent
    def review_analysis_agent(self) -> Agent:
        """Creates the review analysis agent for specific features"""
        return Agent(
            config=self.agents_config['review_analysis_agent'],
            verbose=True
        )

    @task
    def extract_features_task(self) -> Task:
        """Task to extract key product features"""
        return Task(
            config = self.tasks_config['extract_features_task']
        )

    @task
    def scrape_reviews_task(self) -> Task:
        """Task to scrape reviews from the provided product URL"""
        return Task(
            description="Scrape user reviews from the provided product URL",
            agent=self.review_scraper(),
            expected_output="A collection of user reviews with ratings"
        )
    
    @task
    def analyze_feature_reviews_task(self, feature_name) -> Task:
        """Task to analyze reviews for a specific feature"""
        return Task(
            description=f"Analyze all reviews for the '{feature_name}' feature",
            agent=self.review_analysis_agent(),
            context=[self.scrape_reviews_task(), self.extract_features_task()],
            expected_output=f"Sentiment analysis and summary for '{feature_name}' feature"
        )
    
    @task
    def compile_final_report_task(self) -> Task:
        """Task to compile the final product analysis report"""
        return Task(
            description="Compile a comprehensive product analysis report based on feature-wise review insights",
            agent=self.manager_agent(),
            context=[self.extract_features_task(), self.scrape_reviews_task()],
            expected_output="A detailed product analysis report with feature-specific insights and overall recommendations"
        )

    @crew
    def crew(self) -> Crew:
        """Creates the TeamRevify crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )

