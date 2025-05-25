# Medical Assistant RAG

A Retrieval Augmented Generation (RAG) system for medical document management and intelligent query processing.

## Overview

This project implements a medical document management system that uses RAG architecture to provide intelligent responses to medical queries based on uploaded documents. The system can process and analyze different types of medical documents (lab reports and prescriptions) and provide context-aware responses to user queries.

## Features

- **Document Management**
  - Support for multiple document types (lab reports and prescriptions)
  - Automatic document vectorization and indexing
  - Efficient document retrieval using vector stores
  - Dynamic k-value support for flexible document retrieval

- **Intelligent Query Processing**
  - Context-aware response generation using langchain-cerebras
  - Source tracking and citation in responses
  - Medical context-specific processing
  - Multi-collection search capabilities

- **User Interface**
  - Streamlit-based web interface
  - Intuitive document upload system
  - Document type categorization
  - Real-time document display
  - Interactive query interface

[](img/streamlit.png)



## Setup and Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/Medical-Assistant-RaG.git
   cd Medical-Assistant-RaG
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   streamlit run app.py
   ```

4. get your api key from cerebras and add it to the .env file
   ```bash
   CEREBRAS_API_KEY=your_api_key
   ```

## Usage

1. **Document Upload**
   - Select document type (Lab Report/Prescription) from the sidebar
   - Upload your medical document
   - Documents are automatically processed and indexed

2. **Query the System**
   - Enter your medical query in the text input
   - The system will provide responses based on the uploaded documents
   - Responses include citations to source documents

## Technical Details

- **Vector Stores**: The system maintains three separate vector stores:
  - Lab reports store
  - Prescriptions store
  - Combined store for unified search

- **Document Retrieval**: Uses TopKRetriever with dynamic k-value support for flexible document retrieval

- **LLM Integration**: Implements context-aware processing with source tracking and medical context adherence using langchain-cerebras

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.


