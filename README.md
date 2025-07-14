# 📊 VizAI — GenAI-powered Visual Data Analyzer

🚀 **Live Demo:** [Click here to try the app on Streamlit](https://vizinsight.streamlit.app/)

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

Here's how AutoVizAI works, end-to-end:

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
- **Streamlit** – Lightweight Python framework to create web apps with zero frontend code

### 🤖 Generative AI
- **Google Generative AI (Gemini 1.5 Flash)** – Used to generate human-like insights from visual charts
- **Pillow + io.BytesIO** – Converts Matplotlib figures into in-memory image objects for Gemini

### 🔐 Secrets Management
- **Streamlit Secrets Manager** – Used to securely store the Gemini API key (.gitignore)

### 📦 Dependency Management
- `requirements.txt` – Ensures reproducibility of environments

## 🤝 Contributions & Issues

Have ideas to improve AutoVizAI? Found a bug or want to add more chart types?

Feel free to:

- 🛠️ Fork the repo
- 📦 Create a new branch
- 📝 Make your changes
- 🚀 Submit a pull request

> Found an issue or need help? [Open an issue](https://github.com/kailashmannem/vizai/issues) and describe the problem clearly.

All contributions — code, design, documentation, or testing — are welcome!

