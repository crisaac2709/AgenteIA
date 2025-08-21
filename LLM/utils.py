#Utilitario de conexión OpenAI
from langchain_openai import ChatOpenAI

#Utilitario para crear la memoria a corto plazo del modelo
from langchain.memory import ConversationBufferMemory, ConversationTokenBufferMemory

#Utilitario para usar el modelo de OpenAI para que le de representación numérica a nuestros textos
from langchain.embeddings import OpenAIEmbeddings

#Utilitario para vectorizar sobre Chroma
from langchain.vectorstores import Chroma

#Utilitario para crear un chat que incluya bases de conocimientos
from langchain.chains import RetrievalQA

#Librería de ChromaDB
import chromadb

#Utilitario de LangChain para cargar documentos
from langchain.document_loaders import TextLoader

#Utilitario para crear chunks
from langchain.text_splitter import CharacterTextSplitter

#Utilitario para usar el modelo de OpenAI para que le de representación numérica a nuestros textos
from langchain.embeddings import OpenAIEmbeddings
from langchain.embeddings import HuggingFaceEmbeddings


#Utilitario para vectorizar sobre Chroma
from langchain.vectorstores import Chroma

#Librería de manipulación de archivos PDF
import fitz

#Librería para manipular el sistema operativo
import os

#Librería para manipular el sistema operativo
import shutil

#Utilitario para leer el binario de una imagen
import base64

#Utilitario para enviar mensajes más complejos
from langchain_core.messages import HumanMessage



from dotenv import load_dotenv

load_dotenv()

#Obtiene el modelo
def obtenerLlm():
    llm = ChatOpenAI(
        model = os.getenv('MODEL_NAME'),
        api_key = os.getenv('OPENAI_API_KEY'),
        base_url = os.getenv('URL'),
        temperature = 0.2,
        max_tokens = 1000,
    )
    
    return llm


# Obtener modelo para hacer embeddings
def obtenerLlmEmbedding():
    llmEmbedding = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )
    
    return llmEmbedding


# Enviar imagen al modelo
def enviarImagenHaciaModelo(llm, consulta, rutaDeImagen):
    #Variable que almacena imagen como binario
    imagenBin = None
    
    with open(rutaDeImagen, 'rb') as archivo:
        #Leemos el archivo de imagen
        imagen = archivo.read()
        
        #Obtenemos el binario de la imagen
        imagenBin = base64.b64encode(imagen).decode('utf-8')
        
    #Contruimos el JSON del mensaje
    mensaje = HumanMessage(
        content = [
            {
                "type" : "text",
                "text" : consulta
            },
            {
                "type" : "image_url",
                "image_url": {
                    "url" : f"data:image/jpeg;base64,{imagenBin}"
                }
            }
        ]
    )
    
    # Enviamos un mensaje
    respuesta = llm.invoke([mensaje])
    # Devolvemos la respuesta
    return respuesta.content


# Extraer textos desde PDF sin OCR
def extraerTextoDePDF(rutaDePDF, rutaDeTxt):
    texto = ''
    
    # Abrimos el archivo con fitz
    with fitz.open(rutaDePDF) as PDF:
        
        # Recorremos cada pagina del PDF
        for pagina in PDF:
            textoDePagina = pagina.get_text()
            
            # Acumulamos el texto
            texto = texto + textoDePagina + " "
            
    # Abrimos el archivo txt en modo escritura con el encoding UTF-8
    with open(rutaDeTxt, 'w', encoding='utf-8') as archivo:
        #Escribimos el texto en el archivo
        archivo.write(texto)
        
        
#Extrae textos desde PDFs con OCR
def extraerTextosDePdfConOCR(rutaDePdf, rutaDeTxt, rutaDeImagenes, llm):

  #Si el directorio existe, lo borramos
  if os.path.exists(rutaDeImagenes):
    shutil.rmtree(rutaDeImagenes)

  #Creamos el directorio en donde se guardará cada página del documento como una imagen
  os.mkdir(rutaDeImagenes)

  #Variable que determina el número de página que se está procesando
  numeroDePagina = 1

  #Lista que acumula en orden las rutas de las imágenes
  rutasDeImagenes = []

  #Abrimos el archivo
  with fitz.open(rutaDePdf) as pdf:

    #Recorremos cada página del archivo
    for pagina in pdf:

      #Obtenemos la página como imagen
      imagen = pagina.get_pixmap()

      #Definimos la ruta y nombre de la imagen que se almacenará
      rutaDeImagen = f"{rutaDeImagenes}/pagina_"+str(numeroDePagina)+".jpg"

      #Agregamos la ruta de imagen
      rutasDeImagenes.append(rutaDeImagen)

      #Almacenamos la imagen en formato JPG
      imagen.save(rutaDeImagen, "JPEG")

      #Aumentamos el numero de pagina
      numeroDePagina = numeroDePagina + 1

  #Variable que acumula los textos extraidos
  textos = ""

  #Iteramos las imágenes para procesarlos
  for ruta in rutasDeImagenes:
    print(f"Analizando imagen: {ruta}")

    #Obtenemos la descripción de imágenes
    descripcionDeImagen = enviarImagenHaciaModelo(llm, "Eres un OCR, dame los textos que veas, también, si hay imágenes, agrega un texto que las describa", ruta)

    #Agregamos la descripción de la imagen
    textos = textos + " " + descripcionDeImagen

  #Abrimos el archivo en modo escritura con el encoding UTF-8
  with open(rutaDeTxt, "w", encoding="utf-8") as archivo:
      #Escribimos el texto en el archivo
      archivo.write(textos)
      
      
    
