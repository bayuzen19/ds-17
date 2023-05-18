import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import ConfusionMatrixDisplay
from sklearn.metrics import f1_score
import scikitplot as skplt


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

@st.cache()
def experiment_data():
    #=== Load data ====
    data = load_data()

    #==== Scalling ====
    scalling = StandardScaler()

    #=== Define Numeric and Categoric =====

    #---- List feature numeric -----
    num = [x for x in data.select_dtypes(include=['float','int']).columns if x !='Churn']
    cat = [x for x in data.select_dtypes(exclude=['float','int']).columns if x != "gender"]

    #=== Scalling Process ====
    data[num] = scalling.fit_transform(data[num])

    #--- Handle Categoric -----
    data = pd.get_dummies(data,columns=cat,drop_first=True)

    X = data.drop(['Churn','gender'],axis=1)
    y = data['Churn']

    #=== Split Data ====
    X_train,X_test,y_train,y_test = train_test_split(X,y,
                                                    stratify=y,
                                                    test_size=0.3,
                                                    random_state=42)
    
    return X_train,X_test,y_train,y_test

def train_model(n_estimators,max_depth,max_features,bootstrap):
    rf = RandomForestClassifier(n_estimators=n_estimators,max_depth=max_depth,max_features=max_features,bootstrap=bootstrap,random_state=42)
    rf.fit(X_train,y_train)
    return rf

# Main Process
X_train,X_test,y_train,y_test = experiment_data()


#=== visualisasi ===
st.title('Machine Learning :green[Experiment] :tea:')
st.markdown('Try Different Parameter of Random Forest')

with st.form('Train Model'):
    col1,col2 = st.columns(2,gap='medium')
    with col1:
        n_estimators = st.slider('n_estimators : ',min_value=100,max_value=1000)
        max_depth = st.slider('Max Depth : ',min_value=2,max_value=20)
        max_features = st.selectbox('Max Features : ', options=['sqrt','log2',None])
        bootstrap = st.checkbox("Bootstrap")

    submitted = st.form_submit_button('Train')

    if submitted:
        rf_class = train_model(n_estimators,max_depth,max_features,bootstrap)

        # Make prediciton and evaluation
        y_test_preds = rf_class.predict(X_test)
        y_train_preds = rf_class.predict(X_train)

        y_train_proba = rf_class.predict_proba(X_train)
        y_test_proba = rf_class.predict_proba(X_test)

        # Evaluation
        with col2:
            col21,col22 = st.columns(2,gap='medium')

            with col21:
                st.metric('Test F-1 Score', value="{:.2f} %".format(100*(f1_score(y_test,y_test_preds))))
            with col22:
                st.metric('Train F-1 Score', value="{:.2f} %".format(100*(f1_score(y_train,y_train_preds))))

            st.markdown("### Confussion Matrix")
            figure = plt.figure(figsize=(6,6))
            ax = figure.add_subplot(111)

            skplt.metrics.plot_confusion_matrix(y_test,y_test_preds,ax=ax)
            st.pyplot(figure,use_container_width=True)

        st.markdown("### ROC & Precission-Recall Curves")
        col31,col32 = st.columns(2,gap='medium')

        with col31:
            figure_roc = plt.figure(figsize=(8,6))
            ax_roc = figure_roc.add_subplot(111)
            skplt.metrics.plot_roc(y_test,y_test_proba,ax=ax_roc)
            st.pyplot(figure_roc,use_container_width=True)

        with col32:
            figure_rc = plt.figure(figsize=(8,6))
            ax_rc = figure_rc.add_subplot(111)
            skplt.metrics.plot_precision_recall(y_test,y_test_proba,ax=ax_rc)
            st.pyplot(figure_rc,use_container_width=True)

        # Feature Importance
        feature_importance = rf_class.feature_importances_
        importance_df = pd.DataFrame({'Feature': X_train.columns, 'Importance': feature_importance})
        importance_df = importance_df.sort_values(by='Importance', ascending=False)

        plt.figure(figsize=(10, 6))
        ax_imp = sns.barplot(x='Importance', y='Feature', data=importance_df)
        plt.title('Feature Importance')
        plt.xlabel('Importance')
        plt.ylabel('Feature')

        st.pyplot(ax_imp.figure, use_container_width=True)





