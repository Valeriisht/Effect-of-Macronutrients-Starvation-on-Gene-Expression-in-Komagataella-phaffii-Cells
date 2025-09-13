# Effect of Macronutrients Starvation on Gene Expression in ***Komagataella phaffii*** Cells
<img align=right src="https://github.com/user-attachments/assets/0e29d8da-3fbd-4b6e-9d8e-94e8fc46a68e" alt="# prediction tool" width="300"/>

This is a repository of studies on the response to macronutrient deficiency through altered gene expression in *Komagataella phaffii* cells.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://github.com/Valeriisht/Effect-of-Macronutrients-Starvation-on-Gene-Expression-in-Komagataella-phaffii-Cells/edit/main/README.md)


- The development of new methods of analysis makes ***Komagataella phaffi*** yeast a model object of biotechnology and genetics, which in turn stimulates their further study and use as an object of biotechnological research.  In our work, a study was conducted to investigate the effect of phosphate and biotin deficiency on changes in yeast gene expression using transcriptome analysis methods.

## Aim

- The main goal of the project is to study the effect of macronutrient deficiency on the regulation of gene expression in ***Komagataella phaffi*** yeast

## Dataset

The data is contained in the folder - [data/Data.xsxl](https://github.com/Valeriisht/Effect-of-Macronutrients-Starvation-on-Gene-Expression-in-Komagataella-phaffii-Cells/blob/main/data/Data.xlsx)

## Methods

The following tools are used in this project: 

**Quality Control & Preprocessing:**
- *FastQC (Andrews, 2010)*
- *Trimmomatic (Bolger et al., 2014)*

**Alignment & Quantification:**
- *Reference genome:* *Komagataella phaffii* ASM2700v1 (NCBI)
- *Sequence alignment:* HISAT2 (Kim et al., 2019)
- *Read counting:* featureCounts (Liao et al., 2014)

**Differential Expression Analysis:**
- *Statistical analysis:* R 3.6.3 (R Core Team, 2024)
- *DESeq2* for differential expression analysis

**Orthology & Functional Annotation:**
- *Sequence similarity:* BLAST+ (Camacho et al., 2009)
- *Orthology mapping:* Saccharomyces Genome Database (SGD)


**Interactive Visualization Platform:**
- *Backend:* Python 3.11 with Pandas, NumPy, SciPy
- *Web framework:* Streamlit for interactive web application
- *Visualization:* Plotly 

## Results

Script of Interective DataBase about gene expression is located in '''https://github.com/Valeriisht/Effect-of-Macronutrients-Starvation-on-Gene-Expression-in-Komagataella-phaffii-Cells/blob/main/dashboard.py'''

This database integrates RNA-seq data, orthology information, and statistical analysis for comprehensive gene function exploration.

### Launch 

**1. Install all dependencies:**

```
conda env create -f environmental.yaml
conda activate your_env_name
```

**2.Launch in command line:**

```streamlit run phosphate_dashboard.py```

