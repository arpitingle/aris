from langchain_community.chat_models import ChatOllama
from langchain.schema.output_parser import StrOutputParser
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema.runnable import RunnablePassthrough
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

class ChatBot:
    def __init__(self, model_name: str = "mistral", temperature: float = 0.7):
        self.model = ChatOllama(model=model_name, temperature=temperature)
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=100)
        self.memory = ConversationBufferMemory()
        self.conversation = ConversationChain(
            llm=self.model,
            memory=self.memory,
            prompt=PromptTemplate.from_template(
                """
                The following is a friendly conversation between a Human and an AI assistant named Claude. Claude is helpful, creative, clever, and very friendly.

                Current conversation:
                {history}
                Human: {input}
                Claude: """
            ),
            verbose=True
        )

    async def ask_async(self, query: str) -> str:
        try:
            return await self.conversation.arun(input=query)
        except Exception as e:
            return f"An error occurred: {str(e)}"

    def ask(self, query: str) -> str:
        try:
            return self.conversation.run(input=query)
        except Exception as e:
            return f"An error occurred: {str(e)}"

    def clear(self) -> None:
        self.memory.clear()