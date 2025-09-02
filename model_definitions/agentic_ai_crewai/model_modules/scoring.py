import warnings
import json
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from crewai import Agent, Task, Crew, LLM
warnings.filterwarnings('ignore')
warnings.simplefilter(action='ignore', category=DeprecationWarning)
warnings.simplefilter(action='ignore', category=UserWarning)
warnings.simplefilter(action='ignore', category=FutureWarning)
class ModelScorer(object):
    """
    Model scorer using CrewAI agents for collaborative tasks.
    """
    def __init__(self):
        """Initialize CrewAI agents and tasks based on config."""

        with open("artifacts/input/model_config.json", "r") as f:
            config = json.load(f)

        self.llm = LLM(
            model=f"nvidia_nim/{config['LLM_MODEL']}",
            base_url=config["LLM_BASE_URL"],
            api_key=config["LLM_API_KEY"],
        )

        self.researcher = Agent(
            role='Senior Research Analyst',
            goal='Discover new insights',
            backstory="You're an expert at finding interesting information",
            llm=self.llm,
            verbose=True
        )

        self.writer = Agent(
            role='Content Writer',
            goal='Write engaging content',
            backstory="You're a talented writer who simplifies complex information",
            llm=self.llm,
            verbose=True
        )
    def build_tasks(self, user_query):
        """Build tasks dynamically based on user query."""
        self.research_task = Task(
            description=f'Find information about: {user_query}',
            agent=self.researcher,
            expected_output=f"A list of key facts about: {user_query}"
        )
        self.write_task = Task(
            description=f'Write a short summary about: {user_query}',
            agent=self.writer,
            expected_output=f"A concise summary (~100 words) about: {user_query}"
        )
        self.crew = Crew(
            agents=[self.researcher, self.writer],
            tasks=[self.research_task, self.write_task],
            verbose=True
        )
    def invoke(self, query):
        """
        Run the CrewAI workflow and return the result (synchronous).
        """
        try:
            self.build_tasks(query)
            print(f"Started scoring with CrewAI agents for query: {query} ...")
            result = self.crew.kickoff()
            print("CrewAI Result:\n", result)
            return result.json_dict
        except Exception as e:
            print("Error occurred while invoking CrewAI:", e)
            return {"error": str(e)}