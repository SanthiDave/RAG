import base64
from datetime import datetime, timedelta
import io  # Provides the Python interfaces to stream handling
import httpx
import itertools
import os  # Provides functions for interabasecting with the operating system
import mimetypes  # Map filenames to MIME types
import pickle
import queue  # Provides the Python queue, a kind of multi-producer, multi-consumer queue
import time  # Provides various time-related functions
import logging  # Provides a flexible framework for emitting log messages from Python programs
from uuid import uuid4
# from quart_cors import cors
import quart  # Provides the UUID objects according to RFC 4122
import openai  # Provides the OpenAI API
import openai  # Provides the OpenAI API
import nltk  
import subprocess  # Allows you to spawn new processes, connect to their input/output/error pipes, and obtain their return codes
import aiofiles  # Provides support for file-related I/O using async and await
from datetime import datetime, timedelta  # Provides classes for manipulating dates and times
from urllib.parse import urlparse
import mimetypes
from helper.fileReader import process_docs_usecase
from werkzeug.datastructures import FileStorage
import ast  


from urllib.parse import urlparse,unquote
# from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler  # Specific import from langchain package
from langchain_community.document_loaders import (
    CSVLoader,
    TextLoader,
    UnstructuredWordDocumentLoader,
    UnstructuredExcelLoader,
    PyPDFLoader,
    UnstructuredPowerPointLoader,
)  # Specific imports from langchain_community package
from langchain.chat_models import AzureChatOpenAI  # Specific import from langchain package
from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage
)  # Specific imports from langchain package
#import pyodbc  # Provides the Python DB API 2.0 interface to ODBC
# from flask import Flask, Response, request, jsonify, redirect, session, abort, make_response, stream_with_context, url_for  # Provides the Flask web framework and its utilities
# from flask_session import Session  # Provides server-side session support for Flask
import json  # Provides JSON encoder and decoder
from functools import wraps  # Provides a decorator for wrapping a function
import mimetypes  # Map filenames to MIME types
import traceback  # Provides functions to extract, format and print stack traces of Python programs
from contextlib import redirect_stderr, redirect_stdout  # Provides utilities for common tasks involving the with statement
from flask_socketio import SocketIO, send, join_room, leave_room  # Provides Flask support for Socket.IO real-time communication
from helper.brazil_jurisdiction_dynamic_reports import Brazil_Jurisdiction  # Specific import from helper package
from helper.menu_data import get_menu_items, get_usecase_data, validate_API_key,get_usecase_params  # Specific imports from helper package
import asyncio  # Provides infrastructure for writing single-threaded concurrent code using coroutines
from azure.identity import DefaultAzureCredential,ClientSecretCredential  # Provides Azure Identity client library
# from azure.search.documents import SearchClient
from azure.search.documents.aio import SearchClient
# Provides Azure Search client library
# from azure.search.documents.indexes import SearchIndexClient,SearchIndex, SimpleField, SearchableField, DataSource
# from azure.search.documents.indexes.models import SearchIndexer
from helper.doc_processing import DocProcessing  # Specific import from helper package
from helper.fileSession import FileSystemSessionInterface
# Importing various approaches for handling different tasks
from approaches.retrievethenread import RetrieveThenReadApproach
from approaches.readretrieveread import ReadRetrieveReadApproach
from approaches.readdecomposeask import ReadDecomposeAsk
from approaches.Old.chatreadretrieveread import ChatReadRetrieveReadApproach
from approaches.chatreadretrieveread_LC import ChatReadRetrieveReadApproach_LC
from approaches.usecaseReadRetrieveRead import UsecaseReadRetrieveReadApproach
from approaches.Old.usecaseChatReadRetrieveRead import UsecaseChatReadRetrieveReadApproach
from approaches.legalusecaseChatReadRetrieveRead_LC import legalusecaseChatReadRetrieveRead_LC
from approaches.usecaseChatReadRetrieveRead_LC import UsecaseChatReadRetrieveReadApproach_LC
from approaches.ragasDataRetirve import SQLTableManager
from approaches.chatPureReadRetrieveRead import ChatPureReadRetrieveReadApproach
from approaches.ChatVisionRetrieveReadApproach import ChatVisionRetrieveReadApproach
from approaches.ragasDataRetirve import SQLTableManager
from approaches.ragasEvalutationTest import ragasEvaluation

from approaches.dalleImageReadRetrieveRead import DalleImageReadRetrieveReadApproach
from approaches.bingsearchReadRetrive import BingSearchReadRetrive
from approaches.Legal_agent_usecase import LangChainAgent
from approaches.ragasEvalutationTest import ragasEvaluation
from approaches.talktodocument import question_on_doc
from azure.storage.blob import BlobServiceClient
from azure.core.credentials import AzureKeyCredential
import configparser

from azure.identity._internal.user_agent import USER_AGENT
from azure.identity import InteractiveBrowserCredential
import requests
from msal import ConfidentialClientApplication

from azure.cosmos import CosmosClient, PartitionKey

# File and IO
from quart import (Quart, session,Response,Request,Blueprint, abort, send_from_directory, jsonify, make_response, redirect,
                   request, stream_with_context, url_for)


# Set up config parser and read ini configuration file
config = configparser.ConfigParser()
config.read('config.ini')
nltk.download('punkt')  



# Assigning configuration values to variables from config.ini
AZURE_STORAGE_ACCOUNT = config['DEFAULT']['AZURE_STORAGE_ACCOUNT']
AZURE_STORAGE_CONTAINER = config['DEFAULT']['AZURE_STORAGE_CONTAINER']
ARTIFACTS_STORAGE_ACCOUNT = config['DEFAULT']['AZURE_STORAGE_ACCOUNT_ARTIFACTS']
ARTIFACTS_STORAGE_KEY = config['DEFAULT']['AZURE_STORAGE_KEY_ARTIFACTS']
AZURE_SEARCH_SERVICE = config['DEFAULT']['AZURE_SEARCH_SERVICE']
AZURE_SEARCH_INDEX = config['DEFAULT']['AZURE_SEARCH_INDEX']
AZURE_OPENAI_SERVICE = config['DEFAULT']['AZURE_OPENAI_SERVICE']
# AZURE_Dalle3_SERVICE = config['DEFAULT']['AZURE_Dalle3_SERVICE']

AZURE_OPENAI_GPT_DEPLOYMENT = config['DEFAULT']['AZURE_OPENAI_GPT_DEPLOYMENT']
AZURE_OPENAI_CHATGPT_DEPLOYMENT = config['DEFAULT']['AZURE_OPENAI_CHATGPT_DEPLOYMENT']
AZURE_OPENAI_CHATGPT_PLUS_DEPLOYMENT = config['DEFAULT']['AZURE_OPENAI_CHATGPT_PLUS_DEPLOYMENT']
AZURE_OPENAI_CHATGPT_O_DEPLOYMENT = config['DEFAULT']['AZURE_OPENAI_CHATGPT_O_DEPLOYMENT']
AZURE_OPENAI_CHATGPT_O_API_VERSION = config['DEFAULT']['AZURE_OPENAI_CHATGPT_O_API_VERSION']
AZURE_FORM_RECOGNIZER_SERVICE = config['DEFAULT']['AZURE_FORM_RECOGNIZER_SERVICE']
AZURE_FORM_RECOGNIZER_KEY = config['DEFAULT']['AZURE_FORM_RECOGNIZER_KEY']

KB_FIELDS_CONTENT = config['DEFAULT']['KB_FIELDS_CONTENT']
KB_FIELDS_CATEGORY = config['DEFAULT']['KB_FIELDS_CATEGORY']
KB_FIELDS_SOURCEPAGE = config['DEFAULT']['KB_FIELDS_SOURCEPAGE']
WHISPER_API_ENDPOINT = config['DEFAULT']['WHISPER_API_ENDPOINT']
WHISPER_API_KEY = config['DEFAULT']['WHISPER_API_KEY']
WHISPER_DEPLOYMENT_NAME = config['DEFAULT']['WHISPER_DEPLOYMENT_NAME']

# For the API keys (again, be cautious with sensitive data in plain-text files):
OPENAI_API_KEY = config['DEFAULT']['OPENAI_API_KEY']
GPTO_OPENAI_API_KEY = config['DEFAULT']['GPTO_OPENAI_API_KEY']
GPT4VISION_ENDPOINT=  config['DEFAULT']['GPT4VISION_ENDPOINT']
GPT4VISION_KEY=  config['DEFAULT']['GPT4VISION_KEY']

GPT4o_VISION_ENDPOINT = config['DEFAULT']['GPT4o_VISION_ENDPOINT']
GPT4o_VISION_KEY = config['DEFAULT']['GPT4o_VISION_KEY']

Dalle_api_endpoint = config['DEFAULT']['Dalle_api_endpoint']
Dalle_api_key = config['DEFAULT']['Dalle_api_key']
Dalle_deployment = config['DEFAULT']['Dalle_deployment']
BING_SEARCH_ENDPOINT = f""
BING_SUBSCRIPTION_KEY = config['DEFAULT']['BING_SUBSCRIPTION_KEY']

SEARCH_API_KEY = config['DEFAULT']['SEARCH_API_KEY']
STORAGE_API_KEY = config['DEFAULT']['STORAGE_API_KEY']

CLIENT_ID = config['DEFAULT']['CLIENT_ID']
CLIENT_SECRET = config['DEFAULT']['CLIENT_SECRET']

TENANT_ID = config['DEFAULT']['TENANT_ID']
APP_BASE = config['DEFAULT']['APP_BASE']
REDIRECT_URI = config['DEFAULT']['REDIRECT_URI']
AZURE_OPENAI_SERVICE_GPTO = config['DEFAULT']['AZURE_OPENAI_SERVICE_GPTO']
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
REDIRECT_URI = f"https://{REDIRECT_URI}/.auth/login/aad/callback"


print("config['DEFAULT']['REDIRECT_URI']=======>",config['DEFAULT']['REDIRECT_URI'])
LOGOUT_REDIRECT_URI = f"https://{config['DEFAULT']['REDIRECT_URI']}/"

# Microsoft Graph API configuration
GRAPH_API_ENDPOINT = ""
GRAPH_GROUP_ENDPOINT = ""
GRAPH_Property_ENDPOINT= ""

# Initialize user token and user info as None and empty dictionary respectively
AD_USER_TOKEN = None
AD_USER_INFO = {}

# Create a ConfidentialClientApplication instance for Azure AD authentication
PCApp = ConfidentialClientApplication(
        client_id=CLIENT_ID,
        client_credential=CLIENT_SECRET,
        authority=AUTHORITY,
        exclude_scopes = ["offline_access"]
    )


# Start of Cosmos DB connections
COSMOSDB_SERVICE = config['DEFAULT']['COSMOSDB_SERVICE']  # Cosmos DB service name
COSMOSDB_URI = f""  # Cosmos DB URI
COSMOSDB_PRIMEKEY = config['DEFAULT']['COSMOSDB_PRIMEKEY']  # Cosmos DB primary key
COSMOSDB_CONSTR = f"AccountEndpoint={COSMOSDB_URI};AccountKey={COSMOSDB_PRIMEKEY};"  # Cosmos DB connection string
COSMOSDB_DATABASE_NAME = "geagptlogs"  # Cosmos DB database name
COSMOSDB_CONTAINER_NAME = "chatlogs"  # Cosmos DB container name for chat logs
COSMOSDB_THREAD_CONTAINER_NAME = "threadlogs"  # Cosmos DB container name for thread logs
COSMOSDB_LEGALCHAT_CONTAINER_NAME = "legalchat"  # Cosmos DB container name for legal chat
COSMOSDB_DocContent_CONTAINER_NAME = "document_content"
document_content_key_path = PartitionKey(path="/session_document_key")

# Print the base app and client ID for debugging purposes
print("APP_BASE:", APP_BASE)
print("CLIENT_ID:", CLIENT_ID)
print("ARTIFACTS_STORAGE_ACCOUNT::",ARTIFACTS_STORAGE_ACCOUNT)
print("AZURE_STORAGE_KEY_ARTIFACTS::",ARTIFACTS_STORAGE_KEY)

# Create a CosmosClient instance
cosdb_client = CosmosClient(url=COSMOSDB_URI, credential=COSMOSDB_PRIMEKEY)

# Create the database if it does not exist
database = cosdb_client.create_database_if_not_exists(id=COSMOSDB_DATABASE_NAME)

# Define partition keys for different containers
key_path = PartitionKey(path="/chat_session_id")
thread_key_path = PartitionKey(path="/user_id")
legalchat_key_path = PartitionKey(path="/legal_team")

# Create the containers if they do not exist
container = database.create_container_if_not_exists(
    id=COSMOSDB_CONTAINER_NAME, partition_key=key_path, offer_throughput=400
)
thread_container = database.create_container_if_not_exists(
    id=COSMOSDB_THREAD_CONTAINER_NAME, partition_key=thread_key_path, offer_throughput=400
)
legalchat_container = database.create_container_if_not_exists(
    id=COSMOSDB_LEGALCHAT_CONTAINER_NAME, partition_key=legalchat_key_path, offer_throughput=400
)

document_content_container = database.create_container_if_not_exists(
    id=COSMOSDB_DocContent_CONTAINER_NAME, partition_key=document_content_key_path, offer_throughput=400
)



# Use the current user identity to authenticate with Azure OpenAI, Cognitive Search and Blob Storage (no secrets needed,
# just use 'az login' locally, and managed identity when deployed on Azure). If you need to use keys, use separate AzureKeyCredential instances with the
# keys for each service
# If you encounter a blocking error during a DefaultAzureCredntial resolution, you can exclude the problematic credential by using a parameter (ex. exclude_shared_token_cache_credential=True)

# Used by the OpenAI SDK
# Set the OpenAI to Azure
openai.api_type = "azure"
openai.api_base = f""
openai.api_version = "2023-03-15-preview"
openai.api_key = OPENAI_API_KEY
openai.gpto_api_base = f""
openai.gpto_api_key = ""


#Start Brought here from PrepDocs.py
# temparaykeys#
search_creds = AzureKeyCredential(SEARCH_API_KEY)

#End Brought here from PrepDocs.py

# Set up clients for Cognitive Search and Storage
search_client = SearchClient(
    endpoint=f"",
    index_name=,
    credential=)

# Create a BlobServiceClient instance for Azure Storage
blob_client = BlobServiceClient(
    account_url=f"",
    credential=)


blob_service_client = BlobServiceClient(
    account_url=f"",
    credential=)


# Get a container client for the specified Azure Storage container
blob_container = blob_client.get_container_client()

# SQL server configuration
SQL_SERVER = config['DEFAULT']['SQL_SERVER']
SQL_DATABASE = config['DEFAULT']['SQL_DATABASE']
SQL_USER = config['DEFAULT']['SQL_USERNAME']
SQL_PASSWORD = config['DEFAULT']['SQL_PASSWORD']

# Create a queue for streaming logs
stream_logs_queue = queue.Queue()

