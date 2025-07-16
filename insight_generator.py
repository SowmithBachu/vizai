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

Based on the image of the plot, provide 3–5 insights in bullet points. Each point should be a full sentence. Do not include any introduction or summary, just the points. Focus on trends, clusters, outliers, and correlations. Format your answer as Markdown bullet points.
"""
    if fig:
        image = fig_to_image(fig)
        response = model.generate_content([image, prompt])
    else:
        response = model.generate_content(prompt)
    text = response.text.strip()
    # Extract up to 4 bullet points
    points = [line.strip('-•* ') for line in text.splitlines() if line.strip().startswith(('-', '•', '*'))]
    points = [p for p in points if p]  # Remove empty
    points = points[:4]  # Limit to 4
    if points:
        html = '<div class="font-semibold text-lg mb-2 text-pink-400 flex items-center gap-2"><i class="lucide lucide-brain-circuit w-5 h-5 text-pink-400"></i>AI Insight</div>'
        html += '<ul class="list-disc pl-6 text-base text-slate-100">' + ''.join(f'<li class="mb-2">{p}</li>' for p in points) + '</ul>'
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
