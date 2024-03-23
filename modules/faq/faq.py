import logging
import os
import sys
from fastapi import APIRouter,Body, Path
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