# Create a Brazil_Jurisdiction instance with the SQL server configuration
brazil_jurisdiction = Brazil_Jurisdiction(SQL_SERVER, SQL_DATABASE, SQL_USER, SQL_PASSWORD)
# Various approaches to integrate GPT and external knowledge, most applications will use a single one of these patterns
# or some derivative, here we include several for exploration purposes
ask_approaches = {
    "rtr": RetrieveThenReadApproach(AZURE_OPENAI_CHATGPT_O_DEPLOYMENT,AZURE_OPENAI_CHATGPT_O_API_VERSION, KB_FIELDS_SOURCEPAGE, KB_FIELDS_CONTENT),
    "rrr": ReadRetrieveReadApproach(search_client, AZURE_OPENAI_GPT_DEPLOYMENT, KB_FIELDS_SOURCEPAGE, KB_FIELDS_CONTENT),
    "rda": ReadDecomposeAsk(search_client, AZURE_OPENAI_GPT_DEPLOYMENT, KB_FIELDS_SOURCEPAGE, KB_FIELDS_CONTENT)
}
talk_approaches = {}
chat_approaches = {
    "rrr_old": ChatReadRetrieveReadApproach(search_client, AZURE_OPENAI_CHATGPT_DEPLOYMENT, AZURE_OPENAI_GPT_DEPLOYMENT, KB_FIELDS_SOURCEPAGE, KB_FIELDS_CONTENT),
    "prrr": ChatPureReadRetrieveReadApproach(AZURE_OPENAI_CHATGPT_DEPLOYMENT, AZURE_OPENAI_CHATGPT_PLUS_DEPLOYMENT, AZURE_OPENAI_GPT_DEPLOYMENT),
#    "rrr":   ChatReadRetrieveReadApproach_LC(AZURE_OPENAI_CHATGPT_O_DEPLOYMENT,AZURE_OPENAI_CHATGPT_O_API_VERSION, KB_FIELDS_SOURCEPAGE, KB_FIELDS_CONTENT),
    "orrr": ChatPureReadRetrieveReadApproach(AZURE_OPENAI_CHATGPT_DEPLOYMENT, AZURE_OPENAI_CHATGPT_PLUS_DEPLOYMENT, AZURE_OPENAI_GPT_DEPLOYMENT),
    "vrrr": ChatVisionRetrieveReadApproach(AZURE_OPENAI_CHATGPT_DEPLOYMENT, AZURE_OPENAI_CHATGPT_PLUS_DEPLOYMENT, AZURE_OPENAI_GPT_DEPLOYMENT)
}

usecase_approaches = {
    "rrr": UsecaseReadRetrieveReadApproach(search_client, AZURE_OPENAI_CHATGPT_DEPLOYMENT, AZURE_OPENAI_GPT_DEPLOYMENT, KB_FIELDS_SOURCEPAGE, KB_FIELDS_CONTENT),
    "crrr_old": UsecaseChatReadRetrieveReadApproach(search_client, AZURE_OPENAI_CHATGPT_DEPLOYMENT, AZURE_OPENAI_GPT_DEPLOYMENT, KB_FIELDS_SOURCEPAGE, KB_FIELDS_CONTENT),
    #"crrr": UsecaseChatReadRetrieveReadApproach_LC(AZURE_OPENAI_CHATGPT_O_DEPLOYMENT,AZURE_OPENAI_CHATGPT_O_API_VERSION, KB_FIELDS_SOURCEPAGE, KB_FIELDS_CONTENT),
    #"crrr":UsecaseChatReadRetrieveReadApproach_LC(search_client, AZURE_OPENAI_CHATGPT_DEPLOYMENT, AZURE_OPENAI_CHATGPT_PLUS_DEPLOYMENT, AZURE_OPENAI_GPT_DEPLOYMENT, KB_FIELDS_SOURCEPAGE, KB_FIELDS_CONTENT),
    # "lrrr":legalusecaseChatReadRetrieveRead_LC(AZURE_OPENAI_CHATGPT_O_DEPLOYMENT,AZURE_OPENAI_CHATGPT_O_API_VERSION, KB_FIELDS_SOURCEPAGE, KB_FIELDS_CONTENT)

}

image_approaches = {
    "drrr": DalleImageReadRetrieveReadApproach(AZURE_OPENAI_CHATGPT_DEPLOYMENT, AZURE_OPENAI_GPT_DEPLOYMENT,Dalle_api_endpoint,Dalle_api_key)

}

sql_table_manager = SQLTableManager(config)
ragasEvaluation = ragasEvaluation(config, search_client, AZURE_OPENAI_CHATGPT_DEPLOYMENT, AZURE_OPENAI_CHATGPT_PLUS_DEPLOYMENT, KB_FIELDS_SOURCEPAGE, KB_FIELDS_CONTENT,AZURE_SEARCH_SERVICE,AZURE_SEARCH_INDEX,SEARCH_API_KEY,AZURE_OPENAI_SERVICE,AZURE_OPENAI_CHATGPT_O_API_VERSION)

app = Quart(__name__)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB
bp = Blueprint("routes", __name__, static_folder='static')

app.config['SECRET_KEY'] = ''
app.secret_key = ''
app.config['SESSION_COOKIE_NAME'] = 'test'
app.session_interface = FileSystemSessionInterface(session_dir='flask_session')
# Set the session timeout to 10 minutes (600 seconds)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=59)


# Initialize Flask-Session for the app
# Session(app)
queues = {}
# Create a DefaultAzureCredential instance for Azure authentication
auth_credential = DefaultAzureCredential()
# Define a route for serving static files
# @app.route("/", defaults={"path": "index.html"})


@app.before_request  
async def before_request():  
    # Placeholder for any logic you might want to execute before each request  
    pass  


@app.after_request  
async def set_security_headers(response: Response):  
    # Prevents the webpage from being displayed in a frame, iframe, or object  
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'  
    # Enables the Cross-Site Scripting (XSS) filter in the browser and instructs it to block the page if an attack is detected  
    response.headers['X-XSS-Protection'] = '1; mode=block'  
    # Enforces the use of HTTPS. The max-age is set to 1 year (31536000 seconds), includes all subdomains, and is eligible for HSTS preloading  
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains; preload'  
    # Defines the Content Security Policy (CSP) to specify which resources can be loaded by the browser  
    csp_header = (  
        # "default-src 'self'; "  # Only allows resources from the same origin  
        # "img-src 'self' data:; "  # Allows images from the same origin and data URLs  
        "style-src 'self' 'unsafe-inline'; "  # Allows styles from the same origin and inline styles  
        "font-src 'self' data: https://res-1.cdn.office.net https://*.azureedge.net;"  # Allows fonts from the same origin, data URLs, and specified CDNs  
    )  
    response.headers['Content-Security-Policy'] = csp_header  
    return response 


@app.route("/")
async def index():
    response = await make_response(await app.send_static_file('index.html'))
    if 'AD_USER_INFO' not in session:
        print("AD_USER_INFO user inside index path=====>",AD_USER_INFO)
        response.set_cookie('isUserLoggedIn', 'False')
    else:
        response.set_cookie('isUserLoggedIn', 'True')

    return response


@app.route("/<path:path>")
async def static_file(path):
    """
    Serve the static files from the static folder.
    Parameters:
        path (str): The path to the static file.
    """ """
    """
    return await send_from_directory(app.static_folder, path)

# Serve content files from blob storage from within the app to keep the example self-contained.
# *** NOTE *** this assumes that the content files are public, or at least that all users of the app
# can access all the files. This is also slow and memory hungry.

# Define a route for serving content files
@app.route("/content/<path>")
async def content_file(path):
    debug_info = {
        'status': 'success',
        'steps': {}
    }
    # Step 1: Check if the path is valid
    if not path:
        debug_info['status'] = 'error'
        debug_info['steps']['path_check'] = 'Path is empty or None'
        return jsonify(debug_info), 400
    logging.debug("1. Path is not empty : "+path)
    # Step 2: Try to access the blob
    try:
        print("path=====>",path)
        blob =  blob_container.get_blob_client(path).download_blob()
    except Exception as e:
        debug_info['status'] = 'error'
        debug_info['steps']['blob_access'] = f"Error accessing blob: {str(e)}"
        debug_info['steps']['trace'] = traceback.format_exc()
        return jsonify(debug_info), 500
    logging.debug("2. Got blob : ")
    # Step 3: Check MIME type

    try:
        mime_type = blob.properties["content_settings"]["content_type"]
        if mime_type == "application/octet-stream":
            mime_type = mimetypes.guess_type(path)[0] or "application/octet-stream"
        debug_info['steps']['mime_type'] = mime_type
    except Exception as e:
        debug_info['status'] = 'error'
        debug_info['steps']['mime_type_error'] = f"Error determining MIME type: {str(e)}"
        debug_info['steps']['trace'] = traceback.format_exc()
        return jsonify(debug_info), 500
    logging.debug("3. Got mime type : ")
    # Step 4: Read the blob content
    try:
        content =  blob.readall()
    except Exception as e:
        debug_info['status'] = 'error'
        debug_info['steps']['blob_read'] = f"Error reading blob content: {str(e)}"
        debug_info['steps']['trace'] = traceback.format_exc()
        return jsonify(debug_info), 500
    # If everything worked, return the content as before:
    return Response(content, mimetype=mime_type, headers={"Content-Disposition": f"inline; filename={path}"})
# Define a route for serving use case specific content files
@app.route("/uc/content/<usecasename>/<subfolder>/<path>")
async def usecase_content_file(usecasename,subfolder,path):

    # Log the path and use case name
    print("1. Path is not empty : "+path)
    print("2. usecasename : "+usecasename)

    # Construct the container name from the use case name
    uc_container = f"{usecasename}-content/{subfolder}"
    # Get a client for the container
    blob_container = blob_client.get_container_client(uc_container)
    print("3. Citation container : "+uc_container)
    print("4. Got container : ")


    # Try to get and download the blob
    try:
        blobObj = blob_container.get_blob_client(path)
        print("5. Got blobObj : ")
        blob = blobObj.download_blob()
        print("6. Got blob : ")
    except Exception as e:
        # Log any exceptions and return an error response
        logging.exception("Exception in /uc/content/{usecasename}/{path} :"+str(e))
        return jsonify({"error": str(e)}), 500

    # Get the MIME type of the blob
    mime_type = blob.properties["content_settings"]["content_type"]
    print("7. mime_type : "+mime_type)

    # If the MIME type is "application/octet-stream", try to guess the real MIME type
    if mime_type == "application/octet-stream":
        mime_type = mimetypes.guess_type(path)[0] or "application/octet-stream"
    return blob.readall(), 200, {"Content-Type": mime_type, "Content-Disposition": f"inline; filename={path}"}

@app.route("/uc/content/<usecasename>/<path>")
async def usecase_content_file_without_subfolder(usecasename,path):
    """
    Serve the content files for a specific use case.
    Parameters:
        usecasename (str): The name of the use case.
        path (str): The path to the content file.
    """
    # Log the path and use case name
    print("1. Path is not empty : "+path)
    print("2. usecasename : "+usecasename)

    # Construct the container name from the use case name
    uc_container = f"{usecasename}-content"
    # Get a client for the container
    blob_container = blob_client.get_container_client(uc_container)
    print("3. Citation container : "+uc_container)
    print("4. Got container : ")


    # Try to get and download the blob
    try:
        blobObj = blob_container.get_blob_client(path)
        print("5. Got blobObj : ")
        blob = blobObj.download_blob()
        print("6. Got blob : ")
    except Exception as e:
        # Log any exceptions and return an error response
        logging.exception("Exception in /uc/content/{usecasename}/{path} :"+str(e))
        return jsonify({"error": str(e)}), 500

    # Get the MIME type of the blob
    mime_type = blob.properties["content_settings"]["content_type"]
    print("7. mime_type : "+mime_type)

    # If the MIME type is "application/octet-stream", try to guess the real MIME type
    if mime_type == "application/octet-stream":
        mime_type = mimetypes.guess_type(path)[0] or "application/octet-stream"
    return blob.readall(), 200, {"Content-Type": mime_type, "Content-Disposition": f"inline; filename={path}"}


# Define a route for serving talk specific content files
@app.route("/talk/content/<thread>/<path>")
def talk_content_file(thread,path):
    """
    Serve the content files for a specific chat thread.
    Parameters:
        thread (str): The name of the chat thread.
        path (str): The path to the content file.
    """
    # Log the path and thread
    logging.exception("1. Path is not empty : "+path)
    logging.exception("2. thread : "+thread)

    # The container name is the same as the thread name
    talk_container = f"{thread}"

    # Get a client for the container
    blob_container = blob_client.get_container_client(talk_container)
    logging.exception("3. Citation container : "+talk_container)
    logging.exception("4. Got container : ")

    # Try to get and download the blob
    try:
        blobObj = blob_container.get_blob_client(path)
        logging.exception("5. Got blobObj : ")
        blob = blobObj.download_blob()
        logging.exception("6. Got blob : ")
    except Exception as e:
        # Log any exceptions and return an error response
        logging.exception("Exception in /talk/content/{thread}/{path} :"+str(e))
        return jsonify({"error": str(e)}), 500

    # Get the MIME type of the blob
    mime_type = blob.properties["content_settings"]["content_type"]
    logging.exception("7. mime_type : "+mime_type)

    # If the MIME type is "application/octet-stream", try to guess the real MIME type
    if mime_type == "application/octet-stream":
        mime_type = mimetypes.guess_type(path)[0] or "application/octet-stream"
    return blob.readall(), 200, {"Content-Type": mime_type, "Content-Disposition": f"inline; filename={path}"}

# Custom decorator for authentication of APIs
async def requires_aad(route_function):
    """
    Decorator to require Azure Active Directory (AAD) authentication for a route function.
    """

    # Use the wraps function from the functools module to preserve the metadata of the decorated function
    @wraps(route_function)
    async def decorated_function(*args, **kwargs):
        """
        Check if the request has a valid access token in the session.
        If the access token is valid, call the route function with the request arguments.
        If the access token is not valid, return a 403 Forbidden response.

        """
        if 'AD_USER_INFO' not in session:
            # User is not logged in, redirect to the login page

            response = make_response(jsonify({'message': 'User is  LogOut'}), 200)
            response.set_cookie('isUserLoggedIn','False')
            cookie_name = app.config['SESSION_COOKIE_NAME']
            response.delete_cookie(cookie_name)
            abort(403)
        else:
            # If the 'AD_USER_INFO' key is in the session, get its value
            AD_USER_INFO = session['AD_USER_INFO']
            if 'groups' not in AD_USER_INFO:
                # User is not logged in, redirect to the login page
                response = make_response(jsonify({'error': 'User is not logged in'}), 403)
                response.set_cookie('isUserLoggedIn', 'False')
                return response
                #abort(403)
        # return if loggied in
        return await route_function(*args, **kwargs)

    return decorated_function


def check_menu_access(f):
    @wraps(f)
    async def decorated_function(*args, **kwargs):
        json_data = await request.get_json()
        menu_name = json_data.get('menu_name')
        print("menu_name=====>",menu_name)
        if 'menus' not in session:
            return jsonify({'error': 'User is not logged in or session expired'}), 403

        if menu_name not in session['menus']:
            return jsonify({'error': 'User does not have access to this menu'}), 403

        return await f(*args, **kwargs)
    return decorated_function

