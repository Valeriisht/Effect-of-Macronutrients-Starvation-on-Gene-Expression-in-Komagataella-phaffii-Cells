import os

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.graph_objects as go
import numpy as np


st.set_page_config(
    page_title="**Komagataella Phaffii** Phosphate and Biotin Response",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1E90FF;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #1E90FF;
        border-bottom: 2px solid #1E90FF;
        padding-bottom: 0.5rem;
        margin-top: 1.5rem;
    }
    .gene-card {
        background-color: #F0F8FF;
        border-radius: 10px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background-color: #FFFFFF;
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        font-weight: bold;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1E90FF;
        color: white;
    }
</style>
""", unsafe_allow_html=True)


st.markdown('<h1 class="main-header">Komagataella Phaffii Phosphate and Biotin Response</h1>', unsafe_allow_html=True)
st.markdown('<h3>Interactive database of genes activated by phosphate and biotin deficiency</h3>', unsafe_allow_html=True)

cur_dir = os.getcwd()
file_path = os.path.join(cur_dir, "data", "Data.xlsx")

st.markdown('<h4>Data are presented for genes that significantly changed expression under phosphate and biotin deficiency conditions. Biotin data are presented only for cells grown on methanol as a carbon source.</h4>', unsafe_allow_html=True)
st.markdown('<h4>Data are presented for genes that significantly changed expression under phosphate and biotin deficiency conditions. Biotin data are presented only for cells grown on methanol as a carbon source.</h4>', unsafe_allow_html=True)


@st.cache_data
def load_data():

    all_sheets = pd.read_excel(file_path, sheet_name=None)

    sheet_names = list(all_sheets.keys())

    data_act = all_sheets[sheet_names[0]]  
    data_rep = all_sheets[sheet_names[1]]  
    data_phosphate = all_sheets[sheet_names[2]].add_suffix("_phosphate")
    data_biotin = all_sheets[sheet_names[4]].add_suffix("_biotin")

    return data_act, data_rep, data_phosphate, data_biotin

# Data loading
df_active, df_repres, data_phosphate, data_biotin = load_data()


df_temp = pd.concat([df_active, df_repres], ignore_index=True)

df_common_cond = pd.merge(data_phosphate, data_biotin,
                     left_on=data_phosphate.columns[0], 
                     right_on=data_biotin.columns[0], 
                     how="outer")



df_common = pd.merge(df_temp, df_common_cond,
                     left_on=df_temp.columns[0], 
                     right_on = df_common_cond.columns[0], 
                     how="left")

df_common = df_common.dropna(subset=["Pichia gene name"])


# st.sidebar.header("🔍 Filtering and settings")
# Details 
st.header("Information about a single gene")

if not df_common.empty:
    selected_gene = st.selectbox(
        "Choose Gene from list",
        df_common["Pichia gene name"].tolist()
    )
    
    gene_data = df_common[df_common["Pichia gene name"] == selected_gene].iloc[0]



tab1, tab2, tab3 = st.tabs(["🎯 Gene Details", "📊 Expression Data", " 💻 Visualisation"])

with tab1:
    st.header("Protein Information")
    st.info("For the identified orthologous genes in ***S. cerevisiae***, for which more information is available on the structure and functions of their proteins, an alignment of the corresponding amino acid sequences and sequences from the yeast proteome of ***S. cerevisiae*** was performed.")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("***Komagataella phaffii*** Protein")
        st.info(f"**Protein ID:** {gene_data['Pichia protein ID']}")
        st.info(f"**Description:** {gene_data['Pichia description']}")
    
    with col2:
        st.subheader("***Saccharomyces cerevisiae*** Ortholog")
        st.info(f"**Protein ID:** {gene_data['Saccharomyces accession ID']}")
        st.info(f"**Description:** {gene_data['SGD description']}")
    
    st.divider()
    st.subheader("BLAST Results Aligment")
    st.info("Detailed information on the alignment results")
    col_blast1, col_blast2 = st.columns(2)
    with col_blast1:
        st.metric(label="E-value", value=f"{gene_data['E-value']:.2e}")
    with col_blast2:
        st.metric(label="Percent Identity", value=f"{gene_data['Per. Ident']:.1f}%")

with tab2:
    st.header("Differential Expression Analysis")

    with st.container():
        st.markdown("""
        <div style='background-color: #F0F8FF; padding: 15px; border-radius: 10px; border-left: 5px solid #1E90FF; margin-bottom: 20px;'>
        <h4 style='color: #1E90FF; margin-top: 0;'>Experimental Conditions</h4>
        <ul style='margin-bottom: 0;'>
        <li><span style='color: #1E90FF;'><strong>Phosphate:</strong>/span><span style='color: #1E90FF;'>1 g/L vs. 30 mg/L</span></li>
        <li><span style='color: #1E90FF;'><strong>Biotin:</strong></span><span style='color: #1E90FF;'>400 µg/L vs. Biotin-free medium</span></li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    ### **P-value**  
    **Statistical significance of expression change**  
    - **P < 0.05** → Significant change  
    - **P < 0.001** → Highly significant  
    - **P < 1e-10** → Extremely significant (multiple testing corrected)  

    ### **BaseMean**  
    **Average expression level across all samples**  
    - **High values** → Constitutively expressed gene  
    - **Low values** → Lowly expressed or condition-specific gene  
    """)
        
    col3, col4 = st.columns(2)
    with col3:
        st.subheader("Phosphate Response")
        if not pd.isna(gene_data['baseMean_phosphate']):
            if gene_data['log2FoldChange_phosphate'] > 0:
                st.metric("log2FoldChange", 
                        value=f"{gene_data['log2FoldChange_phosphate']:.2f}",
                        delta=f"{gene_data['log2FoldChange_phosphate']:.2f} - Upregulated",
                        delta_color="normal")
            else:
                st.metric("log2FoldChange", 
                        value=f"{gene_data['log2FoldChange_phosphate']:.2f}",
                        delta=f"{gene_data['log2FoldChange_phosphate']:.2f} - Downregulated",
                        delta_color="normal")
                

            st.caption(f"**P-value:** {gene_data['P value_phosphate']:.3e}")
            st.caption(f"**BaseMean:** {gene_data['baseMean_phosphate']:.1f}")
        else:
            st.warning("No significant phosphate response data")
    
    with col4:
        st.subheader("Biotin Response")
        if not pd.isna(gene_data['baseMean_biotin']):
            st.metric("log2FoldChange", 
                      value=f"{gene_data['log2FoldChange_biotin']:.2f}",
                      delta="Upregulated" if gene_data['log2FoldChange_biotin'] > 0 else "Downregulated")    
            st.caption(f"**P-value:** {gene_data['p value_biotin']:.3e}")
            st.caption(f"**BaseMean:** {gene_data['baseMean_biotin']:.1f}")
        else:
            st.warning("No significant biotin response data")

with tab3:
    st.markdown('<div class="gene-card">', unsafe_allow_html=True)
    st.header("Visualization and Comparison")

    plot_data = []

    if not pd.isna(gene_data.get("log2FoldChange_phosphate", None)):
        plot_data.append(("Phosphate", gene_data["log2FoldChange_phosphate"],
                         gene_data["P value_phosphate"], gene_data['baseMean_phosphate']))

    if not pd.isna(gene_data.get("log2FoldChange_biotin", None)):
        plot_data.append(("Biotin", gene_data["log2FoldChange_biotin"],
                         gene_data["p value_biotin"], gene_data['baseMean_biotin'])) 

    if plot_data:
        df_plot = pd.DataFrame(plot_data, columns=["Condition", "log2FoldChange",
                                                   "P-value", "BaseMean"])

        col7, col8 = st.columns(2)

        with col7:
            volcano_data = []
            for condition, fc, pval, _ in plot_data:
                volcano_data.append({
                    'Condition': condition, 
                    "log2FoldChange": fc, 
                    "neg_log10_pvalue": -np.log10(pval) if pval > 0 else 10,  
                    "Significant": pval < 0.05
                })
            
            df_volcano = pd.DataFrame(volcano_data)

            fig = px.scatter(df_volcano, x="log2FoldChange",
                             y='neg_log10_pvalue', 
                             color='Condition', 
                             color_discrete_map={True: '#FF4500', False: '#1E90FF'},
                             hover_data=['Significant'], 
                             title='Statistical significance of changes',
                             labels={'log2FoldChange': 'log2 Fold Change', 
                                    'neg_log10_pvalue': '-log10(P-value)'})
            
            fig.add_hline(y=-np.log10(0.05), line_dash="dash", line_color="red")
            fig.add_vline(x=1, line_dash="dash", line_color="gray")
            fig.add_vline(x=-1, line_dash="dash", line_color="gray")
            fig.add_vline(x=0, line_dash="dash", line_color="green")

            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )

            if fig:
                st.plotly_chart(fig, use_container_width=True)
        
        with col8:  
            if len(plot_data) == 2:
                st.subheader("Comparison of two conditions")
                
                fig2 = px.scatter(x=[plot_data[0][1]], y=[plot_data[1][1]],
                                 labels={'x': 'log2FoldChange Phosphate', 'y': 'log2FoldChange Biotin'},
                                 title='Fold Change Comparison',
                                 hover_data=[['Gene: ' + selected_gene]])
                
                fig2.add_hline(y=0, line_color="gray")
                fig2.add_vline(x=0, line_color="gray")
                
                quadrant = ""
                if plot_data[0][1] > 0 and plot_data[1][1] > 0:
                    quadrant = "Upregulated in both conditions"
                elif plot_data[0][1] < 0 and plot_data[1][1] < 0:
                    quadrant = "Downregulated in both conditions"
                elif plot_data[0][1] > 0 and plot_data[1][1] < 0:
                    quadrant = "Upregulated by phosphate, Downregulated by biotin"
                else:
                    quadrant = "Downregulated by phosphate, Upregulated by biotin"
                
                fig2.add_annotation(x=plot_data[0][1], y=plot_data[1][1],
                                   text=quadrant,
                                   showarrow=True,
                                   arrowhead=1)
                
                fig2.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(fig2, use_container_width=True)

                fig2.add_hline(y=-np.log10(0.05), line_dash="dash", line_color="red")
                fig2.add_vline(x=1, line_dash="dash", line_color="gray")
                fig2.add_vline(x=-1, line_dash="dash", line_color="gray")
                fig2.add_vline(x=0, line_dash="dash", line_color="green")
    
    st.markdown('</div>', unsafe_allow_html=True)
