import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# ==== Function =====
@st.cache()
def load_data():
    df = pd.read_csv("./telco_churn.csv")
    #convert total charge ke numeric
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'],errors='coerce')
    #filter data tenure diatas 0
    df = df.query('tenure > 0')
    #drop customerid
    df = df.drop('customerID',axis=1).reset_index(drop=True)
    df['Churn'] = df['Churn'].replace(['Yes','No'],[1,0]).astype(int)
    return df

def bar_stack(df,col_x,col_y='Churn'):

    # create crosstab and normalize the values
    ct = pd.crosstab(df[col_x], df[col_y])
    ct_pct = ct.apply(lambda x: x / x.sum(), axis=1)

    # plot stacked horizontal bar chart
    ax = ct_pct.plot(kind='barh', stacked=True, color=['#1f77b4', 'red'])

    # add annotations
    for i in ax.containers:
        # get the sum of values in each container
        total = sum(j.get_width() for j in i)
        
        for j in i:
            # get the width and height of the bar
            width = j.get_width()
            height = j.get_height()
            
            # calculate the position of the text
            x = j.get_x() + width / 2
            y = j.get_y() + height / 2
            
            # format the text as percentage
            text = f'{width:.0%}'
            
            # set the position and format of the annotation
            ax.annotate(text, xy=(x, y), xytext=(0, 0), textcoords='offset points',
                        ha='center', va='center', color='white', fontsize=12,
                        fontweight='bold')

    # set plot title and labels
    ax.set_title(f'Churn Rate by {col_x}')
    ax.set_xlabel('Number of Customers')
    ax.set_ylabel(f'{col_x}')
    # # show the plot
    plt.legend(title='Churn', loc='center left', bbox_to_anchor=(1.0, 0.5))



# ==== Main Processs ======
st.set_option('deprecation.showPyplotGlobalUse', False)

# --- Load Data ----
df = load_data()

# --- Title ---
st.title('Customer :red[Churn] :man-running: :green[Analysis]')
st.markdown('''
    ---
''')
# Move selectbox widget outside the if statements
sidebar = st.sidebar.selectbox(
    "Menu",
    ['Background',
     'Summary',
     'Eksplorasi'
      ]
)

if sidebar == 'Background':
    st.subheader('Business Problem')
    st.write('Masalah bisnis yang dihadapi adalah churn pelanggan yang tinggi di industri telekomunikasi. Hal ini dapat mempengaruhi keuntungan perusahaan dan reputasi merek, sehingga perusahaan perlu mengambil tindakan untuk mempertahankan pelanggan yang ada.')
    st.subheader('Objective')
    st.write('Tujuan analisis adalah mengidentifikasi faktor-faktor yang berkontribusi terhadap churn pelanggan dan mengembangkan strategi retensi pelanggan yang efektif berdasarkan temuan analisis.')

elif sidebar == 'Summary':
    st.subheader('Tampilan Data')
    st.markdown('''
    ---
    ''')
    st.table(df.head())

    st.subheader('Desriptive Statistics Customer Churn - Numeric')
    st.markdown('''
    ---
    ''')
    st.table(df.query('Churn == 1').describe())
    st.write("**Insight** : ")
    st.write('- Pelanggan yang churn mayoritas adalah non-senior citizen (75.53%), tetapi ada sekitar 25.47% pelanggan yang churn merupakan senior citizen.')
    st.write('- Masa berlangganan (tenure) pelanggan churn memiliki nilai rata-rata yang relatif rendah (17.98 bulan), artinya mayoritas pelanggan yang churn telah menggunakan layanan selama kurang dari 2 tahun.')
    st.write('- Biaya bulanan (monthly charges) pelanggan churn memiliki rata-rata yang relatif rendah (74.44 dollar), namun dengan standar deviasi yang cukup tinggi (24.67 dollar), sehingga ada pelanggan churn dengan biaya bulanan yang sangat rendah (18.85 dollar) atau sangat tinggi (118.35 dollar).')
    st.write('- Total biaya (total charges) pelanggan churn memiliki rata-rata yang cukup tinggi (1531.80 dollar), namun dengan standar deviasi yang cukup tinggi juga (1890.82 dollar), sehingga ada pelanggan churn dengan total biaya yang sangat rendah (18.85 dollar) atau sangat tinggi (8684.80 dollar).')

    st.subheader('Desriptive Statistics Customer Churn - Categoric')
    st.table(df.query('Churn == 1').describe(include='O').T)
    st.write('- Mayoritas pelanggan yang churn adalah pelanggan dengan kontrak bulanan dan mayoritas juga menggunakan Fiber optic sebagai layanan internet mereka')
    st.write('- Lebih dari 60% pelanggan yang churn tidak memiliki layanan tambahan seperti online security, online backup, device protection, dan tech support.')
    st.write('-  Lebih dari setengah pelanggan yang churn memilih pembayaran menggunakan electronic check dan mayoritas pelanggan juga memilih paperless billing dan Pelanggan yang churn mayoritas adalah pelanggan individu (tidak memiliki pasangan atau tanggungan')

