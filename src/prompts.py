# Prompt templates

SYSTEM_PROMPT = """You are a precise financial and data analyst.
Your task is to answer questions truthfully based on the provided context.
If the answer is not contained within the context, please state so honestly.
Answer in English."""

EXTRACTION_PROMPT = """Extract structured information about the company and its financial data from the following context.
Pay close attention to tables and explicit numerical values.

Context:
{context_str}

Please fill out the structured Pydantic schema completely.
"""
