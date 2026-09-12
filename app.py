from oracle_db import get_connection
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate


# -----------------------------
# 1. Local AI
# -----------------------------
llm = ChatOllama(
    model="llama3.2:3b",
    temperature=0
)


# -----------------------------
# 2. AI Router
# -----------------------------
prompt = ChatPromptTemplate.from_template("""
You route employee database questions.

Return EXACTLY this format:

OPERATION|PARAMETER

Allowed operations:

GET_EMPLOYEE
TOP_EARNERS
SALARY_STATS
BY_DEPARTMENT

Rules:

- Specific employee question
  -> GET_EMPLOYEE|employee_id

- Top/highest paid employees
  -> TOP_EARNERS|number

- Average/minimum/maximum/overall salary statistics
  -> SALARY_STATS|NONE

- Employees in a department
  -> BY_DEPARTMENT|department

Examples:

"Tell me about employee 104"
GET_EMPLOYEE|104

"Who are the top 3 highest paid employees?"
TOP_EARNERS|3

"Show me employees in IT"
BY_DEPARTMENT|IT

"What is the average salary?"
SALARY_STATS|NONE

Return ONLY the operation and parameter.

User question:
{question}
""")

chain = prompt | llm


# -----------------------------
# 3. Read Oracle DBMS_OUTPUT
# -----------------------------
def read_db_output(cursor):
    while True:
        line_var = cursor.var(str)
        status_var = cursor.var(int)

        cursor.callproc(
            "dbms_output.get_line",
            [line_var, status_var]
        )

        status = status_var.getvalue()

        if status != 0:
            break

        print(line_var.getvalue())


# -----------------------------
# 4. Ask user
# -----------------------------
question = input("Ask a question: ")

response = chain.invoke({
    "question": question
})

result = response.content.strip()

print("\nAI decision:", result)


# -----------------------------
# 5. Extract operation + parameter
# -----------------------------
try:
    operation, parameter = result.split("|", 1)

    operation = operation.strip().replace("`", "")
    parameter = parameter.strip().replace("`", "")

except ValueError:
    print("AI returned an invalid format.")
    exit()


# -----------------------------
# 6. Validate operation
# -----------------------------
allowed_operations = {
    "GET_EMPLOYEE",
    "TOP_EARNERS",
    "SALARY_STATS",
    "BY_DEPARTMENT"
}

if operation not in allowed_operations:
    print("Invalid operation:", operation)
    exit()


# -----------------------------
# 7. Connect to Oracle
# -----------------------------
connection = get_connection()

cursor = connection.cursor()

cursor.callproc("dbms_output.enable")


# -----------------------------
# 8. Execute PL/SQL
# -----------------------------
if operation == "SALARY_STATS":

    cursor.callproc("get_salary_stats")


elif operation == "TOP_EARNERS":

    try:
        limit = int(parameter)
    except ValueError:
        limit = 3

    cursor.callproc(
        "get_top_earners",
        [limit]
    )


elif operation == "GET_EMPLOYEE":

    try:
        employee_id = int(parameter)
    except ValueError:
        print("Invalid employee ID.")
        cursor.close()
        connection.close()
        exit()

    cursor.callproc(
        "get_employee",
        [employee_id]
    )


elif operation == "BY_DEPARTMENT":

    department = parameter.upper()

    cursor.callproc(
        "get_employees_by_department",
        [department]
    )


# -----------------------------
# 9. Display Oracle result
# -----------------------------
print("\nOracle result:")
print("-" * 40)

# Capture Oracle output
oracle_lines = []

while True:
    line_var = cursor.var(str)
    status_var = cursor.var(int)

    cursor.callproc(
        "dbms_output.get_line",
        [line_var, status_var]
    )

    status = status_var.getvalue()

    if status != 0:
        break

    oracle_lines.append(line_var.getvalue())

oracle_result = "\n".join(oracle_lines)

print(oracle_result)


# -----------------------------
# AI explains the Oracle result
# -----------------------------
summary_prompt = ChatPromptTemplate.from_template("""
You are an assistant explaining database results to a user.

User question:
{question}

Database result:
{result}

Give a short, clear answer to the user.

Do not invent any information.
Only use the database result.
Do not mention Python, LangChain, Oracle, or internal processing.

Answer naturally in 1-3 sentences.
""")

summary_chain = summary_prompt | llm

summary = summary_chain.invoke({
    "question": question,
    "result": oracle_result
})

print("\nAI answer:")
print(summary.content.strip())


# -----------------------------
# 10. Close connection
# -----------------------------
cursor.close()
connection.close()