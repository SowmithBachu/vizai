import os
from flask import Flask, request, jsonify, make_response
import pandas as pd
import tempfile
from data_cleaner import clean_data
from plot_generator import generate_plot
from insight_generator import init_gemini, generate_insight, handle_nl_query
from fpdf import FPDF
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import io

load_dotenv()

app = Flask(__name__)
UPLOAD_FOLDER = tempfile.gettempdir()

@app.route('/api/chart', methods=['POST'])
def api_chart():
    try:
        data = request.json
        chart_type = data.get('chartType')
        x_axis = data.get('xAxis')
        y_axis = data.get('yAxis')
        data_csv = data.get('dataCsv')
        if not data_csv or not chart_type:
            return jsonify({'error': 'Missing data or chart type'}), 400
        df = pd.read_csv(io.StringIO(data_csv))
        cleaned_df = clean_data(df.copy())
        plot = generate_plot(cleaned_df, chart_type, x_axis, y_axis)
        if plot:
            # Handle Plotly figures for geomap and sankey
            if chart_type in ["geomap", "sankey"]:
                try:
                    import plotly.io as pio
                    img_bytes = plot.to_image(format="png", engine="kaleido")
                except Exception as e:
                    return jsonify({'error': f'Plotly export failed: {e}'}), 500
                response = make_response(img_bytes)
                response.headers.set('Content-Type', 'image/png')
                return response
            if chart_type in ["pairplot", "clustermap", "jointplot"]:
                fig = plot.figure if hasattr(plot, "figure") else plot
            else:
                fig = plot
            buf = io.BytesIO()
            fig.savefig(buf, format="png", bbox_inches='tight')
            if hasattr(fig, 'clf'):
                plt.close(fig)
            buf.seek(0)
            response = make_response(buf.read())
            response.headers.set('Content-Type', 'image/png')
            return response
        else:
            return jsonify({'error': 'Could not generate plot'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/insight', methods=['POST'])
def api_insight():
    try:
        data = request.json
        chart_type = data.get('chartType')
        x_axis = data.get('xAxis')
        y_axis = data.get('yAxis')
        data_csv = data.get('dataCsv')
        if not data_csv or not chart_type:
            return jsonify({'error': 'Missing data or chart type'}), 400
        df = pd.read_csv(io.StringIO(data_csv))
        cleaned_df = clean_data(df.copy())
        model = init_gemini()
        insight = generate_insight(model, cleaned_df, chart_type, x_axis, y_axis)
        return jsonify({'insight': insight})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/nl_query', methods=['POST'])
def api_nl_query():
    try:
        data = request.json
        nl_query = data.get('nlQuery')
        data_csv = data.get('dataCsv')
        if not data_csv or not nl_query:
            return jsonify({'error': 'Missing data or query'}), 400
        df = pd.read_csv(io.StringIO(data_csv))
        cleaned_df = clean_data(df.copy())
        model = init_gemini()
        answer = handle_nl_query(model, cleaned_df, nl_query)
        return jsonify({'answer': answer})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Expose the app object for Vercel
app = app 