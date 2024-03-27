import logging
import os
import sys
from fastapi import APIRouter,Body, Path, FastAPI, HTTPException
from llama_index.core import (ServiceContext, SimpleDirectoryReader,
                              StorageContext, VectorStoreIndex,
                              load_index_from_storage)
from llama_index.core.node_parser import SimpleNodeParser
import openai
from os import environ as env

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

os.environ['NUMEXPR_MAX_THREADS'] = '4'
os.environ['NUMEXPR_NUM_THREADS'] = '2'

# key is from SUST team
os.environ["OPENAI_API_KEY"] = env['OPENAI_API_KEY']
openai.api_key = env['OPENAI_API_KEY']

router = APIRouter()

chat_engines = {}

@router.post("/ask")
async def ask_question(question: str = Body(...)):

    node_parser = SimpleNodeParser(
        separator=" ", 
        chunk_size=512, 
        chunk_overlap=20
    )

    service_context = ServiceContext.from_defaults(node_parser=node_parser, system_prompt="You are a customer service representative for a Bank loan named Mellisa. A customer asks you a question. Answer the question from the given context only, do not provide additional information.")

    try:
        storage_context = StorageContext.from_defaults(persist_dir='storage/cache/faq')
        index = load_index_from_storage(storage_context)
        print('loading from disk')
    except:
        documents = SimpleDirectoryReader(input_files=["files/others/FAQ1.pdf"]).load_data()
        index = VectorStoreIndex.from_documents(documents, service_context=service_context)
        index.storage_context.persist(persist_dir='storage/cache/faq')
        print("Reading from file")

    response = index.as_query_engine().query(question)
    return {"data": response.response}


# def create_chat_engine(indexStorage: any):
#     global chat_engines
#     chat_id = str(uuid.uuid4()) 

#     memory = ChatMemoryBuffer.from_defaults(token_limit=2000)

#     chat_engine = indexStorage.as_chat_engine(
#         chat_mode="context",
#         memory=memory,
#         system_prompt=(
#             "You are a chatbot, able to have normal interactions, as well as talk"
#             # " about an essay discussing Paul Grahams life."
#         ),
#     )

#     chat_engines[chat_id] = chat_engine

#     return chat_id



# @router.post("/create_chat")
# async def create_chat(transcript_id: str):

#     if not transcript_id:
#         raise HTTPException(status_code=400, detail="transcript_id is required")
#     transcription = transcript_collection.find_one(ObjectId(transcript_id))
#     if not transcription:
#         raise HTTPException(status_code=404, detail="Chat not found")

#     transcription["_id"] = str(transcription["_id"])

#     index = create_index_and_query(transcript_id, transcription["transcription"])
    
#     chat_id = create_chat_engine(index)

#     return {"chat_id": chat_id, "transcript_id": transcript_id}


# @router.post('/history_chat')
# async def history_chat(payload: Agent2QuestionRequest):
#     global chat_engines

#     if not payload.chat_id:
#         raise HTTPException(status_code=400, detail="Chat ID is required")

#     # Check if the chat engine is already loaded
#     if payload.chat_id not in chat_engines:
#         return 'Chat not found'
    
#     response = chat_engines[payload.chat_id].chat(payload.question)

#     return response
