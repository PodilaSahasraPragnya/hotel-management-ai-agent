# Hotel Management AI Agent

A Python-based simulation of an AI agent that carries out hotel management tasks by interacting with a simulated hotel environment.

## Overview

The Hotel Management AI Agent demonstrates how an agent can work toward a goal by selecting actions, using hotel-related tools, observing results, and determining whether the goal has been completed.

For example, a task might be:

> Check in a guest for two nights, assign a clean room, and add late checkout.

The application demonstrates the workflow of an agent interacting with an environment rather than simply providing a text-based response.

**Note:** This is a simulation project. It does not connect to real hotels, guest records, reservations, or payment systems.

## Features

- Simulated hotel management tasks.
- Agent-based task execution.
- Separation of hotel tools and the simulated environment.
- Observation of actions and their results.
- Goal-completion workflow.
- Streamlit-based application interface.
- Deterministic default controller for predictable, repeatable demonstrations.

## Technologies Used

- **Python** — Application logic and agent workflow.
- **Streamlit** — Web-based user interface.

## How It Works

The project follows this workflow:

1. **Goal:** Define the hotel management task.
2. **Agent:** Determine the actions needed to pursue the goal.
3. **Tools:** Execute supported operations in the simulated hotel.
4. **Environment:** Update the simulated state and return observations.
5. **Observation:** Evaluate the results of the actions.
6. **Goal completion:** Determine whether the requested task has been completed.

The default controller uses deterministic logic. The project structure is designed to allow an LLM-based decision-maker to be added later.

## Project Structure

```text
hotel-management-ai-agent/
├── app.py
├── agent.py
├── environment.py
├── test_agent.py
├── requirements.txt
├── run.bat
├── run.sh
└── README.md
```

## Prerequisites

- Python 3 installed on your computer.
- pip package manager.

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/hotel-management-ai-agent.git
cd hotel-management-ai-agent
```

Replace `YOUR-USERNAME` with your GitHub username.

Alternatively, download the repository as a ZIP file and extract it.

### 2. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 3. Run the Application

```bash
python -m streamlit run app.py
```

Streamlit should open the application in your browser. If it does not, open the local URL printed in the terminal, usually `http://localhost:8501`.

On Windows, you can also try running the provided `run.bat` file.

## Testing

The repository includes a file named `test_agent.py`.

The tests can be run using:

```bash
python -m unittest test_agent.py
```

This command is appropriate if the file uses Python's built-in `unittest` framework. If it uses another testing framework, follow the instructions in the test file.

## Limitations

- All hotel operations are simulated.
- The application does not interact with real hotel systems.
- The default controller is deterministic rather than LLM-driven.
- Real booking, payment, and guest-management integrations are outside the current scope.

## Future Improvements

- Add an LLM-based decision-making component.
- Expand the range of supported hotel management tasks.
- Improve task validation and error handling.
- Add more automated tests.
- Integrate with real hotel systems in a future version, with appropriate security and authorization.

## Learning Outcomes

This project provides an opportunity to explore:

- Python application development.
- Agent-based workflows.
- Tool and environment separation.
- State changes and observations.
- Streamlit application development.
- Automated testing and modular code organization.