elif sidebar=='Eksplorasi':
    # Move selectbox widget outside the if statements
    eda_sidebar = st.sidebar.selectbox(
        "Analysis",
        ["Correlation",
         'Line Chart',
         'Bar Chart']
    )

    if eda_sidebar == 'Correlation':
        # --- Membuat Grid ----
        col1,col2 = st.columns(2)
        # --- Membuat Chart pada grid 1---
        with col1:
            st.write('Correlation Matrix With :blue[Pearson]')
            # Membuat mask untuk hanya menampilkan diagonal atas
            correlation_matrix = df.corr(method='pearson')
            mask = np.triu(np.ones_like(correlation_matrix, dtype=bool))

            fig,ax = plt.subplots()
            ax = sns.heatmap(correlation_matrix,
                            annot=True,
                            mask=mask,
                            cmap='coolwarm',
                            linewidths=0.5,
                            vmin=-1,
                            vmax=1)
            st.pyplot(fig)

        # --- Membuat Chart pada Grid 2 ---
        with col2:
            st.write('Correlation Matrix With :green[Spearman]')
            # Membuat mask untuk hanya menampilkan diagonal atas
            correlation_matrix = df.corr(method='spearman')
            mask = np.triu(np.ones_like(correlation_matrix, dtype=bool))

            fig,ax = plt.subplots()
            ax = sns.heatmap(correlation_matrix,
                            annot=True,
                            mask=mask,
                            cmap='coolwarm',
                            linewidths=0.5,
                            vmin=-1,
                            vmax=1)
            st.pyplot(fig)

        # --- Conclusion ---
        st.write('**Insight** :')
        st.markdown('''
            Dari korelasi matrix baik pearson dan spearman menunjukkan bahwa churn memiliki hubungan dengan :
            - Senior Citizen : Kekuatan korelasi cenderung lemah dan positif, ketika seseorang sudah berusia wajib memiliki KTP, kemungkinan churn bisa terjad.
            - Tenur : Korelasi Menengah dan Negative, ketika customer sudah lama berlanganan maka potensi churn akan semakin kecil.
            - Monthly Charges : Lemah dan Positif, ketika monthly charges semakin besar diterima oleh customer, potensi untuk churn meningkat.
            - Total Charges : Lemah dan Negatif, ketika customer telah menghabiskan banyak uang (dalam total) maka potensi churn semakin kecil. *kemungkinan hal ini terjadi pada customer yang telah loyal*.
        ''')

    elif eda_sidebar == 'Line Chart':
            fig,ax = plt.subplots()

            ax = df.groupby(['tenure'])['Churn'].mean()
            ax.plot(linestyle='--',
                    marker='o',
                    figsize=(10,8))
            plt.title('Churn Rate By Tenure',fontsize=14)
            plt.ylabel("Churn Rate %");
            st.pyplot(fig)

            st.write('Data menunjukkan bahwa churn rate (persentase pelanggan yang berhenti berlangganan) cenderung tinggi pada pelanggan dengan tenure rendah.')
            st.write('- Pelanggan dengan tenure 1 memiliki churn rate tertinggi yaitu 61,99%.')
            st.write('Terdapat kemungkinan bahwa pelanggan dengan tenure rendah dan churn rate tinggi kebanyakan berasal dari kontrak bulanan, karena pelanggan yang berlangganan kontrak bulanan cenderung lebih mudah untuk berhenti berlangganan jika mereka tidak puas dengan layanan yang diberikan. Namun, hal ini masih perlu diperiksa dengan memeriksa data mengenai kontrak yang dipilih oleh pelanggan yang churn.')
    
    elif eda_sidebar == 'Bar Chart':
        st.pyplot(bar_stack(df,'Contract'))
        st.markdown('''
            <div style="text-align: justify;">
            Terlihat bahwa pelanggan yang memiliki kontrak bulanan (month-to-month) memiliki churn rate yang jauh lebih tinggi dibandingkan dengan pelanggan yang memiliki kontrak satu tahun atau dua tahun. Lebih dari setengah (57.29%) dari pelanggan dengan kontrak bulanan berhenti berlangganan (churn), sedangkan pelanggan dengan kontrak satu tahun dan dua tahun memiliki churn rate yang jauh lebih rendah, yakni masing-masing 11.28% dan 2.85%. Hal ini menunjukkan bahwa pelanggan dengan kontrak bulanan cenderung lebih tidak setia dan lebih mudah untuk berhenti berlangganan.
            </div>
            ''', unsafe_allow_html=True)

        st.pyplot(bar_stack(df,'SeniorCitizen'))
        st.markdown('''
            <div style="text-align: justify;">
            Terlihat Bahwa dari Senior Citizen memiliki churn rate yang tinggi dibandingkan dengan yang bukan senior citizen.
            </div>
            ''', unsafe_allow_html=True)
        
        col1,col2 = st.columns(2)

        with col1:
                st.pyplot(bar_stack(df,'Dependents'))

        with col2:
                st.pyplot(bar_stack(df,'Partner'))

        st.markdown('''
        Dari visualisasi diatas kita dapat mengetahui bahwa :
        - Kebanyakkan yang tidak memiliki partner lebih banyak yang churn dibandingkan dengan yang memiliki partner.
        - Kebanyakkan yang churn tidak memiliki dependents.
        ''')

        
#=== Lanjut ke Eksperiment =====



    