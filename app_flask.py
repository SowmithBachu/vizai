from flask import Flask, render_template, request, send_file, flash, jsonify, make_response, redirect
import pandas as pd
import os
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
app.secret_key = 'supersecretkey'
UPLOAD_FOLDER = tempfile.gettempdir()

@app.route('/')
def root():
    return redirect('/landing')

@app.route('/app', methods=['GET', 'POST'])
def index():
    df = None
    cleaned_df = None
    plot_url = None
    insight = None
    nl_query = None
    nl_answer = None
    chart_types = [
        "scatterplot", "lineplot", "barplot", "countplot", "boxplot", "violinplot",
        "stripplot", "swarmplot", "histplot", "kdeplot",
        "pairplot", "heatmap", "annotated_heatmap", "clustermap", "jointplot", "rugplot", "forecast"
    ]
    columns = []
    file_uploaded = False
    if request.method == 'POST':
        # Natural language query
        if request.form.get('nl_query'):
            nl_query = request.form.get('nl_query')
            if request.form.get('data_csv'):
                import io
                df = pd.read_csv(io.StringIO(request.form['data_csv']))
                cleaned_df = clean_data(df.copy())
                try:
                    model = init_gemini()
                    nl_answer = handle_nl_query(model, cleaned_df, nl_query)
                except Exception as e:
                    nl_answer = f"Failed to answer query: {e}"
            # Always show the previous plot if it exists
            plot_url = '/static/plot.png' if os.path.exists('static/plot.png') else None
            return render_template('singlepage.html', file_uploaded=True, df=df, cleaned_df=cleaned_df, columns=columns, chart_types=chart_types, plot_url=plot_url, insight=insight, data_csv=request.form.get('data_csv'), nl_query=nl_query, nl_answer=nl_answer)
        # File upload
        if 'file' in request.files and request.files['file'].filename:
            file = request.files['file']
            filename = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filename)
            ext = file.filename.split('.')[-1]
            try:
                if ext == 'csv':
                    df = pd.read_csv(filename)
                else:
                    df = pd.read_excel(filename)
                file_uploaded = True
            except Exception as e:
                flash(f'Failed to read file: {e}', 'danger')
                return render_template('singlepage.html')
        # If file already uploaded, get from hidden form
        elif request.form.get('data_csv'):
            import io
            df = pd.read_csv(io.StringIO(request.form['data_csv']))
            file_uploaded = True
        # Data cleaning and plotting
        if df is not None:
            cleaned_df = clean_data(df.copy())
            columns = cleaned_df.columns.tolist()
            # Chart generation
            chart_type = request.form.get('chart_type')
            x_axis = request.form.get('x_axis')
            y_axis = request.form.get('y_axis')
            if chart_type:
                # Robust axis selection
                if chart_type not in ["pairplot", "clustermap", "heatmap"] and (not x_axis or x_axis not in columns):
                    x_axis = columns[0] if columns else None
                if chart_type in [
                    "scatterplot", "lineplot", "barplot", "boxplot", "violinplot",
                    "stripplot", "swarmplot", "jointplot"
                ] and (not y_axis or y_axis not in columns):
                    y_axis = columns[1] if len(columns) > 1 else columns[0] if columns else None
                try:
                    plot = generate_plot(cleaned_df, chart_type, x_axis, y_axis)
                    if plot:
                        # Always treat plot as a Figure object for saving
                        fig = plot.figure if hasattr(plot, "figure") else plot
                        plot_path = os.path.join('static', 'plot.png')
                        fig.savefig(plot_path)
                        plt.close(fig)
                        plot_url = '/static/plot.png'
                        try:
                            model = init_gemini()
                            insight = generate_insight(model, cleaned_df, chart_type, x_axis, y_axis, fig=fig)
                        except Exception as e:
                            insight = f"Failed to generate insight: {e}"
                    else:
                        flash('Could not generate the plot. Please check your column selection.', 'warning')
                except Exception as e:
                    flash(f'Error generating plot: {e}', 'danger')
            # PDF export
            if request.form.get('export_pdf'):
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=12)
                pdf.cell(200, 10, txt="VizAI - AI Insights Report", ln=True, align="C")
                pdf.ln(10)
                pdf.multi_cell(0, 10, f"Chart Type: {chart_type}")
                pdf.ln(5)
                pdf.multi_cell(0, 10, "AI Insight:\n" + (insight or ''))
                if plot_url and os.path.exists('static/plot.png'):
                    pdf.image('static/plot.png', x=10, y=None, w=180)
                pdf_path = os.path.join(UPLOAD_FOLDER, 'vizai_report.pdf')
                pdf.output(pdf_path)
                return send_file(pdf_path, as_attachment=True)
        # For form persistence, store cleaned data as CSV in hidden field
        data_csv = cleaned_df.to_csv(index=False) if cleaned_df is not None else ''
        return render_template('singlepage.html', file_uploaded=file_uploaded, df=df, cleaned_df=cleaned_df, columns=columns, chart_types=chart_types, plot_url=plot_url, insight=insight, data_csv=data_csv, nl_query=nl_query, nl_answer=nl_answer)
    return render_template('singlepage.html', file_uploaded=False)

@app.route('/landing')
def landing():
    return render_template('landing.html')

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

if __name__ == '__main__':
    app.run(debug=True) 