# Define a route for getting menu items, which requires Azure Active Directory (AAD) authentication
@app.route('/menu_items', methods=['GET'])
# @requires_aad
async def menu_items():
    try:
        if 'AD_USER_INFO' not in session:
            print("inside not in session=======>")
            response = await make_response(jsonify({'error': 'User is not logged in'}), 403)
            response.set_cookie('isUserLoggedIn', 'False')
            cookie_name = app.config['SESSION_COOKIE_NAME']
            response.delete_cookie(cookie_name)
            return response
        else:
            AD_USER_INFO = session['AD_USER_INFO']
            print("session['AD_USER_INFO'] in else ========>",session['AD_USER_INFO'])
            session_id = session.get('_id', 'No Session ID')
            print(f"Session ID after setting user info: {session_id}")
            if 'groups' not in AD_USER_INFO:
                response = await make_response(jsonify({'error': 'User is not logged in'}), 403)
                response.set_cookie('isUserLoggedIn', 'False')
                cookie_name = app.config['SESSION_COOKIE_NAME']
                response.delete_cookie(cookie_name)
                return response

        print("session['AD_USER_INFO']========>",session['AD_USER_INFO'])
        print("session access_token===========>",session["access_token"])
        AD_USER_INFO = await get_user_details(access_token=session["access_token"])
        print("after get_user_details AD_USER_INFO========>",AD_USER_INFO)
        # if( status_code in AD_USER_INFO and AD_USER_INFO.status_code ==401):
        #     response = await make_response(jsonify({'error': 'User is not logged in'}), 403)
        #     response.set_cookie('isUserLoggedIn', 'False')
        #     cookie_name = app.config['SESSION_COOKIE_NAME']
        #     response.delete_cookie(cookie_name)
        #     return response

        session['AD_USER_INFO'] = AD_USER_INFO

        # Get the list of group IDs from the user details
        groups_list = AD_USER_INFO.get('groups', [])
        user_groupIds = [str(grp["GroupId"]) for grp in groups_list]
        # Get the menu items for the user's groups
        menu_items_list = await get_menu_items(user_groupIds)
        # Get the chat threads
        #threads = await chat_threads()
        return_obj = {}
        return_obj["menus"] = menu_items_list
        return_obj["user_groupIds"] = user_groupIds
        # Map the threads and add them to the return object
        # mapped_threads = [map_object(obj) for obj in threads]
        #return_obj["threads"] = threads
        session['menus'] = [menu['MenuItemName'] for menu in menu_items_list]

        return quart.jsonify(return_obj)
    except Exception as e:
        logging.exception("Exception in /menu_items/")
        strE = str(e)
        print("strE======>",strE)
        if "SyntaxError" in strE:
            return jsonify({"error": "Unfortunately, an error occurred while processing the response from GPT. Please try again."}), 500
        return jsonify({"error": str(e)}), 500

# Custom decorator for authentication of APIs
def requires_authentication(route_function):
    """
    Decorator to require API key authentication for a route function.
    """
    @wraps(route_function)
    async def decorated_function(*args, **kwargs):
        """
        Check if the request has a valid API key in the Authorization header.
        If the API key is valid, call the route function with the request arguments.
        If the API key is not valid, return a 401 Unauthorized response.
        """
        api_key = request.headers.get('Authorization')
        usecase_name = request.view_args.get('name')
        if not api_key or not validate_API_key(api_key, usecase_name):
            return jsonify({'message': 'Unauthorized'}), 401

        return route_function(*args, **kwargs)

    return decorated_function

# Define a route for a use case API, which requires authentication
@app.route('/api/v1/usecase/<name>', methods=['POST'])
@requires_authentication
async def usecase_api(name):
    """
    Handle the use case request.
    Parameters:
        name (str): The name of the use case.

    """
    # Ensure that the OpenAI token is available
    await ensure_openai_token()

    # Get the deployment name and approach from the request JSON
    gpt_deployment = (await request.get_json())["overrides"].get("deploymentName")
    approach = (await request.get_json())["approach"]

    # Get the user information from the session
    AD_USER_INFO = session['AD_USER_INFO']

    # Check if this is a new chat thread
    isNewChatThread = (await request.get_json())["isNewChatThread"]

    # Set the approach based on the deployment name
    if gpt_deployment=="chatplus":
        approach = "crrr"
    else:
        approach = "rrr"
    try:
        # Set up clients for Cognitive Search and Storage
        search_client = SearchClient(
            endpoint=f"https://{AZURE_SEARCH_SERVICE}.search.windows.net",
            index_name=f"{name}-index",
            credential=search_creds)

        # Get the implementation for the approach
        impl = usecase_approaches.get(approach)
        if not impl:
            return jsonify({"error": "unknown approach"}), 400
        if isNewChatThread == True:
            threadUrl = (await request.get_json())["threadUrl"]
            await cosmos_thread_logger(request.json["session_id"],"Usecase "+name,request.json["current_question"],threadUrl=threadUrl)

        # Run the implementation with the history, employee organization data, and overrides
        r = await impl.run(
            (await request.get_json())["history"],
            AD_USER_INFO['employeeOrgData'],
            (await request.get_json()).get("overrides") or {},
            usecase_search_client=search_client)

        result = await cosmos_logger(request.json["session_id"],"Usecase "+name,request.json["current_question"],r)
        if result and result.get('id') is not None:
            r['messageID'] = result['id']

        return jsonify(r)
    except Exception as e:
        logging.exception("Exception in /usecase/"+name)
        strE = str(e)
        if "SyntaxError" in strE:
            return jsonify({"error": "Unfortunately, an error occurred while processing the response from GPT. Please try again."}), 500
        return jsonify({"error": str(e)}), 500

# Define a route for getting use case parameters, which requires authentication
@app.route('/api/v1/params/<name>', methods=['GET'])
@requires_authentication
async def usecase_params_api(name):
    """
    Retrieve and return the details for a specific use case.

    This function takes in the name of a use case and retrieves its details using the get_usecase_data function.
    If the use case details exist, it logs the details and returns them as a JSON response with a 200 OK status code.
    If the use case details do not exist, it raises an exception and returns a 500 Internal Server Error status code with the exception message.
    Any other exceptions that occur during the process are also logged and returned as a 500 error.

    Parameters:
    name (str): The name of the use case to retrieve details for.

    Returns:
    json, int: A JSON object containing the use case details and a status code. If an exception occurs, the JSON object will contain the error message.
    """
    try:
        # Get the details for the use case
        usecase_details = await get_usecase_data(name)

        # Log the use case details
        logging.exception(usecase_details)

        # If the use case details exist, return them as a JSON response with a 200 OK status code
        if usecase_details:
            return jsonify(usecase_details), 200
        else:
            # If the use case details do not exist, raise an exception
            raise Exception(f"{name} Usecase not found")
    except Exception as e:
        # Log any exceptions
        logging.exception("Exception in /params/"+name)

        # Return the exception message as an error with a 500 Internal Server Error status code
        return jsonify({"error": str(e)}), 500

# Define a route for a use case, which does not require authentication
@check_menu_access
# Define the route for the usecase endpoint, expecting a POST request  
@app.route('/usecase/<name>', methods=['POST'])  
async def usecase(name):  
    """Handle the use case request."""  
    # Ensure OpenAI token is available and valid  
    await ensure_openai_token()  
    # Get the content type of the request  
    content_type = quart.request.content_type  
    # Get user info from session if available  
    AD_USER_INFO = session['AD_USER_INFO'] if session else None  
    employeeOrgData = AD_USER_INFO['employeeOrgData'] if AD_USER_INFO else None  
    # Check if the content type is either 'multipart/form-data' or 'application/x-www-form-urlencoded'  
    if 'multipart/form-data' in content_type or 'application/x-www-form-urlencoded' in content_type:  
        # Parse form data  
        json_data = await request.form  
        json_data_str = json_data.get('data')  
        json_data = json.loads(json_data_str)  
    else:  
        # Parse JSON data  
        json_data = await quart.request.get_json()  
      
    # Check if it's a new chat thread  
    isNewChatThread = json_data.get("isNewChatThread")  
      
    try:  
        conf_params = {}  
          
        # Get sql_params from the current user session (commented out for now)  
        user_id = session['AD_USER_INFO'].get("UserID")  
        sql_params_key = f"{user_id}"+"_"+f"{name}"
        usecase_sql_parmas= session.get(sql_params_key, None)
        
        print("before usecase_sql_parmas=======>",usecase_sql_parmas)  
        
        ## call the sql server if usecase_sql_parmas is  none  and save them in the session else take it from session -------------
        if usecase_sql_parmas is None:
            usecase_sql_parmas = await get_usecase_parmaeters(name,sql_params_key)
        ## if it dont work than we will create contant files dependes on the usecase we will create usecase file. -----------------  
        print("after usecase_sql_parmas=======>",usecase_sql_parmas)  
          
        # Get overrides from JSON data if any  
        overrides = json_data.get("overrides") or {} 
        
        print("overrides=========>",overrides) 
          
        # Create GPT Config object to pass in run method  
        conf_params['semantic_captions'] = True if overrides.get("semantic_captions") else False  
        conf_params['frequency_penalty'] = overrides.get("frequency_penalty") or 0  
        conf_params['presence_penalty'] = overrides.get("presence_penalty") or 0  
        conf_params['exclude_category'] = overrides.get("exclude_category") or None  
        conf_params['prompt_template'] = overrides.get("prompt_template") or None  
  
        # Check if user modified the params, if not take from SQL DB  
        conf_params['max_token'] = overrides.get("max_tokens") if overrides.get("max_tokens") else usecase_sql_parmas.get('MaxResponseLength', None)
        conf_params['top'] = overrides.get("top") if  overrides.get("top") else usecase_sql_parmas.get('NumDocRAG',None)
        conf_params['stop'] = overrides.get("stop") if overrides.get("stop") else usecase_sql_parmas.get('stopSequences', None) 
        conf_params['temperature'] = overrides.get("temperature") if overrides.get("temperature") else usecase_sql_parmas.get('temperature', 0)
        conf_params['ResponsePromptFewShotExample'] = usecase_sql_parmas.get('fewShotExample', None)  
        conf_params['deploymentName'] = usecase_sql_parmas.get('deploymentName', None)  
          
        # Init method parameters  
        usecase_name = usecase_sql_parmas.get('use_case_name', None)  
        indexname = usecase_sql_parmas.get('Indexname', None)  
        QueryPrompt = usecase_sql_parmas.get('QueryPrompt', None)  
        responsePrompt = usecase_sql_parmas.get('systemPrompt', None)  
        context_file_key = usecase_sql_parmas.get('context_file_key', None)  
        is_file_upload = usecase_sql_parmas.get('IsFileUpload', None)  
        IsVisionEnabled = usecase_sql_parmas.get('IsVisionEnabled', None)  
        is_rag = usecase_sql_parmas.get('IsRAGFlag', None)  
        deployment_name = usecase_sql_parmas.get('deploymentName', None)  
        refine_user_query = usecase_sql_parmas.get('RefineUserQueryFlag', None)  
        ResponsePromptFewShotExample = usecase_sql_parmas.get('fewShotExample', None)  
        
        
        print("conf_params=========>",conf_params) 
        
        # Initialize search client if RAG is enabled  
        if is_rag:  
            search_client = SearchClient(  
                endpoint=f"",  
                index_name=indexname,  
                credential= 
            )  
        else:  
            search_client = None  
          
        # Regular passed parameters  
        files = await request.files  
        history = json_data.get("history")  
        sessionId = json_data.get("session_id")  
        current_question = json_data.get("question")  
        is_ImageUploaded = json_data.get("is_ImageUploaded",None)
        session_instance_key = f"instance_{sessionId}"  
        current_instance = session.get(session_instance_key, None)  
        impl = ""  
        file_data_content = None  
        uploaded_file_key = None  
          
        # Get content of the uploaded files from UI and pass it to set method  
        files_uploaded = any(file.filename for file in files.getlist('files'))  
        if(files_uploaded):  
            file_data = await process_docs_usecase(files, sessionId)  
            if (file_data is not None):  
                file_data_content = file_data  
            if(file_data_content is not None):  
                uploaded_file_key = file_data_content['session_document_key']  
          
        # Log the new chat thread if applicable  
        
        if isNewChatThread and is_ImageUploaded and isinstance(current_question,list) and len(current_question)>1:
            threadUrl = json_data.get("threadUrl")  
            await cosmos_thread_logger(sessionId,"Usecase " + name,current_question[1],threadUrl=threadUrl)
        elif isNewChatThread:  
            threadUrl = json_data.get("threadUrl")  
            await cosmos_thread_logger(sessionId, "Usecase " + name, current_question, threadUrl=threadUrl)  
        
        # Initialize the UsecaseChatReadRetrieveReadApproach_LC object if not already done  
        if current_instance is None:  
            impl = UsecaseChatReadRetrieveReadApproach_LC(  
                usecase_name,  
                AZURE_OPENAI_CHATGPT_O_API_VERSION,  
                QueryPrompt,  
                responsePrompt,  
                ResponsePromptFewShotExample,  
                employeeOrgData,  
                KB_FIELDS_SOURCEPAGE,  
                KB_FIELDS_CONTENT,  
                context_file_key,  
                is_file_upload,  
                is_rag,  
                deployment_name,  
                refine_user_query,  
                IsVisionEnabled  
            )  
            session[session_instance_key] = impl  
        else:  
            impl = current_instance  
          
        # Return an error if the implementation is unknown  
        if not impl:  
            return jsonify({"error": "unknown approach"}), 400  
          
        # Set user upload files key if available  
        if uploaded_file_key:  
            await impl.set_user_upload_files_key(uploaded_file_key)  
          
        # Run the implementation and return the response  
        return Response(impl.run(history, conf_params, sessionId, current_question,is_ImageUploaded, search_client), content_type='text/event-stream')  
      
    except Exception as e:  
        # Log and return the exception  
        logging.exception("Exception in /usecase/" + name)  
        strE = str(e)  
        if "SyntaxError" in strE:  
            return jsonify({"error": "Unfortunately, an error occurred while processing the response from GPT. Please try again."}), 500  
        return jsonify({"error": str(e)}), 500  


