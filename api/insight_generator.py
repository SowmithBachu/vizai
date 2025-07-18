import os
import google.generativeai as genai
import pandas as pd
import io

def init_gemini():
    api_key = os.getenv('GEMINI_API_KEY')
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-1.5-flash')

def generate_insight(model, df, chart_type, x_axis, y_axis, fig=None):
    # Save the plot to a buffer
    buf = io.BytesIO()
    if fig:
        fig.savefig(buf, format='png')
        buf.seek(0)
    else:
        buf = None
    prompt = f"Analyze the following {chart_type} and provide 3-5 insights."
    if x_axis:
        prompt += f" X-axis: {x_axis}."
    if y_axis:
        prompt += f" Y-axis: {y_axis}."
    if buf:
        response = model.generate_content([
            prompt,
            genai.types.content.ImageContent(buf.read(), mime_type='image/png')
        ])
    else:
        response = model.generate_content(prompt)
    return response.text

def handle_nl_query(model, df, query):
    prompt = f"Given the following data, answer the question: {query}\n\n{df.head(10).to_csv(index=False)}"
    response = model.generate_content(prompt)
    return response.text 