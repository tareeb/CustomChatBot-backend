from langchain_community.document_loaders import PyPDFium2Loader
from langchain_groq import ChatGroq


from utils.config import config_embeddings, models

import os
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from django.conf import settings
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain.retrievers.contextual_compression import ContextualCompressionRetriever
from langchain_cohere import CohereRerank
import pypdfium2 as pdfium
from langchain_core.documents import Document
from langchain_openai import AzureOpenAIEmbeddings
from langchain_core.runnables import ConfigurableFieldSpec

from langchain_community.vectorstores import Neo4jVector
from langchain.text_splitter import TokenTextSplitter

from langchain_openai import AzureChatOpenAI
from utils.config import models, config_embeddings

from utils.GraphConnection import Neo4jConnection

class Neo4jPipeline:
    def __init__(self):
        try:
            self.client = Neo4jConnection.get_neo4j_connection()
            if not self.client:
                raise Exception("Failed to connect to Neo4j")
        except Exception as e:
            raise Exception(f"Failed to connect to Neo4j")

    def chunking(self, document):

        pdf = pdfium.PdfDocument(document)
        docs = []
        for x in range(len(pdf)):
            content = pdf[x].get_textpage().get_text_range()
            metadata = {"page": x + 1}
            doc = Document(page_content=content, metadata=metadata)
            docs.append(doc)

        parent_splitter = TokenTextSplitter(chunk_size=1000, chunk_overlap=300)
        child_splitter = TokenTextSplitter(chunk_size=300, chunk_overlap=90)
        parent_documents = parent_splitter.split_documents(docs)

        return (parent_documents, child_splitter)

    def save_embeddings(self, docs, chatbotname, documentname):
        graph = self.client
        parent_documents, child_splitter = self.chunking(docs)

        for parent in parent_documents:
            child_documents = child_splitter.split_documents([parent])
            params = {
                "parent": parent.page_content,
                "children": [c.page_content for c in child_documents],
                "chatbotname": chatbotname,
                "documentname": documentname,
            }

            graph.query(
                """
            CREATE (p:Parent {text: $parent , chatbotname: $chatbotname , documentname: $documentname})
            WITH p
            UNWIND $children AS child
            
            CREATE (c:Child {text: child, chatbotname: $chatbotname , documentname: $documentname})
            CREATE (c)-[:HAS_PARENT]->(p)
            """,
                params,
            )

        embeddings = AzureOpenAIEmbeddings(
                openai_api_key=os.environ.get("OPENAI_AZURE_API_KEY"),
                azure_endpoint=config_embeddings["text-embedding-3-large"]["endpoint"],
                deployment=config_embeddings["text-embedding-3-large"]["model_name"],
                openai_api_type="azure",
        )

        embedding_dimension = 3072

        Neo4jVector.from_existing_graph(
            embeddings,
            url=os.environ.get("NEO4J_URL"),
            username="neo4j",
            password=os.environ.get("NEO4J_PASSWORD"),
            index_name=chatbotname,
            node_label="Child",
            text_node_properties=["text"],
            embedding_node_property="embedding",
        )

    def get_llm(self):
        # llm = AzureChatOpenAI(
        #     openai_api_key=os.environ["OPENAI_AZURE_API_KEY_3"],
        #     azure_endpoint=models["gpt-4-1106-azure-3"]["endpoint"],
        #     openai_api_version="2023-07-01-preview",
        #     deployment_name="gpt-4-1106-Preview-Azure",
        #     # model=" gpt-4-1106-Preview-Azure",
        #     openai_api_type="azure",
        # )
        llm = ChatGroq(
            temperature=0,
            groq_api_key=os.environ["GROQ_API_KEY"],
            model_name=models["GROQ"]["model_name2"],
        )
        return llm

    def get_retriever(self, chatbotname):
        embeddings = AzureOpenAIEmbeddings(
            openai_api_key=os.environ.get("OPENAI_AZURE_API_KEY"),
            azure_endpoint=config_embeddings["text-embedding-3-large"]["endpoint"],
            deployment=config_embeddings["text-embedding-3-large"]["model_name"],
            openai_api_type="azure",
        )

        retrieval_query = """
        MATCH (node)-[:HAS_PARENT]->(parent)
        WITH parent, MAX(node.score) AS score
        WHERE parent.chatbotname = '{chatbotname}'
        RETURN parent.text AS text, score , {{}} AS metadata
        """.format(
            chatbotname=chatbotname
        )

        vectorstore = Neo4jVector.from_existing_index(
            embeddings,
            url=os.environ.get("NEO4J_URL"),
            username="neo4j",
            password=os.environ.get("NEO4J_PASSWORD"),
            index_name=chatbotname,
            node_label="Child",
            embedding_node_property="embedding",
            retrieval_query=retrieval_query,
        )
        retriever = vectorstore.as_retriever()

        retriever_from_llm = MultiQueryRetriever.from_llm(
            retriever=retriever, llm=self.get_llm()
        )

        compressor = CohereRerank(cohere_api_key=os.environ["COHERE_KEY"])

        compression_retriever = ContextualCompressionRetriever(
            base_compressor=compressor, base_retriever=retriever_from_llm
        )

        return compression_retriever

    def generate_history_chat_response(self, query, request, chatbotname, prompt):
        retriever = self.get_retriever(chatbotname)
        llm = self.get_llm()

        contextualize_q_system_prompt = """Given a chat history and the latest user question 
        which might reference context in the chat history, formulate a standalone 
        question which can be understood without the chat history. \
        Do NOT answer the question of the user. \
        Just reformulate the question if it is refrencing chat history otherwise return the question as it is."""

        contextualize_q_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", contextualize_q_system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ]
        )
        history_aware_retriever = create_history_aware_retriever(
            llm, retriever, contextualize_q_prompt
        )

        if prompt != "":
            qa_system_prompt2 = f"""{prompt}{{context}}"""
        else:
            qa_system_prompt = """You are an assistant for question-answering tasks. 
                Use the following pieces of retrieved context to answer the question. \
                You must generate answer to user query only using the retrieved context. \
                If the given context doesn't contain the information
                inform the user politely that you lack information
                and suggest contacting support at support@gmail.com \
                keep the Answer concise , be supportive.
            {context}"""

        qa_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", qa_system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ]
        )
        question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)

        rag_chain = create_retrieval_chain(
            history_aware_retriever, question_answer_chain
        )

        def get_session_history(
            session_id: str, chatbot_name: str
        ) -> BaseChatMessageHistory:

            key = f"{session_id}_{chatbot_name}"

            if key not in settings.ADVANCE_STORE:
                settings.ADVANCE_STORE[key] = ChatMessageHistory()

            return settings.ADVANCE_STORE[key]

        conversational_rag_chain = RunnableWithMessageHistory(
            rag_chain,
            get_session_history,
            input_messages_key="input",
            history_messages_key="chat_history",
            output_messages_key="answer",
            history_factory_config=[
                ConfigurableFieldSpec(
                    id="session_id",
                    annotation=str,
                    name="Session ID",
                    description="Unique identifier for the user session",
                    default="",
                    is_shared=True,
                ),
                ConfigurableFieldSpec(
                    id="chatbot_name",
                    annotation=str,
                    name="Chatbot Name",
                    description="Unique identifier of chatbot User is Using",
                    default="",
                    is_shared=True,
                ),
            ],
        )

        result = conversational_rag_chain.invoke(
            {"input": query},
            config={
                "configurable": {
                    "session_id": request.session.session_key,
                    "chatbot_name": chatbotname,
                }
            },  # constructs a key "abc123" in `store`.
        )["answer"]

        return result

    def save_embeddings_pipeline(self, docs, chatbotname, documentname):
        self.save_embeddings(docs, chatbotname, documentname)
        return

    def deleteAdvanceChatbot(self, chatbotname):
        try:
            graph = self.client
            params = {"chatbotname": chatbotname}

            graph.query(
                """
                MATCH (c: Child {chatbotname: $chatbotname})-[r:HAS_PARENT]->(p:Parent {chatbotname: $chatbotname})
                DELETE c, r , p
                """,
                params,
            )

            return

        except Exception as e:
            raise e.args[0]

    def deleteAdvanceDocument(self, chatbotname, documentname):
        try:
            graph = self.client
            params = {
                "chatbotname": chatbotname,
                "documentname": documentname,
            }

            graph.query(
                """
                MATCH (c: Child {chatbotname: $chatbotname , documentname : $documentname})-[r:HAS_PARENT]->(p:Parent {chatbotname: $chatbotname , documentname : $documentname})
                DELETE c, r , p
                """,
                params,
            )

            return

        except Exception as e:
            raise e.args[0]
