import gradio as gr
import hashlib
from typing import List, Dict
import os

from document_processor.file_handler import DocumentProcessor
from retriever.builder import RetrieverBuilder
from agents.workflow import AgentWorkflow
from config import constants, settings
from utils.logging import logger

# 1) Example question + document pairs shown in the dropdown.
#    Drop your own files into examples/ and add an entry here to extend this.
EXAMPLES = {
    "Sample: Solar Power Basics": {
        "question": "What is the efficiency range of monocrystalline panels, and how long is the typical warranty?",
        "file_paths": ["examples/sample-solar-report.md"]
    },
}

def main():
    processor = DocumentProcessor()
    retriever_builder = RetrieverBuilder()
    workflow = AgentWorkflow()

    # Define custom CSS for styling
    css = """
    .title {
        font-size: 1.5em !important; 
        text-align: center !important;
        color: #FFD700; 
    }

    .subtitle {
        font-size: 1em !important; 
        text-align: center !important;
        color: #FFD700; 
    }

    .text {
        text-align: center;
    }
    """

    js = """
    function createGradioAnimation() {
        var container = document.createElement('div');
        container.id = 'gradio-animation';
        container.style.fontSize = '2em';
        container.style.fontWeight = 'bold';
        container.style.textAlign = 'center';
        container.style.marginBottom = '20px';
        container.style.color = '#eba93f';

        var text = 'Welcome to DocChat 🐥!';
        for (var i = 0; i < text.length; i++) {
            (function(i){
                setTimeout(function(){
                    var letter = document.createElement('span');
                    letter.style.opacity = '0';
                    letter.style.transition = 'opacity 0.1s';
                    letter.innerText = text[i];

                    container.appendChild(letter);

                    setTimeout(function() {
                        letter.style.opacity = '0.9';
                    }, 50);
                }, i * 250);
            })(i);
        }

        var gradioContainer = document.querySelector('.gradio-container');
        gradioContainer.insertBefore(container, gradioContainer.firstChild);

        return 'Animation created';
    }
    """

    with gr.Blocks(title="DocChat 🐥") as demo:
        gr.Markdown("## DocChat: powered by Docling 🐥 and LangGraph", elem_classes="subtitle")
        gr.Markdown("# How it works ✨:", elem_classes="title")
        gr.Markdown("📤 Upload your document(s), enter your query then hit Submit 📝", elem_classes="text")
        gr.Markdown("Or you can select one of the examples from the drop-down menu, select Load Example then hit Submit 📝", elem_classes="text")
        gr.Markdown("⚠️ **Note:** DocChat only accepts documents in these formats: '.pdf', '.docx', '.txt', '.md'", elem_classes="text")

        # 2) Maintain the session state for retrieving doc changes
        session_state = gr.State({
            "file_hashes": frozenset(),
            "retriever": None
        })

        # 3) Layout 
        with gr.Row():
            with gr.Column():
                # Section for Examples
                gr.Markdown("### Example 📂")
                example_dropdown = gr.Dropdown(
                    label="Select an Example 🐥",
                    choices=list(EXAMPLES.keys()),
                    value=None,  # initially unselected
                )
                load_example_btn = gr.Button("Load Example 🛠️")

                # Standard input components
                files = gr.Files(label="📄 Upload Documents", file_types=constants.ALLOWED_TYPES)
                question = gr.Textbox(label="❓ Question", lines=3)

                submit_btn = gr.Button("Submit 🚀")
                
            with gr.Column():
                answer_output = gr.Textbox(label="🐥 Answer", interactive=False)
                verification_output = gr.Textbox(label="✅ Verification Report")

        # 4) Helper function to load example into the UI
        def load_example(example_key: str):
            """
            Given a key like 'Example 1', 
            read the relevant docs from disk and return
            them as file-like objects, plus the example question.
            """
            if not example_key or example_key not in EXAMPLES:
                return [], ""  # blank if not found

            ex_data = EXAMPLES[example_key]
            question = ex_data["question"]
            file_paths = ex_data["file_paths"]

            # Prepare the file list to return. We read them from disk to
            # give Gradio something it can handle as "uploaded" files.
            loaded_files = []
            for path in file_paths:
                if os.path.exists(path):
                    # Gradio can accept a path directly, or a file-like object
                    loaded_files.append(path)
                else:
                    logger.warning(f"File not found: {path}")

            # The function can return lists matching the outputs we define below
            return loaded_files, question

        load_example_btn.click(
            fn=load_example,
            inputs=[example_dropdown],
            outputs=[files, question]
        )

        # 5) Standard flow for question submission
        def process_question(question_text: str, uploaded_files: List, state: Dict):
            """Handle questions with document caching."""
            try:
                if not question_text.strip():
                    raise ValueError("❌ Question cannot be empty")
                if not uploaded_files:
                    raise ValueError("❌ No documents uploaded")

                current_hashes = _get_file_hashes(uploaded_files)
                
                if state["retriever"] is None or current_hashes != state["file_hashes"]:
                    logger.info("Processing new/changed documents...")
                    chunks = processor.process(uploaded_files)
                    retriever = retriever_builder.build_hybrid_retriever(chunks)
                    
                    state.update({
                        "file_hashes": current_hashes,
                        "retriever": retriever
                    })
                
                result = workflow.full_pipeline(
                    question=question_text,
                    retriever=state["retriever"]
                )
                
                return result["draft_answer"], result["verification_report"], state
                    
            except Exception as e:
                logger.error(f"Processing error: {str(e)}")
                return f"❌ Error: {str(e)}", "", state

        submit_btn.click(
            fn=process_question,
            inputs=[question, files, session_state],
            outputs=[answer_output, verification_output, session_state]
        )

    # share=True would expose the app - and any uploaded documents - through a
    # public Gradio tunnel. Keep it local by default; opt in with DOCCHAT_SHARE=1.
    # Gradio 6 takes theme/css/js at launch() rather than on Blocks().
    demo.launch(
        theme=gr.themes.Citrus(),
        css=css,
        js=js,
        server_name="127.0.0.1",
        server_port=int(os.environ.get("DOCCHAT_PORT", 5000)),
        share=os.environ.get("DOCCHAT_SHARE") == "1",
    )

def _get_file_hashes(uploaded_files: List) -> frozenset:
    """Generate SHA-256 hashes for uploaded files."""
    hashes = set()
    for file in uploaded_files:
        with open(file.name, "rb") as f:
            hashes.add(hashlib.sha256(f.read()).hexdigest())
    return frozenset(hashes)

if __name__ == "__main__":
    main()
