**Nexa** is a voice- and text-enabled AI assistant designed using Streamlit, LangChain, and the Ollama LLM with the LLaMA3 model. This intelligent assistant supports natural conversation with users and provides spoken responses using text-to-speech capabilities. Users can interact with Nexa in two modes — either by typing or speaking — and toggle between these modes at any time using a simple UI button. The app listens to voice input via a microphone using Google’s speech recognition service and responds using LangChain’s prompt chain integrated with the Ollama backend.

The backend includes `pyttsx3` for converting AI-generated responses into speech, creating a fully interactive conversational experience. Nexa is designed to handle context-aware conversations and maintains a history of messages exchanged with timestamps. The app layout is built using Streamlit’s chat interface for a clean, centered, and modern user experience.

To run the project, ensure that you have Python installed, along with necessary dependencies such as `streamlit`, `speechrecognition`, `pyaudio`, `pyttsx3`, `langchain`, and `langchain-ollama`. Also, make sure the `llama3` model is available locally through Ollama (`ollama run llama3`). Once everything is set up, you can launch the assistant by running `streamlit run app.py` in your terminal.

Nexa is ideal for use cases that require a hands-free AI assistant, including personal productivity, support tasks, and ambient computing setups. Future improvements may include additional languages, theme customizations, floating UI widgets, and integrations with knowledge sources using RAG techniques.

Let me know if you'd like a downloadable `README.md` file or a version with images, badges, or a folder structure.
