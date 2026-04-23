from langchain_core.tools import tool
from langchain_groq import ChatGroq
from app.config import settings


def make_summarize_voice_tool():
    llm = ChatGroq(model="gemma2-9b-it", api_key=settings.groq_api_key, temperature=0)

    @tool
    def summarize_voice_note(transcription: str) -> dict:
        """
        Summarize a voice note transcription into concise discussion points
        suitable for the Topics Discussed field.
        """
        response = llm.invoke(
            f"Summarize this voice note transcription into 2-4 concise bullet points "
            f"suitable for a CRM topics discussed field:\n\n{transcription}"
        )
        return {"summary": response.content}

    return summarize_voice_note