#Crea una base de conocimiento con una colección
def crearBaseDeConocimiento(ruta, coleccion):
  
  if os.path.exists(ruta):
    shutil.rmtree(ruta)
    
  #Creamos una base de conocimiento y obtenemos el cliente conectado a ella
  cliente = chromadb.PersistentClient(
    path = ruta
  )

  #Cremos una colección para guardar la información de los cursos
  coleccion_informacion_cursos = cliente.get_or_create_collection(
    name = coleccion
  )
  
  

#Carga documentos a la base de conocimiento
def cargarDocumentosEnBaseDeConocimiento(rutaDeDocumentos, rutaDeBaseDeConocimiento, coleccion, llmEmbedding):
  #Variable que acumula el contenido de los documentos
  contenidoDeDocumentos = []

  #Bucle de lectura del contenido de los documentos
  for ruta in rutaDeDocumentos:

    #Definimos el cargador del documento
    loader = TextLoader(
      file_path = ruta,
      encoding = "utf-8"
    )

    #Leemos el documento
    documento = loader.load()

    #Agregamos el contenido
    contenidoDeDocumentos = contenidoDeDocumentos + documento

  #Defininmos el cortador de chunks
  cortador = CharacterTextSplitter(
    chunk_size = 1000,
    chunk_overlap = 100
  )

  #Creamos los chunks
  chunks = cortador.split_documents(contenidoDeDocumentos)

  #Nos conectamos a la base de conocimiento en donde escribiremos
  db = Chroma.from_documents(
      documents = chunks,
      embedding = llmEmbedding,
      persist_directory = rutaDeBaseDeConocimiento,
      collection_name = coleccion
  )

  #Ejecutamos el almacenamiento
  db.persist()
  
  

#Obtiene una base de conocimiento
def obtenerBaseDeConocimiento(rutaDeBaseDeConocimiento, coleccion, llmEmbedding):
  #Nos conectamos a la base de conocimiento
  db = Chroma(
      embedding_function = llmEmbedding,
      persist_directory = rutaDeBaseDeConocimiento,
      collection_name = coleccion
  )

  #Creamos la conexión de base de conocimiento para ser usada por algún llm
  baseDeConocimiento = db.as_retriever()

  return baseDeConocimiento


"""
#Crea una sesión de chat
def crearSesionDeChat(llm, personalidad, baseDeConocimiento):
  #Creamos la memoria a corto plazo
  memoria = ConversationBufferMemory()

  #Agregamos la "personalidad" a nuestra IA
  memoria.chat_memory.add_ai_message(personalidad)

  #Creación del chat avanzado
  chat = RetrievalQA.from_chain_type(
      llm = llm,
      chain_type = "stuff",
      retriever = baseDeConocimiento,
      memory = memoria
  )

  return chat



#Envia un mensaje al chat
def enviarMensajeAlChat(chat, mensaje):

  #Envíamos el mensaje
  respuesta = chat.invoke(mensaje)

  #Devolvemos la respuesta
  return respuesta["result"]
  
"""


from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate

QA_RULES = """Responde SOLO con lo que esté en CONTEXTO.
Si el contexto es insuficiente, responde exactamente:
"Fuera de alcance de la base de conocimiento"."""

PROMPT = ChatPromptTemplate.from_messages([
    ("system", "{system_prompt}"),
    ("human", "Pregunta: {question}\n\nCONTEXTO:\n{context}\n\nRespuesta en español:")
])

def crearSesionDeChat(llm, personalidad, retriever):
    mem = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        input_key="question",   # 👈 qué campo es la entrada del usuario
        output_key="answer"     # 👈 qué campo guardar en memoria
    )

    system_prompt = (personalidad or "") + "\n\n" + QA_RULES

    chat = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        combine_docs_chain_kwargs={
            "prompt": PROMPT.partial(system_prompt=system_prompt)
        },
        memory=mem,
        return_source_documents=True
    )
    return chat

def enviarMensajeAlChat(chat, mensaje):
    out = chat.invoke({"question": mensaje})   # 👈 usa "question"
    if not out.get("source_documents"):
        return "Fuera de alcance de la base de conocimiento."
    return out.get("answer") or "Fuera de alcance de la base de conocimiento."
