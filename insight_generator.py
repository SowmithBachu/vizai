import google.generativeai as genai
import io
from PIL import Image

def fig_to_image(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches='tight')
    buf.seek(0)
    image = Image.open(buf)
    return image

def init_gemini():
    import os
    api_key = os.environ.get("GEMINI_API_KEY")
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("models/gemini-1.5-flash-latest")

def generate_insight(model, df, chart_type, x_col="", y_col="", fig=None):
    prompt = f"""
You are a data analyst. A user has plotted a {chart_type}.
The selected columns were:
X-axis: {x_col or 'Not used'}
Y-axis: {y_col or 'Not used'}

Based on the image of the plot, provide 3–5 insights in bullet points.
Focus on trends, clusters, outliers, and correlations.
"""
    if fig:
        image = fig_to_image(fig)
        response = model.generate_content([image, prompt])
    else:
        response = model.generate_content(prompt)
    # Post-process to ensure bullet points as HTML list
    text = response.text.strip()
    # Split into lines, filter bullet points, and wrap in <ul>
    points = [line.strip('-•* ') for line in text.splitlines() if line.strip().startswith(('-', '•', '*'))]
    if points:
        html = '<ul>' + ''.join(f'<li>{p}</li>' for p in points) + '</ul>'
        return html
    else:
        # fallback: return as is
        return text

def handle_nl_query(model, df, user_query):
    prompt = f"""
You are a data analyst. The user has asked a question about their data:
"{user_query}"

Here is the data (first 20 rows):
{df.head(20).to_csv(index=False)}

Answer the user's question as clearly as possible, using bullet points or a short paragraph if appropriate. If the question is about trends, time periods, or aggregations, provide a concise summary and, if possible, suggest what chart or analysis would help.
"""
    response = model.generate_content(prompt)
    return response.text.strip()
