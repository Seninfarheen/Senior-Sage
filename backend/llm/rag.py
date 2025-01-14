from langchain.chains import RetrievalQA
from langchain_community.llms import OpenAI
import openai
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
import PyPDF2
import os
from dotenv import load_dotenv
import pickle


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI()

# Extract text from PDF
def extract_text_from_pdf(file_path):
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text

# Chunk text and include metadata
def chunk_text_with_metadata(text, file_name, chunk_size=1000, overlap=200):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap
    )
    chunks = text_splitter.split_text(text)
    metadata = [{"source": file_name}] * len(chunks)
    return chunks, metadata

# Create vector database with metadata
def create_vector_db_with_metadata(text_chunks, metadata):
    embeddings = OpenAIEmbeddings()
    vector_db = FAISS.from_texts(text_chunks, embeddings, metadatas=metadata)
    return vector_db

def create_vector_db(SAVE_DIR):
    pdf_directory = os.path.join(BASE_DIR, "documents")
    all_chunks = []
    all_metadata = []

    for filename in os.listdir(pdf_directory):
        if filename.endswith('.pdf'):
            text = extract_text_from_pdf(os.path.join(pdf_directory, filename))
            chunks, metadata = chunk_text_with_metadata(text, filename)
            all_chunks.extend(chunks)
            all_metadata.extend(metadata)

    vector_db = create_vector_db_with_metadata(all_chunks, all_metadata)
    save_vector_db(vector_db, all_metadata, SAVE_DIR)

    return vector_db

# Save the FAISS index and metadata
def save_vector_db(vector_db, metadata, save_dir):
    os.makedirs(save_dir, exist_ok=True)
    vector_db.save_local(save_dir)  # Save the FAISS index
    with open(os.path.join(save_dir, "metadata.pkl"), "wb") as f:
        pickle.dump(metadata, f)

# Load the FAISS index and metadata
def load_vector_db(save_dir, embeddings):
    vector_db = FAISS.load_local(save_dir, embeddings, allow_dangerous_deserialization=True)
    with open(os.path.join(save_dir, "metadata.pkl"), "rb") as f:
        metadata = pickle.load(f)
    vector_db.metadatas = metadata  # Restore metadata
    return vector_db

def get_context(vector_db, query):
    retriever = vector_db.as_retriever()
    results = retriever.invoke(query)
    answer = results[0].page_content
    source = results[0].metadata["source"]
    return f"According to {source}, {answer}"

def get_answer(user_input, context):
    system_prompt = f"""
    You are an assistant to help answer any questions the user might have. The users are older in age, and will be asking you health related questions, use your knowledge to answer their queries in 
    a compasionate manner. FInd relevant information about the quesries in CONTEXT and customise your answer to the USER_QUERY based on that.
    Dont add anything new apart from the information found in CONTEXT. Also present the source of your answer, that can be found in CONTEXT also.

    USER_QUERY = {user_input}
    CONTEXT = {context}
    """

    completion = client.chat.completions.create(
        model = "gpt-4o-mini",
        messages = [
            {"role": "system", "content" : system_prompt}
        ]
    )

    response = completion.choices[0].message.content

    return response

if __name__ == "__main__":
# while(True):
    # pdf_directory = os.path.join(BASE_DIR, "documents")
    # all_chunks = []
    # all_metadata = []

    # for filename in os.listdir(pdf_directory):
    #     if filename.endswith('.pdf'):
    #         text = extract_text_from_pdf(os.path.join(pdf_directory, filename))
    #         chunks, metadata = chunk_text_with_metadata(text, filename)
    #         all_chunks.extend(chunks)
    #         all_metadata.extend(metadata)

    # vector_db = create_vector_db_with_metadata(all_chunks, all_metadata)

    SAVE_DIR = os.path.join(BASE_DIR, "vector_db")
    if os.path.exists(SAVE_DIR):
        embeddings = OpenAIEmbeddings()
        vector_db = load_vector_db(SAVE_DIR, embeddings)
    else:
        vector_db = create_vector_db(SAVE_DIR)


    while(True):
        query = input("\nWhat is your question: ")
        if query == "STOP":
            break
        context = get_context(vector_db, query)
        print(context, "\n\n")
        response = get_answer(query, context)
        print(response)
