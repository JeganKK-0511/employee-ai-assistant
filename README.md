# Employee AI Assistant

An AI-powered employee database assistant built with **Oracle PL/SQL, Python, LangChain, and Ollama**.

The application allows users to ask employee-related questions in natural language. A local Llama 3.2 model identifies the required database operation, Python validates the operation, and Oracle PL/SQL executes the controlled database logic.

## Architecture

```text
User Question
      ↓
LangChain + Llama 3.2
      ↓
Operation + Parameter
      ↓
Python Validation
      ↓
Oracle PL/SQL
      ↓
Employee Database
      ↓
Database Result
      ↓
Llama 3.2
      ↓
Natural Language Answer
```

## Features

- Natural-language employee queries
- Local AI using Ollama and Llama 3.2
- LangChain-based query routing
- Oracle database integration using Python
- Business logic implemented with PL/SQL procedures
- Controlled list of allowed database operations
- AI-generated natural-language responses
- No paid AI API required
- Database credentials stored using environment variables

## Example Questions

The assistant can handle questions such as:

```text
What is the average salary?
```

```text
Who are the top 3 highest paid employees?
```

```text
Show me employees in IT
```

```text
Tell me about employee 104
```

## Supported Operations

The AI router selects one of four controlled operations:

| Operation | Purpose |
|---|---|
| `GET_EMPLOYEE` | Retrieve a specific employee |
| `TOP_EARNERS` | Find the highest-paid employees |
| `SALARY_STATS` | Calculate salary statistics |
| `BY_DEPARTMENT` | Retrieve employees by department |

The application validates the AI-selected operation before executing it.

This prevents the language model from directly generating and executing arbitrary SQL.

## Technology Stack

- **Oracle Database XE**
- **Oracle PL/SQL**
- **Python 3**
- **python-oracledb**
- **LangChain**
- **LangChain Ollama**
- **Ollama**
- **Llama 3.2 3B**

## Project Structure

```text
employee-ai-assistant/
│
├── app.py
├── oracle_db.py
├── requirements.txt
├── .gitignore
└── .env
```

## Oracle PL/SQL Procedures

The project uses stored procedures for database operations:

```text
GET_EMPLOYEE
GET_TOP_EARNERS
GET_SALARY_STATS
GET_EMPLOYEES_BY_DEPARTMENT
```

This keeps database logic inside Oracle while Python handles application and AI integration.

## Installation

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd employee-ai-assistant
```

### 2. Install Python dependencies

```bash
python -m pip install -r requirements.txt
```

### 3. Install Ollama

Install Ollama and download the local model:

```bash
ollama pull llama3.2:3b
```

### 4. Configure Oracle credentials

Create a `.env` file:

```text
ORACLE_USER=ai_app
ORACLE_PASSWORD=your_password
ORACLE_DSN=localhost:1521/XEPDB1
```

Do not commit `.env` to GitHub.

### 5. Run the application

```bash
python app.py
```

## Example Flow

For the question:

```text
What is the average salary?
```

The AI router returns:

```text
SALARY_STATS|NONE
```

Python validates the operation and calls:

```text
GET_SALARY_STATS
```

Oracle returns the salary statistics, and the local Llama model converts the result into a short natural-language response.

## Security Design

The application does **not** allow the LLM to directly execute arbitrary SQL.

Instead, the model chooses from a predefined set of operations:

```text
GET_EMPLOYEE
TOP_EARNERS
SALARY_STATS
BY_DEPARTMENT
```

Python validates the selected operation before calling the corresponding PL/SQL procedure.

This provides a controlled interface between the AI model and the database.

## Future Improvements

Possible future enhancements include:

- Add more employee analytics
- Add conversation history
- Add authentication
- Add structured AI outputs
- Add automated tests
- Add a simple web interface
- Add logging and monitoring

## Author

Built as a portfolio project to demonstrate integration between **Oracle Database, PL/SQL, Python, LangChain, and local LLMs**.