# Define the route for the usecaseLegal endpoint, expecting a POST request  
@app.route('/usecaselegal/<name>', methods=['POST'])  
async def usecaseLegal(name):  
    """Handle the use case request."""  
      
    # Ensure OpenAI token is available and valid  
    await ensure_openai_token()  
      
    # Get JSON data from the request  
    json_data = await quart.request.get_json()  
      
    # Check if it's a new chat thread  
    isNewChatThread = json_data.get("isNewChatThread")  
    print("isNewChatThread=====>", isNewChatThread)  
      
    # Get user info from session if available  
    AD_USER_INFO = session['AD_USER_INFO'] if session else None  
    employeeorgdata = AD_USER_INFO['employeeOrgData'] if AD_USER_INFO else None  
      
    try:  
        # Initialize search client  
        search_client = SearchClient(  
            endpoint=f"https://{AZURE_SEARCH_SERVICE}.search.windows.net",  
            index_name=f"{name}-index",  
            credential=search_creds  
        )  
          
        # Get the SQL parameters from the current user session  
        conf_params = {}  
        user_id = session['AD_USER_INFO'].get("UserID")  
        sql_params_key = f"{user_id}" + "_" + f"{name}"  
        usecase_sql_parmas = session.get(sql_params_key, None)
        
        print("after usecase_sql_parmas=======>",usecase_sql_parmas)  
        
        if usecase_sql_parmas is None:
            usecase_sql_parmas = await get_usecase_parmaeters(name,sql_params_key)  
      
        print("before usecase_sql_parmas========>", usecase_sql_parmas)  
          
        # Get overrides from JSON data if any  
        overrides = json_data.get("overrides") or {}  
        print("overrides========>", overrides)  
          
        # Creating GPT Config object to pass in run method  
        conf_params['semantic_captions'] = True if overrides.get("semantic_captions") else False  
        conf_params['frequency_penalty'] = overrides.get("frequency_penalty") or 0  
        conf_params['presence_penalty'] = overrides.get("presence_penalty") or 0  
        conf_params['exclude_category'] = overrides.get("exclude_category") or None  
        conf_params['prompt_template'] = overrides.get("prompt_template") or None  
          
        # Check if user modified the params, if not take from SQL DB  
        conf_params['max_token'] = overrides.get("max_tokens") if overrides.get("max_tokens") else usecase_sql_parmas.get('MaxResponseLength', None)  
        conf_params['top'] = overrides.get("top") if overrides.get("top") else usecase_sql_parmas.get('NumDocRAG', None)  
        conf_params['stop'] = overrides.get("stop") if overrides.get("stop") else usecase_sql_parmas.get('stopSequences', None)  
        conf_params['temperature'] = overrides.get("temperature") if overrides.get("temperature") else usecase_sql_parmas.get('temperature', 0)  
        conf_params['deploymentName'] = usecase_sql_parmas.get('deploymentName', None)  
          
        # Init method parameters  
        print("usecase_sql_parmas.get('IsFileUpload',None)======>", usecase_sql_parmas.get('IsFileUpload', None))  
        usecase_name = usecase_sql_parmas.get('use_case_name', None)  
        QueryPrompt = usecase_sql_parmas.get('QueryPrompt', None)  
        responsePrompt = usecase_sql_parmas.get('systemPrompt', None)  
        deployment_name = usecase_sql_parmas.get('deploymentName', None)  
        refine_user_query = usecase_sql_parmas.get('RefineUserQueryFlag', None)  
        ResponsePromptFewShotExample = usecase_sql_parmas.get('fewShotExample', None)  
          
        # Retrieve necessary data from JSON payload  
        history = json_data.get("history")  
        overrides = json_data.get("overrides") or {}  
        sessionId = json_data.get("session_id")  
        approach = json_data.get("approach")  
        current_question = json_data.get("question")  
        session_instance_key = f"instance_{sessionId}"  
        current_instance = session.get(session_instance_key, None)  
        impl = ""  
          
        # Log the new chat thread if applicable  
        if isNewChatThread:  
            threadUrl = json_data.get("threadUrl")  
            await cosmos_thread_logger(sessionId, "Usecase " + name, current_question, threadUrl=threadUrl)  
          
        # Initialize the legalusecaseChatReadRetrieveRead_LC object if not already done  
        if current_instance is None:  
            if approach == "lrrr":  
                impl = legalusecaseChatReadRetrieveRead_LC(  
                    usecase_name,  
                    deployment_name,  
                    AZURE_OPENAI_CHATGPT_O_API_VERSION,  
                    refine_user_query,  
                    QueryPrompt,  
                    responsePrompt,  
                    employeeorgdata,  
                    KB_FIELDS_SOURCEPAGE,  
                    KB_FIELDS_CONTENT  
                )  
                session[session_instance_key] = impl  
        else:  
            impl = current_instance  
          
        # Return an error if the implementation is unknown  
        if not impl:  
            return jsonify({"error": "unknown approach"}), 400  
          
        # Run the implementation and return the response  792
        
        return Response(impl.run(history, conf_params, sessionId, current_question, search_client), content_type='text/event-stream')  
      
    except Exception as e:  
        # Log and return the exception  
        logging.exception("Exception in /usecase/" + name)  
        strE = str(e)  
        if "SyntaxError" in strE:  
            return jsonify({"error": "Unfortunately, an error occurred while processing the response from GPT. Please try again."}), 500  
        return jsonify({"error": str(e)}), 500  




async def get_usecase_parmaeters(name,sql_params_key):
    try:
            usecase_details = get_usecase_params(name)
            if usecase_details:
                usecase_details = {k: str(v) if not isinstance(v, (str, int, float, bool, list, dict, type(None))) else v for k, v in usecase_details.items()}
                
            #------------------------------------------------------------------------------------
            # Taking filePath and get the cosmos key
            #------------------------------------------------------------------------------------
            filePaths = usecase_details.get('filePath',None)  # "['path1','path2']"
            #Path of the fie
            if (filePaths is not None and filePaths != ""):
                filePaths = ast.literal_eval(filePaths)  
                print("inside file path option======>",filePaths)
                sessionId = str(uuid4())
                file_data_content = await download_file_data(filePaths,sessionId)
                usecase_details['context_file_key'] =  file_data_content['session_document_key'] #sql_context_file_key

            usecase_details.pop('filePath')  # "['path1','path2']"
            #------------------------------------------------------------------------------------
            # Store the sql_params in the current user session
            #------------------------------------------------------------------------------------
            usecase_details_input = {
                "use_case_name":usecase_details.get("use_case_name",None),
                "systemPrompt":usecase_details.get("systemPrompt",None),
                "deploymentName":usecase_details.get("deploymentName",None),
                "maxResponseLength":usecase_details.get("maxResponseLength",None),
                "temperature":usecase_details.get("temperature",None),
                "topProbabilities":usecase_details.get("topProbabilities",None),
                "stopSequences":usecase_details.get("stopSequences",None),
                "pastMessagesToInclude":usecase_details.get("pastMessagesToInclude",None),
                "frequencyPenalty":usecase_details.get("frequencyPenalty",None),
                "presencePenalty":usecase_details.get("presencePenalty",None),
                "Indexname":usecase_details.get("Indexname",None),
                "QueryPrompt":usecase_details.get("QueryPrompt",None),
                "fewShotExample":usecase_details.get("fewShotExample",None),
                "filePath":usecase_details.get("filePath",None),
                "IsVisionEnabled":usecase_details.get("IsVisionEnabled",None),
                "IsFileUpload":usecase_details.get("IsFileUpload",None),
                "NumDocRAG":usecase_details.get("NumDocRAG",None),
                "IsRAGFlag":usecase_details.get("IsRAGFlag",None),
                "RefineUserQueryFlag":usecase_details.get("RefineUserQueryFlag",None),
                "context_file_key":usecase_details.get("context_file_key",None),
                "IsVisionEnabled":usecase_details.get("IsVisionEnabled",None),

            }
            if usecase_details:
                if session.get(sql_params_key, None) is None:
                    session[sql_params_key] = usecase_details_input
                
            return usecase_details_input    
                
    except Exception as e:
        # Log any exceptions
        logging.exception("Exception in /get_usecase_parmaeters/"+name)
        return jsonify({"error": str(e)}), 500

                    
                
async def download_file_data(filePaths, sessionId):  
    combined_content = ""  # To store the combined content of all files  
    results = []  
    MAX_FILE_TOKENS = 90000
  
    for filePath in filePaths:  
        parsed_url = urlparse(filePath)  
        path_parts = parsed_url.path.lstrip('/').split('/')  
        container_name = path_parts[0]  
        blob_name = '/'.join(path_parts[1:])  
        mime_type, _ = mimetypes.guess_type(blob_name)  
        if not mime_type:  
            mime_type = 'application/octet-stream'  # Default to binary stream if MIME type is unknown  
        content = download_blob_to_bytes(container_name, blob_name)  
        # Save the file locally  
        file_name = blob_name.split('/')[-1]  
        local_file_path = os.path.join('/temp2/', file_name)  
        # Ensure the directory exists  
        os.makedirs(os.path.dirname(local_file_path), exist_ok=True)  
        # Ensure the content is in bytes before writing  
        if isinstance(content, bytes):  
            print("Content is of type bytes, no need to encode.")  
        else:  
            print("Content is of type str, encoding to bytes.")  
            content = content.encode('utf-8')  
        try:  
            with open(local_file_path, 'wb') as f:  
                f.write(content)  
                print(f"File written successfully to {local_file_path}")  
        except Exception as e:  
            print(f"Error writing file to local storage: {e}")  
            raise  
        try:  
            file_storage = FileStorage(  
                stream=open(local_file_path, 'rb'),  
                filename=file_name,  
                content_type=mime_type  
            )  
        except Exception as e:  
            print(f"Error creating FileStorage object: {e}")  
            raise  
        # Call the process_docs_usecase function  
        files = {'files': [file_storage]}  
        result = await process_docs_usecase(files, sessionId)  
        # Cleanup  
        file_storage.close()  
        if os.path.exists(local_file_path):  
            os.remove(local_file_path)  
          
        combined_content += str(result['content'])  # Combine the content  
          
        # Append individual result for reference  
        results.append({  
            "file_name": file_name,  
            "result": result  
        })  
  
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")  
    session_document_key = f"document_content_{sessionId}_{timestamp}"  
    total_word_count = count_words(combined_content)  
    try:
        if total_word_count > MAX_FILE_TOKENS:  
            print("word count exceeded") 
    except Exception as e:  
            print(f"Max token count exceed: {e}")  
            raise 
        
    final_result = document_content_logger(session_document_key, combined_content)  
    result = {
        "session_document_key" : final_result['session_document_key'],
    }

    return result
       # return session_document_key

def count_words(text):
        """Utility function to count words in a text."""
        return len(text.split())






def download_blob_to_bytes(container_name, blob_name):


    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    blob_data = blob_client.download_blob().readall()
    return blob_data


# Define a route for getting use case parameters, which does not require authentication
@app.route('/params/<name>', methods=['GET'])
async def usecase_params(name):
    """
    Get the details for the use case parameters.
    Parameters:
    name (str): The name of the use case.
    """
    try:
        # Get the details for the use case
        usecase_details = get_usecase_data(name)

        # Ensure all data in usecase_details is JSON-serializable
        if usecase_details:
            usecase_details = {k: str(v) if not isinstance(v, (str, int, float, bool, list, dict, type(None))) else v for k, v in usecase_details.items()}

        # Process the main image
        image_url = usecase_details.get('imagePath', None)
        if image_url:
            try:
                parsed_url = urlparse(image_url)
                path_parts = parsed_url.path.lstrip('/').split('/')
                container_name = path_parts[0]
                blob_name = '/'.join(path_parts[1:])
                mime_type, _ = mimetypes.guess_type(blob_name)
                if not mime_type:
                    mime_type = 'application/octet-stream'  # Default to binary stream if MIME type is unknown

                blob_data = download_blob_to_bytes(container_name, blob_name)
                if blob_data:
                    image_base64 = base64.b64encode(blob_data).decode('utf-8')
                    usecase_details['image'] = f"data:{mime_type};base64,{image_base64}"
            except Exception as e:
                logging.exception(f"Failed to fetch image from URL for {name}: {str(e)}")
                usecase_details['image'] = None
        else:
            usecase_details['image'] = None

        # Process the icon images
        icon_images = usecase_details.get('IconImages', [])
        for idx, icon_url in enumerate(icon_images):
            if icon_url:
                try:
                    print("idx==>",idx)
                    parsed_url = urlparse(icon_url)
                    path_parts = parsed_url.path.lstrip('/').split('/')
                    container_name = path_parts[0]
                    blob_name = '/'.join(path_parts[1:])
                    mime_type, _ = mimetypes.guess_type(blob_name)
                    if not mime_type:
                        mime_type = 'application/octet-stream'  # Default to binary stream if MIME type is unknown

                    blob_data = download_blob_to_bytes(container_name, blob_name)
                    if blob_data:
                        icon_base64 = base64.b64encode(blob_data).decode('utf-8')
                        icon_images[idx] = f"data:{mime_type};base64,{icon_base64}"
                    else:
                        icon_images[idx] = ""
                except Exception as e:
                    logging.exception(f"Failed to fetch icon from URL for {name}: {str(e)}")
                    icon_images[idx] = ""
            else:
                icon_images[idx] = ""

        usecase_details['IconImages'] = icon_images
        
        #------------------------------------------------------------------------------------
        # Taking filePath and get the cosmos key
        #------------------------------------------------------------------------------------
        filePaths = usecase_details.get('filePath',None)  # "['path1','path2']"
         #Path of the fie
        if (filePaths is not None and filePaths != ""):
            filePaths = ast.literal_eval(filePaths)  
            print("inside file path option======>",filePaths)
            sessionId = str(uuid4())
            file_data_content = await download_file_data(filePaths,sessionId)
            usecase_details['context_file_key'] =  file_data_content['session_document_key'] #sql_context_file_key

        usecase_details.pop('filePath')  # "['path1','path2']"
        #------------------------------------------------------------------------------------
        # Store the sql_params in the current user session
        #------------------------------------------------------------------------------------
        usecase_details_input = {
            "use_case_name":usecase_details.get("use_case_name",None),
			"systemPrompt":usecase_details.get("systemPrompt",None),
            "deploymentName":usecase_details.get("deploymentName",None),
			"maxResponseLength":usecase_details.get("maxResponseLength",None),
            "temperature":usecase_details.get("temperature",None),
			"topProbabilities":usecase_details.get("topProbabilities",None),
            "stopSequences":usecase_details.get("stopSequences",None),
			"pastMessagesToInclude":usecase_details.get("pastMessagesToInclude",None),
            "frequencyPenalty":usecase_details.get("frequencyPenalty",None),
            "presencePenalty":usecase_details.get("presencePenalty",None),
            "Indexname":usecase_details.get("Indexname",None),
			"QueryPrompt":usecase_details.get("QueryPrompt",None),
			"fewShotExample":usecase_details.get("fewShotExample",None),
            "filePath":usecase_details.get("filePath",None),
			"IsVisionEnabled":usecase_details.get("IsVisionEnabled",None),
            "IsFileUpload":usecase_details.get("IsFileUpload",None),
            "NumDocRAG":usecase_details.get("NumDocRAG",None),
			"IsRAGFlag":usecase_details.get("IsRAGFlag",None),
			"RefineUserQueryFlag":usecase_details.get("RefineUserQueryFlag",None),
			"context_file_key":usecase_details.get("context_file_key",None),
			"IsVisionEnabled":usecase_details.get("IsVisionEnabled",None),
   
        }
        if usecase_details:
            user_id = session['AD_USER_INFO'].get("UserID")
            sql_params_key = f"{user_id}"+"_"+f"{name}"
            session[sql_params_key] = usecase_details_input
            return jsonify(usecase_details), 200
        else:
            raise Exception(f"{name} Usecase not found")
    except Exception as e:
        # Log any exceptions
        logging.exception("Exception in /params/"+name)
        return jsonify({"error": str(e)}), 500

