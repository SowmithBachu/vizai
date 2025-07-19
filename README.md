# 📊 VizAI — GenAI-powered Visual Data Analyzer

🚀 **Live Demo:** [Click here to try the app on Render](https://viz-ai.onrender.com/)

VizAI is an intelligent data visualization and insight generation tool powered by Pandas, Seaborn, and Gemini 1.5 Flash.  
It helps users upload raw data, clean it, generate rich charts, and receive smart insights directly from the visuals — using the power of generative AI.

## 💡 Motivation

Creating visual insights from raw data shouldn't require heavy tools or long workflows.

Often, analysts or students just want to **quickly visualize a dataset**, spot trends, or gain insights without having to:
- Import data into Excel or PowerBI
- Clean missing or inconsistent values manually
  
**VizAI** was built to solve this — a simple app where you can just:
- Upload your data
- Instantly clean it
- Choose a chart
- And let AI do the insight generation

All in one browser window, with zero setup.

## 🔄 Project Workflow

Here's how VizAI works, end-to-end:

1. **Upload File**  
   The user uploads a `.csv` or `.xlsx` file directly in the app.

2. **Data Cleaning**  
   Missing values are filled, columns are standardized, and invalid data is cleaned using Pandas.

3. **Chart Selection**  
   The user selects from 15+ Seaborn chart types and configures the X and Y axes (if applicable).

4. **Chart Rendering**  
   A Matplotlib/Seaborn chart is generated and displayed within the app.

5. **AI Insight Generation**  
   The chart is converted to an image and sent to **Gemini 1.5 Flash**, which returns 3–5 smart, human-like insights.

6. **Display Insights**  
   The insights are shown in the app as bullet points — helping the user understand trends, patterns, outliers, etc.

> This workflow turns raw data into AI-interpreted visuals in under a minute.

## 🛠️ Tech Stack

### 🧪 Core Libraries
- **Pandas** – Data wrangling, cleaning, and tabular operations
- **NumPy** – Efficient numerical operations and handling of missing values
- **Seaborn** – Statistical data visualization (charts like violinplot, pairplot, heatmap, etc.)
- **Matplotlib** – Low-level chart rendering (for converting plots to image)

### 💻 Web Interface
- **Flask** – Lightweight Python web framework for creating web applications
- **HTML/CSS/JavaScript** – Frontend interface for data upload and visualization

### 🤖 Generative AI
- **Google Generative AI (Gemini 1.5 Flash)** – Used to generate human-like insights from visual charts
- **Pillow + io.BytesIO** – Converts Matplotlib figures into in-memory image objects for Gemini

### 🔐 Secrets Management
- **Environment Variables** – Used to securely store the Gemini API key (GOOGLE_API_KEY)

### 📦 Dependency Management
- `requirements.txt` – Ensures reproducibility of environments

## 🚀 Deployment

### Live Demo
The application is deployed on **Render** and accessible at: [https://viz-ai.onrender.com/](https://viz-ai.onrender.com/)

### Local Development
To run the application locally:

1. **Clone the repository:**
   ```