# CrewAI Agentic AI Model

## Overview

This model leverages the CrewAI framework to perform collaborative tasks using a multi-agent system. The system consists of specialized AI agents that work together to research topics and generate summary content based on user queries.

## Model Description

- **Name**: crewai Chat Agent
- **ID**: ac94bc44-3c0d-4072-a79d-b2fcfef04244
- **Language**: Python
- **Framework**: CrewAI
- **Purpose**: Collaborative content research and summarization

## Architecture

The model implements a task-oriented multi-agent system with the following key agents:

### 1. Researcher Agent
- **Role**: Senior Research Analyst
- **Goal**: Discover new insights
- **Backstory**: "You're an expert at finding interesting information"
- **Responsibilities**: 
  - Receives a user query and conducts research.
  - Gathers key facts and information related to the query.

### 2. Writer Agent
- **Role**: Content Writer
- **Goal**: Write engaging content
- **Backstory**: "You're a talented writer who simplifies complex information"
- **Responsibilities**:
  - Takes the information gathered by the researcher.
  - Composes a concise and easy-to-read summary.

### Crew Orchestration
The `Crew` object manages the workflow:
- It is initialized with the list of agents (`researcher`, `writer`).
- It is assigned a sequence of tasks (`research_task`, `write_task`).
- The `kickoff()` method starts the execution, ensuring tasks are performed in order and the output of one task can be used by the next.

## Configuration

### Hyperparameters

The model is configured via `config.json` and expects the following parameters to connect to an LLM service (like NVIDIA NIM):

| Parameter | Description |
|-----------|-------------|
| `LLM_MODEL` | The specific inference model to use (e.g., `meta/llama3-8b-instruct`) |
| `LLM_BASE_URL` | The base URL for the LLM API endpoint. |
| `LLM_API_KEY` | The API key for authenticating with the LLM service. |

**Important**: The API key should be securely stored and provided during deployment, typically by updating `config.json`.

## Usage

### Input Format

The model's `invoke` method accepts a single string query:

```python
# Example call within the scoring logic
invoke(query="What are the latest advancements in AI?")
```

### Output Format

The model returns a dictionary representing the final output from the CrewAI workflow. This is the JSON representation of the final task's result.

### Example Response
```json
{
  "description": "Write a short summary about: The future of AI",
  "agent": "Content Writer",
  "expected_output": "A concise summary (~100 words) about: The future of AI",
  "result": "The future of AI is poised to be transformative, with advancements in machine learning, natural language processing, and computer vision driving innovation across industries. We can expect more personalized experiences, autonomous systems, and breakthroughs in science and medicine. However, ethical considerations and job displacement remain key challenges to address."
}
```

## Features

### Multi-Agent Collaboration
- Agents with distinct roles (`researcher`, `writer`) collaborate on a task.
- The `Crew` orchestrates the workflow, passing information between agents.

### Dynamic Task Creation
- Tasks are built dynamically based on the user's input query, making the model adaptable to a wide range of topics.

### Error Handling
- The `invoke` method includes a try-except block to catch and report any errors that occur during the CrewAI execution, returning an error message in the output.

### Extensible Framework
- New agents and tasks can be easily added to the crew to handle more complex workflows.

## File Structure

```
agentic_ai_crewai/
├── README.md           # This documentation file
├── config.json         # Model configuration and hyperparameters
├── model.json          # Model metadata and description
└── model_modules/
    ├── __init__.py     # Python package initialization
    ├── training.py     # Model training logic (placeholder)
    ├── scoring.py      # Model inference/scoring logic with ModelScorer class
    ├── evaluation.py   # Model evaluation metrics (placeholder)
    └── requirements.txt # Python dependencies
```

## Dependencies

Key dependencies for this model include:
- `crewai`: The core framework for orchestrating agents.
- `langchain-nvidia-ai-endpoints`: For integrating with NVIDIA's AI models.
- `langchain`: Provides the foundational components for building LLM applications.
- `teradatamodelops`: For integration into the ModelOps environment.

See `model_modules/requirements.txt` for the complete list.

## Setup Instructions

1. **Install Dependencies**: Ensure all packages listed in `model_modules/requirements.txt` are installed in the environment.
2. **Configure API**: Update `config.json` with the correct `LLM_MODEL`, `LLM_BASE_URL`, and a valid `LLM_API_KEY`.
3. **Deploy**: Deploy the model using standard ModelOps procedures.

## Use Cases

This model is well-suited for:

1. **Automated Content Creation**: Generating summaries or short articles on a given topic.
2. **Research Assistance**: Quickly gathering and summarizing information.
3. **Educational Tools**: Providing concise explanations of complex subjects.

## Example Workflow

1. **Input**: A user provides a query (e.g., "Explain quantum computing").
2. **Task Creation**: The `build_tasks` method creates a research task and a writing task based on the query.
3. **Research**: The `researcher` agent executes its task to find information about quantum computing.
4. **Writing**: The `writer` agent receives the research findings and executes its task to write a summary.
5. **Output**: The final summary from the `writer` agent is returned as the result.

## Best Practices

- **Clear Prompts**: Provide specific and clear queries to get the best results from the agents.
- **Agent Tuning**: The `role`, `goal`, and `backstory` of each agent can be modified to specialize their behavior for different domains.
- **Model Selection**: The choice of `LLM_MODEL` will significantly impact the quality of the output. Use a model that is appropriate for the complexity of the tasks.

## Limitations

- **Content Quality**: The output quality is dependent on the capabilities of the underlying LLM.
- **Sequential Process**: The default CrewAI process is sequential; tasks are handled one after another, which may not be the most efficient for all workflows.
- **Fact-Checking**: As with any LLM-based system, the generated content should be reviewed for factual accuracy, especially for critical applications.

## Troubleshooting

### Common Issues

1. **Configuration Error**: Double-check that `config.json` contains the correct keys and valid values for your LLM provider.
2. **API Authentication**: Ensure the `LLM_API_KEY` is correct and has not expired.
3. **Network Issues**: Verify that the deployment environment can reach the `LLM_BASE_URL`.
4. **Dependency Conflicts**: Make sure that all required packages are installed and their versions are compatible.

### Error Messages

The model will return a JSON object with an `error` key if an exception occurs during the `invoke` process, providing a message to help diagnose the issue.
```json
{"error": "Description of the error that occurred."}
```