@app.route('/process_docs', methods=['POST'])
async def process_docs():
    try:
        """
        Process the documents from the request.
        """
        # Define a mapping of file extensions to file loaders and their arguments
        FILE_LOADER_MAPPING = {
            "csv": (CSVLoader, {"encoding": "utf-8"}),
            "docx": (UnstructuredWordDocumentLoader, {}),
            "pdf": (PyPDFLoader, {}),
            "pptx": (UnstructuredPowerPointLoader, {}),
            "txt": (TextLoader, {"encoding": "utf8"}),
            "xlsx": (UnstructuredExcelLoader, {}),
            "c": (TextLoader, {"encoding": "utf8"}),
            "cpp": (TextLoader, {"encoding": "utf8"}),
            "html": (TextLoader, {"encoding": "utf8"}),
            "java": (TextLoader, {"encoding": "utf8"}),
            "json": (TextLoader, {"encoding": "utf8"}),
            "md": (TextLoader, {"encoding": "utf8"}),
            "php": (TextLoader, {"encoding": "utf8"}),
            "py": (TextLoader, {"encoding": "utf8"}),
            "rb": (TextLoader, {"encoding": "utf8"}),
            "tex": (TextLoader, {"encoding": "utf8"}),
            "css": (TextLoader, {"encoding": "utf8"}),
            "js": (TextLoader, {"encoding": "utf8"}),
            "ts": (TextLoader, {"encoding": "utf8"}),
            "xml": (TextLoader, {"encoding": "utf8"})
        }

        # Get the list of files from the request
        files = await request.files

        # Log the files for debugging
        print("files=====>", files)

        # Get the thread ID from the request form
        form_data = await request.form
        threadId = str(form_data.get('threadId'))

        # Define the path for the dictionary
        dict_path = "/tmp/"
        # Get the directory path
        dir_path = os.path.dirname(dict_path)
        # If the directory does not exist, create it
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        documents = {}  # Dictionary to store the content of all files
        total_word_count = 0  # Variable to keep track of total word count
        max_words = 95900  # Maximum allowed word count

        # Iterate over each file item in the ImmutableMultiDict
        for file in files.getlist('files'):
            if file.filename:  # Check if file has a name
                file_name = "file_" + threadId + os.path.splitext(file.filename)[1]
                file_path = dict_path + file_name

                try:
                    # Try to open the file and write to it
                    with open(file_path, 'wb') as f:
                        f.write(file.read())
                except FileNotFoundError as e:
                    # If the file does not exist, create the directory and then open the file and write to it
                    os.makedirs(os.path.dirname(dict_path))
                    with open(file_path, 'wb') as f:
                        f.write(file.read())

                # Extract the file extension
                ext = file_path.split('.')[-1].lower()

                # If the file extension is in the file loader mapping
                if ext in FILE_LOADER_MAPPING:
                    # Get the loader class and arguments
                    loader_class, loader_args = FILE_LOADER_MAPPING[ext]
                    # Create the loader
                    loader = loader_class(file_path, **loader_args)
                    # Get the running loop
                    loop = asyncio.get_running_loop()
                    # Load the documents
                    loaded_documents = await loop.run_in_executor(None, loader.load)
                    # Join the page content of the loaded documents
                    content = "".join([doc.page_content for doc in loaded_documents])
                    # Count the words in the content
                    word_count = len(content.split())

                    # Check if adding this file exceeds the word limit
                    if total_word_count + word_count > max_words:
                        # Truncate the content to fit within the limit
                        allowed_words = max_words - total_word_count
                        truncated_content = " ".join(content.split()[:allowed_words])
                        documents[file.filename] = truncated_content
                        total_word_count += allowed_words
                        print(f"Truncated content for {file.filename} to fit within the word limit.")
                        return quart.jsonify({"error": f"Truncated content for {file.filename} to fit within the word limit."}), 500
                        # break  # Stop processing more files as the limit is reached
                    else:
                        # Store the content in the dictionary with the filename as the key
                        documents[file.filename] = content
                        total_word_count += word_count
                        # Print a success message
                        print(f"Loading successful for {file.filename}")

                # If the file exists, remove it
                if os.path.exists(file_path):
                    os.remove(file_path)

        # Set the documents in the talk approaches
        talk_approaches[threadId] = documents
        if documents:
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            #here threadId is a UUID which is passed from UI to backend, it is not a read threadID or sessionID
            session_document_key = f"document_content_{threadId}_{timestamp}"
            # session[session_document_key] = document
            result = document_content_logger(session_document_key,content=documents)
            cosmosdb_Id =''
            if result and result.get('id') is not None:
                cosmosdb_Id = result['id']
            # Print the talk approaches
            # Return a JSON response with the model, index, storage, and document
            return jsonify({
                "oaModel": "GPT-4",
                "cogIndex": "question-on-doc",
                "storage": "index_name",
                # "document":document,
                "session_document_key":session_document_key,
                "cosmosdb_Id":cosmosdb_Id
            })
        else:
            return jsonify({
                "oaModel": "GPT-4",
                "cogIndex": "question-on-doc",
                "storage": "index_name",
                "message":"Not able to extract the data"
            })

    except Exception as e:
        strE = str(e)
        return quart.jsonify({"error": str(strE)}), 500

async def generate_response_stream(question, content,AD_USER_INFO,session_id,talk):
    try:
        os.environ["AZURE_OPENAI_API_KEY"] =  openai.api_key
        os.environ["AZURE_OPENAI_ENDPOINT"] = openai.api_base
        streamed_data = []
        template = """Answer the question based only on the following context:
            {content}
            Question: {question}
            """
        formatted_template = template.format(content=content, question=question)
        llm = AzureChatOpenAI(
                openai_api_version=AZURE_OPENAI_CHATGPT_O_API_VERSION,
                azure_deployment=AZURE_OPENAI_CHATGPT_O_DEPLOYMENT,
                temperature=0.1,
                max_tokens=2000,
            )
        messages = [
            HumanMessage(content=(formatted_template)),
        ]
        streamed_data = []
        streamed_response = ""
        async for chunk in AsyncIterator(itertools.islice(llm.stream(messages), 0, None)):
            streamed_response += chunk.content
            # Process each chunk
            formatted_data = {
                "data_points": [],  # Assuming you'll fill this in based on your app's logic
                "answer": streamed_response,
                "thoughts": "",  # Same as above, fill in based on your app's logic
                "streamEnd": False  # Indicates ongoing streaming
            }
            # Send each chunk's data back to the client
            yield f"data: {json.dumps(formatted_data)}\n\n"
            # Keep accumulating the content for a final response
            streamed_data.append(chunk.content)
        logged_response = "".join(streamed_data)
        final_response = {
            "data_points": "",  # Assuming 'results' is defined elsewhere in your logic
            "answer": logged_response,
            "thoughts": "",
            "streamEnd": True  # Indicates the end of streaming
        }

        result = await cosmos_logger(
            session_id,
            AD_USER_INFO['employeeOrgData'] if AD_USER_INFO  else {},
            "Talk",
            question,
            final_response,
            talk
        )
        if result and result.get('id') is not None:
            final_response['messageID'] = result['id']
        yield f"data: {json.dumps(final_response)}\n\n"
    except Exception as e:
        print("getting error",str(e))
@app.route('/talk', methods=['POST'])
async def talk():
    try:
        json_data = await quart.request.get_json()
        isNewChatThread = json_data["isNewChatThread"]
        session_id = json_data["session_id"]
        talk = json_data["talk"]
        session_document_key = json_data["session_document_key"]
        doc_content = get_document_content(session_document_key)

        AD_USER_INFO ={}
        if isNewChatThread == True:
            threadUrl = json_data["threadUrl"]
            await cosmos_thread_logger(
                json_data["session_id"],
                "Talk",
                json_data["current_question"],
                threadUrl=threadUrl,
                cogIndex="",
                conversationStyle="",
                oaModel="",
                filename="",
                storage=""
            )
        # Get the question and content from the request JSON
        question = json_data["current_question"]
        # content = json_data["content"]
        os.environ["AZURE_OPENAI_API_KEY"] =  openai.api_key
        os.environ["AZURE_OPENAI_ENDPOINT"] = openai.api_base
        return Response(generate_response_stream(question, doc_content,AD_USER_INFO,session_id,talk),content_type='text/event-stream')
    except Exception as e:
            logging.exception("Exception in /talk")
            strE = str(e)
            if "SyntaxError" in strE:
                return quart.jsonify(
                    {"error": "Unfortunately, an error occurred while processing the response from GPT. Please try again."}
                ), 500
            return quart.jsonify({"error": str(e)}), 500
        # return quart.jsonify({"error": str(e)}), 500

# @app.route('/remove_document/', methods=["POST"])
# async def remove_document():
#     try:
#         print("inside here====>")
#         json_data = await request.get_json()
#         session_document_key = json_data['session_document_key']
#         document_id = json_data['document_id']
#         print("inside here")
#         document = list(document_content_container.query_items(
#             query="SELECT * FROM c WHERE c.id = @id",
#             parameters=[{"name": "@id", "value": document_id}],
#             partition_key=session_document_key
#         ))
#         if not document:
#             return jsonify({'message': f"No document found with ID '{document_id}'. Nothing to delete."}), 404
#         # If the document exists, then proceed to delete it
#         document_content_container.delete_item(item=document_id, partition_key=session_document_key)
#         return jsonify({'message': f"Document with ID '{document_id}' deleted successfully."}), 200
#     except Exception as e:
#         print(f"Failed to delete document: {e}")
#         return jsonify({'error': 'Failed to delete document'}), 500
    
    

# @app.route('/remove_document/', methods=["POST"])
# async def remove_document():
#     try:
#         print("inside here====>")
#         json_data = await request.get_json()
#         session_document_key = json_data['session_document_key']
#         document_id = json_data['document_id']
#         print("inside here")
#         document = list(document_content_container.query_items(
#             query="SELECT * FROM c WHERE c.id = @id",
#             parameters=[{"name": "@id", "value": document_id}],
#             partition_key=session_document_key
#         ))
#         if not document:
#             return jsonify({'message': f"No document found with ID '{document_id}'. Nothing to delete."}), 404
#         # If the document exists, then proceed to delete it
#         document_content_container.delete_item(item=document_id, partition_key=session_document_key)
#         return jsonify({'message': f"Document with ID '{document_id}' deleted successfully."}), 200
#     except Exception as e:
#         print(f"Failed to delete document: {e}")
#         return jsonify({'error': 'Failed to delete document'}), 500



@app.route('/remove_document/', methods=["POST"])
async def remove_document():
    try:
        print("inside here====>")
        json_data = await request.get_json()
        name = json_data['menu_name']
        if name:
            user_id = session['AD_USER_INFO'].get("UserID")
            sql_params_key = f"{user_id}"+"_"+f"{name}" 
            usecase_sql_parmas= session.get(sql_params_key, None)
            context_file_key = usecase_sql_parmas.get(context_file_key,None)
            uploaded_file_key = session.get('uploaded_file_key')
            if context_file_key:
                query = "SELECT * FROM c WHERE c.partitionKey = @context_file_key"  
                parameters = [{"name": "@session_document_key", "value": context_file_key}]  # how to get 
                document = list(container.query_items(  
                    query=query,  
                    parameters=parameters,  
                    partition_key=context_file_key  
                )) 
                if not document:
                    return jsonify({'message': f"No document found with ID '{document_id}'. Nothing to delete."}), 404   
                
                document_content_container.delete_item(partition_key=context_file_key)
                return jsonify({'message': f"Document deleted successfully."}), 200
            if uploaded_file_key:
                query = "SELECT * FROM c WHERE c.partitionKey = @session_document_key"  
                parameters = [{"name": "@session_document_key", "value": uploaded_file_key}]  # how to get 
                document = list(container.query_items(  
                    query=query,  
                    parameters=parameters,  
                    partition_key=uploaded_file_key  
                ))
                if not document:
                    return jsonify({'message': f"No document found. Nothing to delete."}), 404   
                 
                document_content_container.delete_item(partition_key=uploaded_file_key)
                return jsonify({'message': f"Document deleted successfully."}), 200
                
        else:    
            session_document_key = json_data['session_document_key']
            document_id = json_data['document_id']
            print("inside here")
            document = list(document_content_container.query_items(
                query="SELECT * FROM c WHERE c.id = @id",
                parameters=[{"name": "@id", "value": document_id}],
                partition_key=session_document_key
            ))
            if not document:
                return jsonify({'message': f"No document found with ID '{document_id}'. Nothing to delete."}), 404
            # If the document exists, then proceed to delete it
            document_content_container.delete_item(item=document_id, partition_key=session_document_key)
            return jsonify({'message': f"Document with ID '{document_id}' deleted successfully."}), 200
    except Exception as e:
        print(f"Failed to delete document: {e}")
        return jsonify({'error': 'Failed to delete document'}), 500


class AsyncIterator:
    def __init__(self, generator):
        self.generator = generator

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            return next(self.generator)
        except StopIteration:
            raise StopAsyncIteration

# Define a route for the Azure Active Directory login callback
@app.route('/.auth/login/aad/callback')
async def callback():
    """
    Handle the callback from the Azure AD authorization process.

    This function is called after the user has authenticated with Azure AD.
    It extracts the authorization code from the query parameters and uses it to acquire a user token.
    If the user token contains an access token, it stores the access token in the session and uses it to get the user's details.
    The user's details are also stored in the session.
    The function then redirects the user to the home page if the access token is found, or to the login page if not.

    Returns:
    redirect: A redirect response to the home page or the login page.
    """
    # Extract the authorization code from the query parameters
    authorization_code = quart.request.args.get('code')
    # Use the authorization code to get the user token
    AD_USER_TOKEN = PCApp.acquire_token_by_authorization_code(
        code=authorization_code,
        scopes=["user.read"],
        redirect_uri = REDIRECT_URI
    )
    print("AD_USER_TOKEN=========>",AD_USER_TOKEN)
    # If the user token contains an access token; extract, store the token to get users' details
    if "access_token" in AD_USER_TOKEN:
        access_token = AD_USER_TOKEN["access_token"]
        session["access_token"] = access_token
        # You have the access token now, you can use it to make authenticated request
        print("before calling the function==========>")
        AD_USER_INFO = await get_user_details(access_token)
        print("AD_USER_INFO in callback function======>",AD_USER_INFO)
        session['AD_USER_INFO'] = AD_USER_INFO
        print("after the in callback function======>",session['AD_USER_INFO'])

        return quart.redirect("/")

    return quart.redirect("/login")

# Define a route for the login page
@app.route("/login")
async def login():
    """
    Log in the user by redirecting to the Azure AD login endpoint.
    """
    # if logged in already, redirect to home page
    if 'AD_USER_INFO' in session:
        return redirect("/")
    # if not logged in, redirect to the login page
    # get authorization request url
    else:
        # Define the scopes and other parameters
        SCOPES = ["user.read.all"]
        AUTH_URL = PCApp.get_authorization_request_url(
            scopes=SCOPES,
            redirect_uri=REDIRECT_URI,  # Your Redirect URI
        )
        # Redirect the user to the Azure AD login page
        return redirect(AUTH_URL)

# Define a route for the logout page
@app.route("/logout")
async def logout():
    """
    Log out the user by clearing the session values and redirecting to the Azure AD logout endpoint.
    """
    if session:
        session.pop("access_token", None)
        session.pop("AD_USER_INFO", None)
    # LOGOUT_REDIRECT_URI_BASE = config['DEFAULT']['REDIRECT_URI']
    post_logout_redirect_uri = LOGOUT_REDIRECT_URI
    
    print("post_logout_redirect_uri=========>",post_logout_redirect_uri)
    azure_ad_logout_url = (
        f''
        f''
    )
    return quart.redirect(azure_ad_logout_url)


# Define a route for the ask page, which accepts POST requests
@app.route("/ask", methods=["POST"])
async def ask():
    """
    Ask a question using the specified approach and return the response.
    """
    try:

        if session is not None:
        # Get the user information from the session
            AD_USER_INFO = session.get('AD_USER_INFO', {})
        else:
            AD_USER_INFO = {}
        ensure_openai_token()
        approach = (await quart.request.get_json())["approach"]
        isNewChatThread = (await quart.request.get_json())["isNewChatThread"]
        try:
            if isNewChatThread == True:
                threadUrl = (await quart.request.get_json())["threadUrl"]
                await cosmos_thread_logger(
                    (await quart.request.get_json())["session_id"],
                    "GEAGPT Ask",
                    (await quart.request.get_json())["question"],
                    threadUrl=threadUrl,
                )
            impl = ""
            json_data = await quart.request.get_json()
            overrides = json_data.get("overrides") or {}
            sessionId = json_data.get("session_id")
            current_question = json_data.get("question")
            session_instance_key = f"instance_{sessionId}"
            removed_content = session.get(session_instance_key, None)
            if removed_content is None:
                print("inside if ==>")
                impl =  RetrieveThenReadApproach(AZURE_OPENAI_CHATGPT_O_DEPLOYMENT,AZURE_OPENAI_CHATGPT_O_API_VERSION, KB_FIELDS_SOURCEPAGE, KB_FIELDS_CONTENT)
                print("taking instance",impl)
                session[session_instance_key] = impl
            else:
                print("inside else====>")
                impl = removed_content
            if not impl:
                return jsonify({"error": "unknown approach"}), 400
            print("herere=====>")
            if not impl:
                return jsonify({"error": "unknown approach"}), 400

            return Response(impl.run(search_client,current_question,overrides,sessionId,current_question,AD_USER_INFO),content_type='text/event-stream')
        except Exception as e:
            # Log any exceptions
            logging.exception("Exception in /ask")
            strE = str(e)
            if "SyntaxError" in strE:
                return quart.jsonify(
                    {"error": "Unfortunately, an error occurred while processing the response from GPT. Please try again."}
                ), 500
            return quart.jsonify({"error": str(e)}), 500
    except Exception as e:
        # Log any exceptions
        logging.exception("Exception in /ask")
        return quart.jsonify({"error": str(e)}), 500

