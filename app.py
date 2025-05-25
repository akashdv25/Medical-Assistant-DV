import streamlit as st
from src.document_vector_retrieval.topk_docs import TopKRetriever
from src.initialize_llm.load_llm import MedicalLLM
import os


# Set page config
st.set_page_config(
    page_title="Medical Document Assistant",
    page_icon="🏥",
    layout="wide"
)

# Sidebar for file upload
with st.sidebar:
    st.header("📄 Document Upload")
    st.markdown("Upload your medical documents here.")
    
    # Radio buttons for document type selection
    doc_type = st.radio(
        "Select Document Type:",
        options=["Lab Reports", "Prescriptions"],
        help="Choose where to store the uploaded document"
    )

     # Define upload path based on selection
    upload_path = "docs/lab_reports" if doc_type == "Lab Reports" else "docs/prescriptions"
        
    # File uploader
    uploaded_file = st.file_uploader(
        "Upload Document",
        type=["png", "jpg", "jpeg", "pdf", "xlsx", "csv", "txt"],
        help="Supported formats: PNG, JPG, PDF, XLSX, CSV, TXT"
    )
    
        # Handle file upload
    if uploaded_file is not None:
        try:
            # Create directory if it doesn't exist
            os.makedirs(upload_path, exist_ok=True)
            
            # Save the file
            file_path = os.path.join(upload_path, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            st.success(f"File uploaded successfully to {doc_type}!")
            
            # Add refresh button to update vector stores
            if st.button("🔄 Refresh Vector Databases"):
                # Create retriever to update vector stores
                retriever = TopKRetriever(k=3)
                st.success("Vector Databases updated successfully!")
                
        except Exception as e:
            st.error(f"Error uploading file: {str(e)}")
    
    # Show current documents with better styling
    st.markdown("---")
    st.markdown("### 📚 Current Documents")
    
    # Create an expander for lab reports
    with st.expander("🔬 Lab Reports", expanded=True):
        lab_files = os.listdir("docs/lab_reports") if os.path.exists("docs/lab_reports") else []
        if lab_files:
            for file in lab_files:
                st.markdown(f"""
                <div style='background-color: #2E303E; padding: 12px; border-radius: 5px; margin: 3px 0;'>
                    <span style='color: #FFFFFF; font-size: 16px; font-weight: 400; font-family: monospace;'>
                        📄 {file}
                    </span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style='background-color: #2E303E; padding: 12px; border-radius: 5px;'>
                <span style='color: #FFFFFF; font-style: italic; font-family: monospace;'>
                    No lab reports uploaded
                </span>
            </div>
            """, unsafe_allow_html=True)
    
    # Create an expander for prescriptions
    with st.expander("💊 Prescriptions", expanded=True):
        prescription_files = os.listdir("docs/prescriptions") if os.path.exists("docs/prescriptions") else []
        if prescription_files:
            for file in prescription_files:
                st.markdown(f"""
                <div style='background-color: #2E303E; padding: 12px; border-radius: 5px; margin: 3px 0;'>
                    <span style='color: #FFFFFF; font-size: 16px; font-weight: 400; font-family: monospace;'>
                        📄 {file}
                    </span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style='background-color: #2E303E; padding: 12px; border-radius: 5px;'>
                <span style='color: #FFFFFF; font-style: italic; font-family: monospace;'>
                    No prescriptions uploaded
                </span>
            </div>
            """, unsafe_allow_html=True)



# Initialize the retriever and LLM (do this once when the app loads)
@st.cache_resource
def initialize_models():
    medical_llm = MedicalLLM(temperature=0.3)
    return medical_llm

# Title and description
st.title("🏥 Medical Document Assistant")
st.markdown("""
This system helps you find and understand medical information from your documents.
It searches through lab reports and prescriptions to answer your questions.
""")

# Initialize LLM (only once)
medical_llm = initialize_models()

# Query input
query = st.text_area("Enter your medical query:", 
                     placeholder="Example: What were the results of my recent blood tests?",
                     height=100)

# Create two columns for search settings
col1, col2 = st.columns(2)

with col1:
    # Add dropdown for collection selection
    search_option = st.selectbox(
        "Select where to search:",
        options=["All Documents", "Lab Reports Only", "Prescriptions Only"],
        help="Choose which type of documents to search through"
    )

with col2:
    # Add a slider for number of documents to retrieve
    k_docs = st.slider("Number of documents to retrieve:", 
                       min_value=1, max_value=5, value=3,
                       help="Maximum number of relevant documents to consider")

# Process button
if st.button("Get Answer"):
    if query:
        try:
            # Create columns for showing progress
            progress_col1, progress_col2 = st.columns(2)
            
            with progress_col1:
                # Show retrieval progress
                with st.spinner("🔍 Retrieving relevant documents..."):
                    # Create retriever with dynamic k value
                    retriever = TopKRetriever(k=k_docs)
                    
                    # Choose search method based on user selection
                    if search_option == "Lab Reports Only":
                        relevant_docs = retriever.search_lab_reports(query)
                        collection_searched = "lab reports"
                   
                    elif search_option == "Prescriptions Only":
                        relevant_docs = retriever.search_prescriptions(query)
                        collection_searched = "prescriptions"
                   
                    else:  # All Documents
                        relevant_docs = retriever.search_all_documents(query)
                        collection_searched = "all documents"
                    
                    st.success(f"Found {len(relevant_docs)} relevant documents in {collection_searched}")
            
            with progress_col2:
                # Show LLM processing progress
                with st.spinner("🤔 Analyzing documents and generating response..."):
                    result = medical_llm.get_response(query=query, context_docs=relevant_docs)
            
            # Display results in expandable sections
            st.markdown("### 📝 Medical Response")
            st.write(result["response"])
            
            # Show sources in an expander
            with st.expander("📚 View Source Documents"):
                st.markdown(f"#### Documents Referenced from {collection_searched.title()}:")
                for doc_num, source in result["source_details"].items():
                    st.markdown(f"**{doc_num}**: `{source}`")
                st.info(f"Total Sources Used: {result['total_sources']}")
                
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please enter a query first.")

# Add footer with instructions
st.markdown("---")
st.markdown("""
### 💡 Tips:
- Be specific in your questions
- Choose the appropriate collection for your query:
  - **Lab Reports Only**: For questions about test results
  - **Prescriptions Only**: For questions about medications
  - **All Documents**: When you want to search everything
- Upload new documents using the sidebar
- Remember to refresh the document index after uploading new files
""")