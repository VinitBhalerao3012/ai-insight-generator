# ============================================================
# AI-Powered Insight Generator
# Tools: Python, Pandas, Google Gemini AI
# Author: Vinit Bhalerao
# ============================================================

import pandas as pd
from google import genai
from fpdf import FPDF
from dotenv import load_dotenv
import os
import sys
from datetime import datetime

# Load API key from .env
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini
client = genai.Client(api_key=API_KEY)

print("=" * 60)
print("AI-POWERED INSIGHT GENERATOR")
print("=" * 60)

# ── 1. LOAD DATASET
def load_data(filepath):
    print(f"\n[1/5] Loading dataset: {filepath}")
    df = pd.read_csv(filepath)
    print(f"    Loaded {len(df):,} rows and {len(df.columns)} columns")
    return df

# ── 2. ANALYSE DATASET
def analyse_data(df):
    print("\n[2/5] Analysing dataset...")
    analysis = {}
    analysis["shape"] = df.shape
    analysis["columns"] = list(df.columns)
    analysis["dtypes"] = df.dtypes.to_string()
    analysis["missing"] = df.isnull().sum().to_string()
    analysis["summary"] = df.describe().to_string()
    print("    Analysis complete")
    return analysis

# ── 3. GENERATE AI INSIGHTS
def generate_insights(df, analysis):
    print("\n[3/5] Generating AI insights...")
    
    prompt = f"""
    You are a senior data analyst. Analyse this HR dataset and provide a professional business insight report.

    Dataset: {analysis['shape'][0]} rows, {analysis['shape'][1]} columns
    Columns: {', '.join(analysis['columns'][:10])}

    Please provide:
    1. EXECUTIVE SUMMARY — 2-3 sentences
    2. KEY FINDINGS — 3 bullet points
    3. BUSINESS RECOMMENDATIONS — 2 actionable recommendations

    Keep it concise and professional.
    """
    
    response = client.models.generate_content(
        model="models/gemini-2.5-flash-lite",
        contents=prompt
    )
    print("    AI insights generated successfully")
    return response.text

# ── 4. GENERATE PDF REPORT
def generate_pdf(insights, analysis, output_path):
    print("\n[4/5] Generating PDF report...")
    
    pdf = FPDF()
    pdf.add_page()
    
    # Title
    pdf.set_font("Helvetica", "B", 20)
    pdf.set_fill_color(26, 115, 232)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 15, "AI-Powered Data Insight Report", fill=True, ln=True, align="C")
    
    # Date and info
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 8, f"Generated: {datetime.now().strftime('%d %B %Y, %H:%M')}", ln=True, align="C")
    pdf.cell(0, 8, f"Dataset: {analysis['shape'][0]:,} rows x {analysis['shape'][1]} columns", ln=True, align="C")
    pdf.ln(5)
    
    # Columns section
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(26, 115, 232)
    pdf.cell(0, 10, "Dataset Columns:", ln=True)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(0, 0, 0)
    pdf.multi_cell(0, 6, ", ".join(analysis['columns']))
    pdf.ln(5)
    
    # AI Insights
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(26, 115, 232)
    pdf.cell(0, 10, "AI-Generated Insights:", ln=True)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(0, 0, 0)
    
    # Clean and add insights text
    clean_text = insights.encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 6, clean_text)
    
    pdf.output(output_path)
    print(f"    PDF saved: {output_path}")

# ── 5. MAIN
def main():
    data_file = "data/sample_data.csv"
    
    if not os.path.exists(data_file):
        print(f"\n❌ Error: {data_file} not found!")
        print("Please add a CSV file to the data/ folder")
        sys.exit(1)
    
    df = load_data(data_file)
    analysis = analyse_data(df)
    insights = generate_insights(df, analysis)
    
    output_path = f"output/insight_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    generate_pdf(insights, analysis, output_path)
    
    print("\n" + "=" * 60)
    print("REPORT GENERATED SUCCESSFULLY!")
    print(f"Output: {output_path}")
    print("=" * 60)

if __name__ == "__main__":
    main()