# Define a route for the chat page, which accepts POST requests
@check_menu_access
@app.route("/chat", methods=["POST"])  
async def chat():  
    """  
    Chat using the specified approach and return the response.  
    """  
      
    # Initialize OpenAI-related variables  
    dalle_openai_variables()  
      
    # Get the approach and whether it's a new chat thread from the request JSON  
    approach = (await quart.request.get_json())["approach"]  
    isNewChatThread = (await quart.request.get_json())["isNewChatThread"]  
      
    # Get user info from session if available  
    if session is not None:  
        AD_USER_INFO = session.get('AD_USER_INFO', {})  
    else:  
        AD_USER_INFO = {}  
      
    # Determine chat mode based on the approach  
    chatMode = "GEAGPT Chat"  
    if approach == "new":  
        chatMode = "Ask Legal"  
      
    try:  
        # Log the new chat thread if applicable  
        if isNewChatThread:  
            threadUrl = (await quart.request.get_json())["threadUrl"]  
            await cosmos_thread_logger(  
                (await quart.request.get_json())["session_id"],  
                chatMode,  
                (await quart.request.get_json())["current_question"],  
                threadUrl=threadUrl,  
            )  
          
        # Get the JSON data from the request  
        json_data = await quart.request.get_json()  
        name = json_data.get('name', None)  
          
        conf_params = {}  
          
        # Get the SQL parameters from the current user session  
        user_id = session['AD_USER_INFO'].get("UserID")  
        sql_params_key = f"{user_id}" + "_" + f"{name}"  
        usecase_sql_parmas = session.get(sql_params_key, None)  
        overrides = json_data.get("overrides") or {}  
        print("before usecase_sql_parmas========>",usecase_sql_parmas)
         ## call the sql server if usecase_sql_parmas is  none  and save them in the session else take it from session -------------
        if usecase_sql_parmas is None:
            usecase_sql_parmas = await get_usecase_parmaeters(name,sql_params_key)
        ## if it dont work than we will create contant files dependes on the usecase we will create usecase file. -----------------  
        print(" after usecase_sql_parmas========>",usecase_sql_parmas)
          
        # Creating GPT Config object to pass in run method  
        conf_params['semantic_captions'] = True if overrides.get("semantic_captions") else False  
        conf_params['frequency_penalty'] = overrides.get("frequency_penalty") or 0  
        conf_params['presence_penalty'] = overrides.get("presence_penalty") or 0  
        conf_params['exclude_category'] = overrides.get("exclude_category") or None  
        conf_params['prompt_template'] = overrides.get("prompt_template") or None  
          
        # Check if user modified the params, if not take from SQL DB  
        conf_params['max_token'] = overrides.get("max_tokens") if overrides.get("max_tokens") else usecase_sql_parmas.get('MaxResponseLength', None)  
        conf_params['top'] = overrides.get("top") if overrides.get("top") else usecase_sql_parmas.get('NumDocRAG', None)  
        conf_params['stop'] = overrides.get("stop") if overrides.get("stop") else usecase_sql_parmas.get('stopSequences', None)  
        conf_params['temperature'] = overrides.get("temperature") if overrides.get("temperature") else usecase_sql_parmas.get('temperature', 0)  
        conf_params['ResponsePromptFewShotExample'] = usecase_sql_parmas.get('fewShotExample', None)  
        conf_params['deploymentName'] = usecase_sql_parmas.get('deploymentName', None)  
          
        # Init method parameters  
        usecase_name = usecase_sql_parmas.get('use_case_name', None)  
        QueryPrompt = usecase_sql_parmas.get('QueryPrompt', None)  
        responsePrompt = usecase_sql_parmas.get('systemPrompt', None)  
        deployment_name = usecase_sql_parmas.get('deploymentName', None)  
        refine_user_query = usecase_sql_parmas.get('RefineUserQueryFlag', None)  
        ResponsePromptFewShotExample = usecase_sql_parmas.get('fewShotExample', None)  
          
        impl = ""  
        history = json_data["history"]  
        sessionId = json_data.get("session_id")  
        current_question = json_data.get("current_question")  
        session_instance_key = f"instance_{sessionId}"  
        current_instance = session.get(session_instance_key, None)  
          
        # Initialize the ChatReadRetrieveReadApproach_LC object if not already done  
        if current_instance is None:  
            print("inside if ==>")  
            impl = ChatReadRetrieveReadApproach_LC(  
                usecase_name,  
                AZURE_OPENAI_CHATGPT_O_API_VERSION,  
                deployment_name,  
                refine_user_query,  
                QueryPrompt,  
                responsePrompt,  
                ResponsePromptFewShotExample,  
                KB_FIELDS_SOURCEPAGE,  
                KB_FIELDS_CONTENT,  
                AD_USER_INFO  
            )  
            print("taking instance", impl)  
            session[session_instance_key] = impl  
        else:  
            print("inside else====>")  
            impl = current_instance  
          
        # Return an error if the implementation is unknown  
        if not impl:  
            return jsonify({"error": "unknown approach"}), 400  
          
        print("search client =======>", search_client)  
          
        # Run the implementation and return the response  
        return Response(impl.run(history, conf_params, sessionId, current_question, search_client), content_type='text/event-stream')  
      
    except Exception as e:  
        # Log and return the exception  
        logging.exception("Exception in /chat")  
        strE = str(e)  
        if "SyntaxError" in strE:  
            return quart.jsonify(  
                {"error": "Unfortunately, an error occurred while processing the response from GPT. Please try again."},  
            ), 500  
        return quart.jsonify({"error": str(e)}), 500  

# Define a route for the reactToMssage, which accepts POST requests
@app.route("/reactToMessage", methods=["POST"])
async def update_feedback():
    """
    Update the feedback for a message and return the response.
    """
    try:
        # Read the existing document
        message_id = (await quart.request.get_json())["message_id"]
        thumbAction = (await quart.request.get_json())["thumbAction"]
        # thumbAction - null/0/1  0-Dislike 1- Like Null- nothing
        query_params = {
            'query': 'SELECT * FROM c WHERE c.id = @message_id',
            'parameters': [
                {'name': '@message_id', 'value': message_id},
            ]
        }
        # Execute the query
        items = list(container.query_items(
            **query_params,
            enable_cross_partition_query=True
        ))

        if items:
            item = items[0]
            # item['thumbAction'] = thumbAction
            item['response']['thumbAction'] = thumbAction
            item['response']['id'] = message_id
            updated_item = container.replace_item(item=item, body=item)
            return quart.jsonify({'message': 'Document updated successfully',"updated_item":updated_item}), 200
        else:
            return quart.jsonify({'message': 'No document found with the provided message_id'}), 404
    except Exception as e:
        logging.exception("Exception in /ask")
        strE = str(e)
        return quart.jsonify({"error": str(e)}), 500

# Example usage

# Define a route for the audio page, which accepts POST requests
@app.route("/audio", methods=["POST"])
async def audio():
    """
    Transcribe the audio file and return the response.
    """
    try:
        if not await quart.request.files:
            return quart.jsonify({'error': 'No audio file provided in the request'}), 400

        audio_file = await quart.request.files.getlist('files')[0]

        # First we need to upload the audio file in some temporary directory
        if not os.path.exists("./audio"):
            os.makedirs("./audio")
        filename = audio_file.filename
        file_name = os.path.basename(filename)
        destination_path = os.path.join("./audio/", file_name)
        with open(destination_path, 'wb') as dest_file:
            while chunk := await audio_file.read():
                dest_file.write(chunk)

        # Whisper  REST API Call with help of process module
        curl_command = f'curl {WHISPER_API_ENDPOINT}/openai/deployments/{WHISPER_DEPLOYMENT_NAME}/audio/transcriptions?api-version=2023-09-01-preview \
        -H "api-key: {WHISPER_API_KEY}" \
        -H "Content-Type: multipart/form-data" \
        -F "file=@{destination_path}" '
        process = await asyncio.create_subprocess_shell(curl_command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)

        # Remove uploaded files from directory
        if os.path.exists(destination_path):
            os.remove(destination_path)
            print(f"File '{destination_path}' deleted successfully.")

        # Taking output from process module
        stdout, stderr = await process.communicate()
        output = stdout.decode()
        errors = stderr.decode()
        if errors:
            print("Errors:", errors)

        response_object = json.loads(output)
        return quart.jsonify(response_object)
    except Exception as e:
        logging.exception("Exception in /audio")
        strE = str(e)
        if "SyntaxError" in strE:
            return quart.jsonify({"error": "Unfortunately, an error occurred while processing the response from GPT. Please try again."}), 500
        return quart.jsonify({"error": str(e)}), 500


# Define a route for the pure page, which accepts POST requests
@check_menu_access
@app.route("/pure", methods=["POST"])
async def pure():
    """
        Chat using the specified approach and return the response.
    """
    ensure_openai_token()
    approach = (await quart.request.get_json())["approach"]
    isNewChatThread = (await quart.request.get_json())["isNewChatThread"]

    # try to get the implementation for the given approach and run them to return
    try:
        impl = chat_approaches.get(approach)
        if not impl:
            return quart.jsonify({"error": "unknown approach"}), 400
        if isNewChatThread == True:
            threadUrl = (await quart.request.get_json())["threadUrl"]
            await cosmos_thread_logger(
                (await quart.request.get_json())["session_id"],
                "Pure",
                (await quart.request.get_json())["current_question"],
                threadUrl=threadUrl,
            )

        # r = impl.run(
        #     (await quart.request.get_json())["history"],
        #     (await quart.request.get_json()).get("overrides") or {},
        # )
        session_instance_key = f"instance_{(await request.get_json())['session_id']}"
        removed_content = session.get(session_instance_key, None)
        if removed_content is None:
            print("inside if ==>")
            if approach=="vrrr":
                impl =  ChatVisionRetrieveReadApproach(AZURE_OPENAI_CHATGPT_DEPLOYMENT, Dalle_api_endpoint, Dalle_api_key)
            else:
                impl =  ChatPureReadRetrieveReadApproach(AZURE_OPENAI_CHATGPT_DEPLOYMENT, AZURE_OPENAI_CHATGPT_PLUS_DEPLOYMENT, AZURE_OPENAI_GPT_DEPLOYMENT)
            print("taking instance",impl)
            session[session_instance_key] = impl
        else:
            print("inside else====>")
            impl = removed_content
        json_data = await quart.request.get_json()
        history = json_data["history"]
        overrides = json_data.get("overrides") or {}
        sessionId = json_data.get("session_id")
        current_question = json_data.get("current_question")
        return Response(impl.run(history, overrides,sessionId,current_question),content_type='text/event-stream')
    except Exception as e:
        logging.exception("Exception in /pure")
        return quart.jsonify({"error": str(e)}), 500

# Define a route for the pureplus page, which accepts POST requests
@check_menu_access
@app.route("/pureplus", methods=["POST"])
async def pureplus():
    """
        Chat using the specified approach and return the response.
    """
    await ensure_openai_token()
    approach = (await quart.request.get_json())["approach"]
    # AD_USER_INFO = session['AD_USER_INFO']
    AD_USER_INFO = ""
    if session is not None:
        AD_USER_INFO = session.get('AD_USER_INFO', {})
    else:
        AD_USER_INFO = {}
    isNewChatThread = (await quart.request.get_json())["isNewChatThread"]
    # try to get the implementation for the given approach and run them to return
    try:
        impl = chat_approaches.get(approach)
        if not impl:
            return quart.jsonify({"error": "unknown approach"}), 400


        threadUrl = (await quart.request.get_json())["threadUrl"]
        if(approach=="vrrr"):
            print("inside vrrr approach====>")
            r = impl.run(
                (await quart.request.get_json())["history"],
                (await quart.request.get_json()).get("overrides") or {},
                GPT4VISION_ENDPOINT,
                GPT4VISION_KEY
            )
            if approach=="vrrr" and isinstance((await request.get_json())['current_question'],list) and len((await request.get_json())['current_question'])>1:
                await cosmos_thread_logger((await request.get_json())['session_id'],"Pure Plus",(await request.get_json())['current_question'][1],threadUrl=threadUrl)
            elif approach=="vrrr":
                await cosmos_thread_logger((await request.get_json())['session_id'],"Pure Plus",r["answer"],threadUrl=threadUrl)
            result = await cosmos_logger(
                (await quart.request.get_json())["session_id"],
                AD_USER_INFO,
                "Pure Plus",
                (await quart.request.get_json())["current_question"],
                r,
            )
            if result and result.get('id') is not None:
                r['messageID'] = result['id']
            return quart.jsonify(r)
        else:
            if isNewChatThread == True:
                threadUrl = (await quart.request.get_json())["threadUrl"]
                await cosmos_thread_logger(
                    (await quart.request.get_json())["session_id"],
                    "Pure Plus",
                    (await quart.request.get_json())["current_question"],
                    threadUrl=threadUrl,
                )
            impl = ""
            session_instance_key = f"instance_{(await request.get_json())['session_id']}_PurePlus"
            removed_content = session.get(session_instance_key, None)
            if removed_content is None:
                print("inside if ==>")
                impl =  ChatPureReadRetrieveReadApproach(AZURE_OPENAI_CHATGPT_DEPLOYMENT, AZURE_OPENAI_CHATGPT_PLUS_DEPLOYMENT, AZURE_OPENAI_GPT_DEPLOYMENT)
                print("taking instance",impl)
                session[session_instance_key] = 
            else:
                print("inside else====>")
                impl = removed_content
            json_data = await quart.request.get_json()
            history = json_data["history"]
            overrides = json_data.get("overrides") or {}
            sessionId = json_data.get("session_id")
            current_question = json_data.get("current_question")
            return Response(impl.runplus(history, overrides,sessionId,current_question,AD_USER_INFO),content_type='text/event-stream')
    except Exception as e:
        logging.exception("Exception in /pureplus")
        return quart.jsonify({"error": "Error: Azure Open AI has filtered this content as it doesn't comply with the guidelines and may belong to one of the harm categories"}), 500
        # return quart.jsonify({"error": str(e)}), 500

