from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_community.vectorstores.faiss import FAISS
from langchain_community.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain.agents import AgentExecutor, create_react_agent
from langchain import hub

from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())  # read local .env file


llm = ChatOpenAI(model="gpt-4-0125-preview")

embeddings_model_name = "sentence-transformers/all-MiniLM-L6-v2"
embeddings = HuggingFaceEmbeddings(model_name=embeddings_model_name)

db = FAISS.load_local(
    "./index",
    embeddings,
    allow_dangerous_deserialization=True,
)
retriever = db.as_retriever(k=1)

from langchain.agents import tool


@tool
def get_balance_by_id(cedula_id: str) -> str:
    """Obtiene balance de la cuenta by cedula_id."""
    import pandas as pd

    df = pd.read_csv("../data/saldos.csv")
    return df[df["ID_Cedula"] == cedula_id]["Balance"].values[0]


@tool
def get_bank_information(question: str) -> str:
    """Obtiene informacion general del banco sobre tramites de cuentas de ahorros, tarjetas de credito y transferencias."""
    bank_info_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        verbose=True,
    )
    response = bank_info_chain.invoke({"query": question})
    return response["result"]


tools = [get_balance_by_id, get_bank_information]


agent = create_react_agent(llm, tools, prompt=hub.pull("hwchase17/react"))
agent_executor = AgentExecutor(agent=agent, tools=tools)


result = agent_executor.invoke({"input": "hi"})

result = agent_executor.invoke(
    {"input": "Como abro una cuenta de ahorros en el banco?"}
)
# result = agent_executor.invoke(
#     {"input": "Como puedo obtener una tarjeta de credito?"},
# )
# result = agent_executor.invoke(
#     {"input": "Cual es el balance de la cuenta de la cedula V-91827364?"}
# )
# result = agent_executor.invoke(
#     {"input": "Cual es el sentido de la vida?"},
# )

print(result["output"])
