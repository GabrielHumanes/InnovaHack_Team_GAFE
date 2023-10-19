from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.callbacks.manager import CallbackManager
from langchain.llms import LlamaCpp
from flask import Flask, render_template, request, jsonify
from typing import Dict, Any


app = Flask(__name__)

class ChatApp:
    """
    Clase que representa la aplicación de chat.

    Attributes:
        projectId (str): ID del proyecto de Vertex AI.
        embedding_model (TextEmbeddingModel): Modelo de incrustación de texto.
        df (pd.DataFrame): DataFrame que contiene el conjunto de datos.
        embedding_length (int): Tamaño de la incrustación de texto.
        record_count (int): Número de registros en el conjunto de datos.
        dataset (np.ndarray): Conjunto de datos normalizado.
        searcher: Objeto ScaNN para búsqueda de similitud en el conjunto de datos.
        chat_model (ChatModel): Modelo de chat preentrenado.
        parameters (Dict[str, Any]): Parámetros para la generación de respuestas del chat.
    """
    def __init__(self):
        callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
        self.llm = LlamaCpp(
                            model_path = "/home/models/llm/llama2/llama-2-7b-chat.ggmlv3.q8_0.bin",
                            n_ctx = 6000,
                            n_gpu_layers = 512,
                            n_batch = 30,
                            callback_manager=callback_manager,
                            temperature = 0.5,
                            max_tokens = 4095,
                            n_parts = 1
                            )
        
        self.model_answer = ""

    def chat_handler(self) -> Dict[str, Any]:
        """
        Maneja las solicitudes de chat y genera respuestas utilizando el modelo de chat.

        Returns:
            Dict[str, Any]: Respuesta formateada del modelo de chat.

        <s>[INST] <<SYS>>
        {{ system_prompt }}
        <</SYS>>

        {{ user_msg_1 }} [/INST] {{ model_answer_1 }} </s><s>[INST] {{ user_msg_2 }} [/INST]
        """

        # Obtener la pregunta del formulario enviado
        question = request.form.get('question')
        if not question:
            return jsonify(error="No se proporcionó ninguna pregunta.")

        system_prompt = f"""<s>[INST] Hablarás en español de España, en castellano siempre.
        Sus respuestas no deben incluir ningún contenido nocivo, poco ético, racista, sexista, tóxico, peligroso o ilegal.
        Asegúrese de que sus respuestas sean socialmente imparciales y de naturaleza positiva.
        Si una pregunta no tiene sentido o no es coherente con los datos que queremos obtener, explica por qué en lugar de responder algo que no es correcto.
        Si no sabes la respuesta a una pregunta, por favor, no compartas información falsa. Si ya tienes toda la información finaliza amablemente la conversación. <</SYS>>
        
        """
        
        user_msg = question
        self.instance_conversation = system_prompt
        self.instance_conversation += f"<s>[INST] {user_msg} [/INST] </s>"
        self.instance_conversation += f" {self.model_answer} </s>"

        self.model_answer = self.llm(f"{self.instance_conversation} </s>",)
        return jsonify(response = self.model_answer)
    
    
@app.route('/api_healthcheck', methods=['GET'])
def api_healthcheck():
    return jsonify(status="ok")


@app.route('/')
def index():
    return render_template('index.html')


APP = ChatApp()


@app.route('/chat', methods=['POST'])
def chat():
    """
    Manejador de la ruta '/chat' que responde a las solicitudes POST de chat.

    Returns:
        Flask.response_class: Respuesta JSON que contiene la respuesta del modelo de chat.
    """
    return APP.chat_handler()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8034, debug=True)