@check_menu_access
@app.route("/purepluso", methods=["POST"])
async def purepluso():
    """
        Chat using the specified approach and return the response.
    """
    await ensure_openai_token()
    approach = (await quart.request.get_json())["approach"]
    # AD_USER_INFO = session['AD_USER_INFO']
    AD_USER_INFO = ""
    if session is not None:
        AD_USER_INFO = session.get('AD_USER_INFO', {})
    else:
        AD_USER_INFO = {}
    isNewChatThread = (await quart.request.get_json())["isNewChatThread"]
    # try to get the implementation for the given approach and run them to return


    try:
        impl = chat_approaches.get(approach)
        if not impl:
            return quart.jsonify({"error": "unknown approach"}), 400

        threadUrl = (await quart.request.get_json())["threadUrl"]
        if(approach=="vrrr"):
            print("inside vrrr approach====>")
            r = impl.run(
                (await quart.request.get_json())["history"],
                (await quart.request.get_json()).get("overrides") or {},
                GPT4o_VISION_ENDPOINT,
                GPT4o_VISION_KEY
            )
            if approach=="vrrr" and isinstance((await request.get_json())['current_question'],list) and len((await request.get_json())['current_question'])>1:
                await cosmos_thread_logger((await request.get_json())['session_id'],"GPT 4o",(await request.get_json())['current_question'][1],threadUrl=threadUrl)
            elif approach=="vrrr":
                await cosmos_thread_logger((await request.get_json())['session_id'],"GPT 4o",r["answer"],threadUrl=threadUrl)
            result = await cosmos_logger(
                (await quart.request.get_json())["session_id"],
                AD_USER_INFO,
                "Pure Plus",
                (await quart.request.get_json())["current_question"],
                r,
            )
            if result and result.get('id') is not None:
                r['messageID'] = result['id']
            return quart.jsonify(r)
        else:
            impl = ""
            if isNewChatThread == True:
                threadUrl = (await quart.request.get_json())["threadUrl"]
                await cosmos_thread_logger((await request.get_json())['session_id'],"GPT 4o",(await request.get_json())['current_question'],threadUrl=threadUrl)
            session_instance_key = f"instance_{(await request.get_json())['session_id']}_PurePlus"
            removed_content = session.get(session_instance_key, None)
            if removed_content is None:
                print("inside if ==>")
                impl =  ChatPureReadRetrieveReadApproach(AZURE_OPENAI_CHATGPT_DEPLOYMENT, AZURE_OPENAI_CHATGPT_PLUS_DEPLOYMENT, AZURE_OPENAI_GPT_DEPLOYMENT)
                print("taking instance",impl)
                session[session_instance_key] = impl
            else:
                print("inside else====>")
                impl = removed_content
            json_data = await quart.request.get_json()
            history = json_data["history"]
            overrides = json_data.get("overrides") or {}
            sessionId = json_data.get("session_id")
            current_question = json_data.get("current_question")
            return Response(impl.runpluso(history, overrides,AZURE_OPENAI_CHATGPT_O_DEPLOYMENT,sessionId,current_question,AD_USER_INFO,isNewChatThread),content_type='text/event-stream')
    except Exception as e:
        logging.exception("Exception in /pureplus")
        return quart.jsonify({"error": "Error: Azure Open AI has filtered this content as it doesn't comply with the guidelines and may belong to one of the harm categories"}), 500

# # Define a route for the dalle page, which accepts POST requests
@check_menu_access
@app.route("/dalle", methods=["POST"])
async def dalle():
    """
        Chat using the specified approach and return the response.
    """
    dalle_openai_variables()
    AD_USER_INFO = session['AD_USER_INFO']
    
    approach = (await quart.request.get_json())["approach"]

    # try to get the implementation for the given approach and run them to return
    try:
        impl = image_approaches.get(approach)
        if not impl:
            return quart.jsonify({"error": "unknown approach"}), 400
        r = impl.run(
            (await quart.request.get_json())["prompt"],
            (await quart.request.get_json()).get("overrides") or {},
            (await quart.request.get_json()).get("isVariant") or False
        )
        user_prompt = str((await quart.request.get_json())["prompt"])

        revert_openai_variables()
        result =await cosmos_logger(
            (await quart.request.get_json())["session_id"],
            AD_USER_INFO['employeeOrgData'],
            "Dall-E",
            (await quart.request.get_json())["prompt"],
            r
        )
        print("result====>",result)
        if result and result.get('id') is not None:
            r['messageID'] = result['id']
        return quart.jsonify(r)
    except Exception as e:
        logging.exception("Exception in /dalle")

        revert_openai_variables()
        print(str(e))
        return quart.jsonify({"error": "Unfortunately, Microsoft is not yet ready for enabling this feature and GEA is waiting on them to activate it. 😥 🤦‍♂️💀"}), 500

# Define a route for the dalle3 page, which accepts POST requests
@check_menu_access
@app.route("/dalle3", methods=["POST"])
async def dalle3():
    """
        Chat using the specified approach and return the response.
    """
    # Set the OpenAI variables for DALL-E 3
    dalle3_openai_variables()

    # Get the user info from the session
    # AD_USER_INFO = session['AD_USER_INFO']
    if session is not None:
        AD_USER_INFO = session.get('AD_USER_INFO', {})
    else:
        AD_USER_INFO = {}

    # Get the approach from the request JSON
    approach = (await quart.request.get_json())["approach"]
    # Try to get the implementation for the given approach and run them to return
    try:
        impl = image_approaches.get(approach)
        if not impl:
            return quart.jsonify({"error": "unknown approach"}), 400
        r = impl.runDalle3(
            (await quart.request.get_json())["prompt"],
            (await quart.request.get_json()).get("overrides") or {},
            (await quart.request.get_json()).get("isVariant") or False,
            Dalle_api_key,
            Dalle_deployment
        )
        revert_openai_variables()
        result =await cosmos_logger(
            (await quart.request.get_json())["session_id"],
            # AD_USER_INFO['employeeOrgData'],
            "",
            "Dall-E",
            (await quart.request.get_json())["prompt"],
            r
        )
        if result and result.get('id') is not None:
            r['messageID'] = result['id']
        return quart.jsonify(r)
    except Exception as e:
        # Log any exceptions
        logging.exception(f"Exception in /dalle3 {str(e)}")
        print(str(e))
        return quart.jsonify({"error": "Unfortunately, Microsoft is not yet ready for enabling this feature and GEA is waiting on them to activate it. 😥 🤦‍♂️💀"}), 500


@app.route('/remove_instance',methods=["POST"])
async def remove_user_id():
    # Remove 'UserID' from the session
    session_id = (await quart.request.get_json()).get("session_id")
    session_instance_key = f"instance_{session_id}"
    session_id = session.pop(session_instance_key, None)  # Use pop method to avoid KeyError
    if session_instance_key is not None:
        return jsonify({"message": f"{session_instance_key} removed from session"}), 200
    else:
        return jsonify({"message": "session_instance_key not found in session"}), 404

# Define a route for the bing page, which accepts POST requests
@check_menu_access
@app.route("/bing", methods=["POST"])
async def bing():
    """
        Chat using the specified approach and return the response.
    """
   # Ensure the OpenAI token is set
    await ensure_openai_token()

    # Get the approach from the request JSON
    approach = (await quart.request.get_json())["approach"]

    # try to get the implementation for the given approach and run them to return
    try:
         # Get the user info from the session
        # AD_USER_INFO = session['AD_USER_INFO'] // Need to uncomment it
         # Check if it's a new chat thread
        if session is not None:
            AD_USER_INFO = session.get('AD_USER_INFO', {})
        else:
            AD_USER_INFO = {}
        isNewChatThread = (await quart.request.get_json())["isNewChatThread"]
        if isNewChatThread == True:
            threadUrl = (await quart.request.get_json())["threadUrl"]
            await cosmos_thread_logger((await quart.request.get_json())["session_id"],"Bing",(await quart.request.get_json())["current_question"],threadUrl=threadUrl)

        json_data = await quart.request.get_json()
        history = json_data["history"]
        overrides = json_data.get("overrides") or {}
        sessionId = json_data.get("session_id")
        current_question = json_data.get("current_question")
        conversationStyle = json_data.get("conversationStyle")
        session_instance_key = f"instance_{sessionId}"
        removed_content = session.get(session_instance_key, None)
        if removed_content is None:
            print("inside if ==>")
            impl =  BingSearchReadRetrive(AZURE_OPENAI_CHATGPT_O_DEPLOYMENT, AZURE_OPENAI_CHATGPT_O_API_VERSION,BING_SUBSCRIPTION_KEY,BING_SEARCH_ENDPOINT)
            print("taking instance",impl)
            session[session_instance_key] = impl
        else:
            print("inside else====>")
            impl = removed_content
        if not impl:
            return quart.jsonify({"error": "unknown approach"}), 400
        return Response(impl.run(history,current_question, overrides,conversationStyle,sessionId,current_question,AD_USER_INFO),content_type='text/event-stream')
    except Exception as e:
        # Log any exceptions
        logging.exception(f"Exception in /bing {str(e)}")

        revert_openai_variables()
        print(str(e))
        return quart.jsonify({"error": "Unfortunately, Microsoft is not yet ready for enabling this feature and GEA is waiting on them to activate it. 😥 🤦‍♂️💀"}), 500


@app.route("/getAllUseCases", methods=["GET"])
async def getAllUseCases():
    try:
        result =  sql_table_manager.getAllCases()
        return quart.jsonify(result), 200
    except Exception as e:
        logging.exception("Exception in /getAllUseCases", str(e))
        return quart.jsonify({"error": str(e)}), 500

@check_menu_access
@app.route("/data", methods=["POST"])
async def data_management():
    """
    Perform CRUD operations on the SQL table based on the provided action.
    """
    content_type = quart.request.content_type
    try:
        # Extract the action from the request
        if 'multipart/form-data' in content_type or 'application/x-www-form-urlencoded' in content_type:
            result = await sql_table_manager.process_docs(quart.request)
            return quart.jsonify(result), 200
        elif content_type == 'application/json':
            action = (await quart.request.get_json()).get("action")
        if action == "insert":
            # Call the insert_data method
            row = (await quart.request.get_json()).get("row")
            result =  sql_table_manager.insert_data(row)
            return quart.jsonify(result), 200
        elif action == "read":
            # Call the read_data method
            RoleId = (await quart.request.get_json()).get("RoleId")
            result =  sql_table_manager.read_data(RoleId)
            return quart.jsonify(result), 200
        elif action == "update":
            # Call the update_data method
            Questioid = (await quart.request.get_json()).get("QID")
            usecase = (await quart.request.get_json()).get("UsecaseID")
            team = (await quart.request.get_json()).get("team")
            question = (await quart.request.get_json()).get("question")
            ground_truth_answer = (await quart.request.get_json()).get("ground_truth_answer")
            result =  sql_table_manager.update_data(Questioid, usecase, team, question, ground_truth_answer)
            return quart.jsonify(result), 200
        elif action == "delete":
            # Call the delete_data method
            Questioid = (await quart.request.get_json()).get("QID")
            result =  sql_table_manager.delete_data(Questioid)
            return quart.jsonify(result), 200
        elif action == "insert_feedback":
            # Call the delete_data method
            data = (await quart.request.get_json()).get("data")
            result =  sql_table_manager.insert_feedback(data)
            return quart.jsonify(result), 200
        elif action == "get_evalutation":
            UsecaseID = (await quart.request.get_json()).get("UsecaseID")
            result =  sql_table_manager.getDataForEvaluation(UsecaseID)
            return quart.jsonify(result), 200

        else:
            return quart.jsonify({"message": "Invalid action"}), 400
    except Exception as e:
        logging.exception("Exception in /data", str(e))
        return quart.jsonify({"error": str(e)}), 500


@check_menu_access
@app.route("/ragasEvaluation", methods=["POST"])
async def ragasEval():
    try:
        content_type = quart.request.content_type
        if content_type == 'application/json':
            UsecaseID = (await quart.request.get_json()).get("UsecaseID")
            Functionality = (await quart.request.get_json()).get("Functionality")
            Comments = (await quart.request.get_json()).get("Comments")
            user_id = session['AD_USER_INFO'].get("UserID")
            UserId = user_id
            result = ragasEvaluation.run(UsecaseID, Functionality, Comments, UserId)
            return quart.jsonify(result), 200
        else:
            return quart.jsonify({"message": "Invalid content type"}), 400
    except Exception as e:
        logging.exception("Exception in /ragasEvaluation", str(e))
        return quart.jsonify({"error": str(e)}), 500

@check_menu_access
@app.route("/getAverageScore", methods=["POST"])
async def getAverageScore():
    try:
        UsecaseID = (await quart.request.get_json()).get("UsecaseID")
        result = ragasEvaluation.getAverageScore(UsecaseID)
        return quart.jsonify(result), 200
    except Exception as e:
        logging.exception("Exception in /data", str(e))
        return quart.jsonify({"error": str(e)}), 500
@check_menu_access
@app.route("/getRagasEvaluation", methods=["POST"])
async def getRagasEval():
    try:
        ragas_id = (await quart.request.get_json()).get("ragas_id")
        UsecaseID = (await quart.request.get_json()).get("UsecaseID")

        result = ragasEvaluation.get_results_by_ragas_id(ragas_id,UsecaseID)
        return quart.jsonify(result), 200
    except Exception as e:
        logging.exception("Exception in /data", str(e))
        return quart.jsonify({"error": str(e)}), 500
@app.route("/brazil_tax_codes", methods=["POST"])
async def brazil_tax_codes():
    """
    Generate the tax codes for Brazil and return the response.
    """
    content_type = quart.request.content_type
    if content_type == 'application/json':
        body = await quart.request.get_json()
        country = body.get("country")
        states = body.get("states")
        isJurisdiction = body.get("isJurisdiction")

        if isJurisdiction:
            r = brazil_jurisdiction.generate_tax_jurisdiction_tbl(country, states)
        else:
            r = brazil_jurisdiction.generate_custom_tbl(country, states)

        return quart.jsonify(r), 200
    else:
        return quart.jsonify({"message": "Invalid content type"}), 400

@app.route('/get_threads', methods=['GET'])
async def get_threads():
    """
    Get the chat threads from Cosmos DB.

    """
    try:
        user_id = session['AD_USER_INFO'].get("UserID")
        # Sample query parameters, adjust based on your requirements
        query_params = {
            'query': 'SELECT * FROM c WHERE c.user_id = @user_id AND c.isDeleted = @is_deleted ORDER BY c.timestamp',
            'parameters': [
                {'name': '@user_id', 'value': user_id},
                {'name': '@is_deleted', 'value': False},
            ]
        }
        # Execute the query
        results = await thread_container.query_items(**query_params, enable_cross_partition_query=True)

        # Convert results to a list and jsonify the response
        return jsonify(list(results))

    except Exception as e:
        logging.exception("Exception in get_threads() "+ str(e))
        return jsonify({"error": str(e)}), 500
# @app.route('/get_threads', methods=['GET'])
# async def get_threads():
#     """
#     Get the chat threads from Cosmos DB.

#     """
#     try:
#         user_id = session.get('AD_USER_INFO', {}).get("UserID")
#         # Sample query parameters, adjust based on your requirements
#         query_params = {
#             'query': 'SELECT * FROM c WHERE c.user_id = @user_id AND c.isDeleted = @is_deleted ORDER BY c.timestamp',
#             'parameters': [
#                 {'name': '@user_id', 'value': user_id},
#                 {'name': '@is_deleted', 'value': False},
#             ]
#         }
#         # Execute the query
#         results = await thread_container.query_items(**query_params, enable_cross_partition_query=True)

#         # Convert results to a list and jsonify the response
#         return quart.jsonify(list(results))

#     except Exception as e:
#         logging.exception("Exception in get_threads() "+ str(e))
#         return quart.jsonify({"error": str(e)}), 500

async def ensure_openai_token():
    """
    Function: ensure_openai_token
    Description: This function ensures that the OpenAI API key is set correctly.

    Parameters: None

    Returns: None
    """
    openai.api_key = OPENAI_API_KEY

def document_content_logger(session_document_key, content):
    try:
        if 'AD_USER_INFO' in session:
            user_id  = session['AD_USER_INFO'].get("UserID")
        else: user_id = "Ved Prakash Bhawsar"
        new_log = {
            "id": str(uuid4()),
            "user_id": user_id,
            "session_document_key": session_document_key,
            "content": content,
            "timestamp": str(datetime.utcnow())
        }
        logging.debug("Creating new document content log: %s", new_log)
        result = document_content_container.create_item(new_log)
        return result
    except Exception as e:
        logging.exception("Exception occurred in document_content_logger: %s", str(e))
        logging.exception(str(e)), 500

#@app.route("/thread_logger", methods=["POST"])
# @app.route("/thread_logger", methods=["POST"])
async def cosmos_thread_logger(chat_id, mode, name, threadUrl,storage=AZURE_STORAGE_CONTAINER, cogIndex=AZURE_SEARCH_INDEX,conversationStyle="precise",oaModel="gpt-4",filename=""):

    """
    Log the chat thread to Cosmos DB.
    """
    try:
        if 'AD_USER_INFO' in session:
            user_id  = session['AD_USER_INFO'].get("UserID")
        else: user_id = "Ved Prakash Bhawsar"
        # Create a new log entry with the provided data and additional fields
        new_log = {
            "id": chat_id,
            "user_id": user_id,
            "chat_mode": mode,
            "name": name,
            "threadUrl": threadUrl,
            "isDeleted": False,
            "model": oaModel,
            "filename": filename,
            "cogIndex": cogIndex,
            "storage": storage,
            "conversationStyle": conversationStyle,
            "type": "CHAT_THREAD",
            "timestamp": str(datetime.utcnow())
        }
        # Log the new entry to Cosmos DB
        logging.debug(new_log)

        thread_container.create_item(new_log)
        return quart.jsonify({"message": "success"})
    except Exception as e:
        logging.exception("Exception in /cosmos_thread_logger")
        print(str(e))
        logging.exception(str(e))
        return quart.jsonify({"error":str(e)}), 500


def get_document_content(session_document_key):
    try:
        # query = "SELECT * FROM c WHERE c.session_document_key = @session_document_key"
        # parameters = [{"name": "@session_document_key", "value": session_document_key}]

        query_params = {

            "query" : 'SELECT * FROM c WHERE c.session_document_key = @session_document_key',
            'parameters' : [{"name": "@session_document_key", "value": session_document_key}]

        }
        # Execute the query
        results = document_content_container.query_items(**query_params,enable_cross_partition_query=True)

        # Convert results to a list and jsonify the response

        return list(results)

    except Exception as e:
        logging.exception("Exception in get_threads() "+ str(e))
    return []
@app.route('/get_chat_threads/<name>', methods=['GET'])
async def chat_threads(name):
    """
    Retrieve chat threads for a specific user.

    This function retrieves the user ID from the session and uses it to query the thread container in Cosmos DB.
    It selects all documents where the user_id matches the retrieved user ID and isDeleted is False, ordered by the timestamp.
    The results are converted to a list and returned.
    If an exception occurs during the process, it logs the exception and returns an empty list.

    Returns:
        list: A list of chat threads for the user. If an exception occurs, an empty list is returned.
    """
    try:
        user_id = session['AD_USER_INFO'].get("UserID")
        print('name===>',name)
        decoded_name = unquote(name)
        print("decoded_name=====>",decoded_name)
        # Sample query parameters, adjust based on your requirements
        query_params = {
        # Sample query parameters, adjust based on your requirements  query_params = {
            'query': 'SELECT * FROM c WHERE c.user_id = @user_id AND c.chat_mode = @chat_mode AND c.isDeleted = @is_deleted ORDER BY c.timestamp',
            'parameters': [
                {'name': '@user_id', 'value': user_id},
                {'name': '@chat_mode', 'value': decoded_name},
                {'name': '@is_deleted', 'value': False},
            ]
        }


        # Execute the query
        results = thread_container.query_items(**query_params, enable_cross_partition_query=True)

        # Await the result of each map_object call and collect the results
        threads = [await map_object(item) for item in results]
        # Convert results to a list and return the response
        return list(threads)

    except Exception as e:
        logging.exception("Exception in chat_threads() " + str(e))
        return []

@app.route('/get_thread_chats/<chat_session_id>', methods=['GET'])
async def get_thread_chats(chat_session_id):
    """
    Get the chat thread chats from Cosmos DB.
    Parameters:
        chat_session_id (str): The chat session id.
    """
    try:
        #chat_session_id = request.json["chat_session_id"]
        # Sample query parameters, adjust based on your requirements
        query_params = {
            'query': 'SELECT * FROM c WHERE c.chat_session_id = @chat_session_id ORDER BY c.timestamp desc',
            'parameters': [
                {'name': '@chat_session_id', 'value': chat_session_id},
                {'name': '@is_deleted', 'value': False},
            ]
        }
        # Execute the query
        results = list(container.query_items(**query_params))
        # Convert results to a list and jsonify the response
        data = list(results)
        return quart.jsonify({"thread_chats": data})

    except Exception as e:
        logging.exception("Exception in /get_thread_chats")
        return quart.jsonify({"error": str(e)}), 500

@app.route("/legal_chats", methods=["POST"])
async def cosmos_legalchat():
    """
    Handle a request to log a legal chat to Cosmos DB.

    This function retrieves the user ID from the session or defaults to a specific user ID if not found.
    It then extracts the chat ID, query, response, and legal team from the request JSON.
    A new entry is created with these details, along with a unique ID, an empty question embedding, the reviewer (same as the user), and the current timestamp.
    This new entry is logged and added to the legal chat container in Cosmos DB.
    If the operation is successful, it returns a success message.
    If an exception occurs during the process, it logs the exception and returns a 500 error with the exception message.

    Returns:
    json: A JSON object containing the result of the operation. It could be a success message or an error message.
    """
    try:
        if 'AD_USER_INFO' in session:
            user_id  = session['AD_USER_INFO'].get("UserID")
        else: user_id = "Ved Prakash Bhawsar"

        # Get the chat ID, query, response, and legal team from the request JSON
        chat_id = (await quart.request.get_json())["id"]
        query = (await quart.request.get_json())["query"]
        response = (await quart.request.get_json())["response"]
        legal_team = (await quart.request.get_json())["legal_team"]
        new_entry = {
            "id": str(uuid4()),
            "question_id":chat_id,
            "user_id": user_id,
            "question": query,
            "answer": response,
            "legal_team": legal_team,
            "question_embedding":"",
            "reviewed_by":user_id,
            "timestamp": str(datetime.utcnow())
        }

        # Log the new entry to Cosmos DB and add the response to the legal chat container
        logging.debug(new_entry)
        legalchat_container.create_item(new_entry)
        return quart.jsonify({"message": "success"})
    except Exception as e:
        logging.exception("Exception in /legal_chats "+str(e))
        print(str(e))
        logging.exception(str(e))
        return quart.jsonify({"error":str(e)}), 500

#@app.route("/logger", methods=["POST"])
async def cosmos_logger(chat_id,employeeOrgData, mode, prompt, reply,talk=None,legal_team=None):
    """
    Log the chat to Cosmos DB.
    """
    try:
        # Create a new log entry with the provided data and additional fields
        new_log = {
                "id": str(uuid4()),
                "chat_session_id": chat_id,
                "employeeOrgData":employeeOrgData,
                "chat_mode": mode,
                "query": prompt,
                "response": reply,
                "Type": "CHAT",
                "timestamp": str(datetime.utcnow()),
                "talk": talk
            }

        new_log['response']['thumbAction'] = None
        new_log['response']['id'] = new_log['id']
        # if talk or legal_team is provided, add them to the log entry
        if talk is not None:
            new_log.setdefault("talk", talk)
        if legal_team is not None:
            new_log.setdefault("legal_team", legal_team)

        logging.debug(new_log)
        result =  container.create_item(new_log)
        return result
    except Exception as e:
        logging.exception("Exception in /logger")
        print(str(e))
        logging.exception(str(e))
        return quart.jsonify({"error":str(e)}), 500

@app.route("/legal_chats/<legal_team>", methods=["GET"])
async def get_legal_chats(legal_team):
    """
    Get the chats for the specified legal team.
    Parameters:
        legal_team (str): The legal team to filter the chats by.
    """
    try:
        #chat_session_id = request.json["chat_session_id"]
        # Sample query parameters, adjust based on your requirements
        if legal_team == "all":
            # If the legal team is "all", select all chats where the legal team is not null
            query_params = {
                'query': "SELECT c.id,c.query, c.response.answer as response, c.response.legal_team as legal_team, c.chat_mode, c.timestamp  FROM c WHERE c.response.legal_team != null ORDER BY c._ts desc",
                'parameters': [
                    {'name': '@is_deleted', 'value': False},
                ]
            }
        # Otherwise, select all chats where the legal team matches the provided legal team
        else:
            query_params = {
                'query': 'SELECT c.id,c.query, c.response.answer as response, c.response.legal_team as legal_team, c.chat_mode, c.timestamp FROM c WHERE c.response.legal_team = @legal_team ORDER BY c._ts desc',
                'parameters': [
                    {'name': '@legal_team', 'value': legal_team},
                    {'name': '@is_deleted', 'value': False},
                ]
            }

        # Execute the query
        results = container.query_items(**query_params,enable_cross_partition_query=True)

        # Convert results to a list and jsonify the response
        data = list(results)
        return quart.jsonify({"chats": data})

    except Exception as e:
        logging.exception("Exception in /get_thread_chats")
        return quart.jsonify({"error": str(e)}), 500

@app.route("/legal_approved_chats/<legal_team>", methods=["GET"])
async def get_legal_approved_chats(legal_team):
    """
    Get the approved chats for the specified legal team.
    Parameters:
        legal_team (str): The legal team to filter the chats by.
    """
    try:
        #chat_session_id = request.json["chat_session_id"]
        # Sample query parameters, adjust based on your requirements
        if legal_team == "all":
            # If the legal team is "all", select all approved chats where the legal team is not null
            query_params = {
                'query': "SELECT c.id,c.question as query, c.answer as response, c.legal_team, c.timestamp  FROM c WHERE c.legal_team != null ORDER BY c._ts desc",
                'parameters': [
                    {'name': '@is_deleted', 'value': False},
                ]
            }
            # Otherwise, select all approved chats where the legal team matches the provided legal team
        else:

            query_params = {
                'query': 'SELECT c.id,c.question as query, c.answer as response, c.legal_team, c.timestamp FROM c WHERE c.legal_team = @legal_team ORDER BY c._ts desc',
                'parameters': [
                    {'name': '@legal_team', 'value': legal_team},
                    {'name': '@is_deleted', 'value': False},
                ]
            }

        # Execute the query
        results = await legalchat_container.query_items(**query_params,enable_cross_partition_query=True)

        # Convert results to a list and jsonify the response
        data = list(results)
        return quart.jsonify({"chats": data})

    except Exception as e:
        logging.exception("Exception in /get_thread_chats")
        return quart.jsonify({"error": str(e)}), 500

@app.route("/revert_openai_variables", methods=["GET"])
async def revert_openai_variables():
    """
    Function: revert_openai_variables
    Description: This function reverts the OpenAI API variables to their default settings.
                 It configures the base URL, API version, API key, and ensures the OpenAI token is valid.

    Parameters: None

    Returns: JSON object with message indicating the OpenAI API variables have been reverted
    """

    # Setting up openai variable to work with Dall-E
    openai.api_base = f"https://{AZURE_OPENAI_SERVICE}.openai.azure.com"
    openai.api_version = "2023-03-15-preview"
    openai.api_key = OPENAI_API_KEY
    ensure_openai_token()

    return quart.jsonify({"message": "OpenAI API variables have been reverted"})


@app.route("/dalle_openai_variables", methods=["GET"])
async def dalle_openai_variables():
    """
    Function: dalle_openai_variables
    Description: This function sets up the necessary variables to work with the DALL-E model on the OpenAI API.
                 It configures the API type, base URL, API version, and API key.

    Parameters: None

    Returns: JSON object with message indicating the DALL-E OpenAI API variables have been set
    """
    # Setting up openai variable to work with Dall-E
    openai.api_type = "azure"
    openai.api_base = f"https://{AZURE_OPENAI_SERVICE}.openai.azure.com/"
    openai.api_version = "2023-12-01-preview"
    openai.api_key = OPENAI_API_KEY

    return quart.jsonify({"message": "DALL-E OpenAI API variables have been set"})


@app.route("/dalle3_openai_variables", methods=["GET"])
async def dalle3_openai_variables():
    """
    Function: dalle3_openai_variables
    Description: This function sets up the necessary variables to work with the DALL-E 3 model on the OpenAI API.
                 It configures the API type, base URL, API version, and API key.

    Parameters: None

    Returns: JSON object with message indicating the DALL-E OpenAI API variables have been set
    """
    # Setting up openai variable to work with Dall-E
    openai.api_type = "azure"
    openai.api_base = Dalle_api_endpoint
    openai.api_version = "2023-12-01-preview"
    openai.api_key = Dalle_api_key

    return quart.jsonify({"message": "DALL-E OpenAI API variables have been set"})


@app.route("/ensure_openai_token", methods=["GET"])
async def ensure_openai_token():
    """
    Function: ensure_openai_token
    Description: This function ensures that the OpenAI API key is set correctly.

    Parameters: None

    Returns: JSON object with message indicating the OpenAI API key is set correctly
    """
    # Setting up openai variable to work with Dall-E
    openai.api_key = OPENAI_API_KEY

    return quart.jsonify({"message": "OpenAI API key is set correctly"})

async def map_object(original_object):
    """
    Function: map_object
    Description: This function maps the properties of the original object to a new object with specific property names.

    Parameters:
    original_object (dict): The original object to be mapped.

    Returns:
    dict: The mapped object with specific property names.
    """
    # Create a new dictionary and map the properties of the original object to it
    mapped_object = {
        "Name": original_object["name"],
        "Id": original_object["id"],
        "IsDeleted": original_object["isDeleted"],
        "UserId": original_object["user_id"],
        "ThreadUrl": original_object["threadUrl"],
        "Filename": original_object["filename"],
        "ChatModel": original_object["model"],
        "CogIndex": original_object["cogIndex"],
        "ConversationStyle": original_object["conversationStyle"],
        "ChatType": original_object["type"],
        "ChatMode": original_object["chat_mode"],
        "Timestamp": original_object["timestamp"]
    }

    return mapped_object


@app.route("/get_queue/<queue_id>", methods=["GET"])
async def get_queue(queue_id):
    """
    Function: get_queue
    Description: This function retrieves a queue by its ID. If the queue does not exist, it creates a new one.

    Parameters:
    queue_id (str): The ID of the queue to retrieve.

    Returns:
    quart.jsonify: The queue associated with the given ID.
    """
    # queue_id = request.id
    if queue_id not in queues:
        queues[queue_id] = queue.Queue()
    return quart.jsonify({"queue": queues[queue_id]})


async def get_user_details(access_token):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        # "User-Agent": USER_AGENT, # Make sure to define USER_AGENT or remove this line
    }
    try:
        user_info = {}

        async with httpx.AsyncClient() as client:
            response_me = await client.get(GRAPH_API_ENDPOINT, headers=headers)
            response_group = await client.get(GRAPH_GROUP_ENDPOINT, headers=headers)
            response_property = await client.get(GRAPH_Property_ENDPOINT, headers=headers)

            print("response_me=======>", response_me)
            print("response_property=======>", response_property)

            if response_me.status_code == 200:
                user_data = response_me.json()
                user_info = {
                    "UserID": user_data.get("id"),
                    "FullName": user_data.get("displayName"),
                    "Email": user_data.get("mail"),
                }

                if response_group.status_code == 200:
                    group_data = response_group.json()
                    user_groups = [
                        {
                            "GroupId": group.get("id"),
                            "GroupName": group.get("displayName")
                        }
                        for group in group_data["value"]
                    ]
                    user_info["groups"] = user_groups

                    property_data = response_property.json()
                    user_info['employeeOrgData'] = {
                        'employeeOrgData': property_data.get('employeeOrgData'),
                        'department': property_data.get('department')
                    }
                else:
                    raise Exception(response_group.text)
            else:
                raise Exception(response_me.text)

            print("User Info=======>", user_info)
            return user_info

    except Exception as e:
        app.logger.exception(f"Failed to retrieve user data. {str(e)}")
        return jsonify({}), 500

if __name__ == "__main__":
    """
    This is the entry point of the Python script.
    It checks if the script is being run directly (not imported),
    and if so, it starts the Flask application.
    """
    app.run()
    #app.run(debug=True, threaded=True)