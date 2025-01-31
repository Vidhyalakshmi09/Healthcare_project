import pandas as pd
import mysql.connector 
import streamlit as st
import plotly.express as px


mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "Root",
        database="Healthcare",
        autocommit = True)
mycursor = mydb.cursor()


def data_to_sql(df,table_name):
  from sqlalchemy import create_engine

  database_url='mysql://root:Root@localhost:3306/Healthcare'
  engine=create_engine(database_url)
  df.to_sql(name=table_name,con=engine,if_exists='append',index_label=False)
  engine.dispose()

def HOME():
    st.title("Healthcare Data Dashboard")

    
    st.markdown('<h2 style="color: red;">Welcome to the Healthcare Data Analysis</h2>', unsafe_allow_html=True)

    st.markdown("""
    This interactive dashboard allows users to explore healthcare data with visualizations for:
    
    - Monthly Admissions
    - Diagnosis Analysis
    - Bed Occupancy Analysis
    - Length of Stay Distribution
    - Seasonal Admission Patterns
    - Doctor Analysis
    - And more!
    """)

def Business_case_study():

    choice= st.selectbox('Select_the_Business_Case',['Trends in Admission Over Time analysis','Diaganosis analysis','Bed_Occupancy analysis',
                         ' Length of Stay Distribution ',' Seasonal Admission Patterns',' Doctor Analysis ',' Average Length of Stay by Diagnosis ',
                         '  Doctor Average Billing ',' Total Billing by Diagnosis ',' Average Billing by Bed Occupancy ',' Bed Occupancy Count per Diagnosis ',
                         'Test Count per Diagnosis  ',' Test Count per Diagnosis and Test Type ',' Total Health Insurance by Bed Occupancy  ',
                         ' Total Health Insurance by Diagnosis '])
    
    # 1. Monthly Admissions Trend
    if choice=="Trends in Admission Over Time analysis":
        st.markdown('<h1 style="color: red;">Trends in Admission Over Time analysis</h1>', unsafe_allow_html=True)

        sql1="""SELECT YEAR(Admit_Date) AS Year, MONTH(Admit_Date) AS Month, COUNT(Patient_ID) AS Monthly_Admissions
        FROM healthcare
        GROUP BY YEAR(Admit_Date), MONTH(Admit_Date)
        ORDER BY Year, Month;"""
        mycursor.execute(sql1)
        data=mycursor.fetchall()
        df1= pd.DataFrame(data, columns=["Year","Month","Monthly_Admissions"])


        df1['Date'] = pd.to_datetime(df1[['Year', 'Month']].assign(DAY=1))

        st.line_chart(df1,x="Date", y="Monthly_Admissions")
        st.dataframe(df1)


    # 2. Diagnosis Analysis

    if choice=='Diaganosis analysis':
        st.markdown('<h1 style="color: red;">Diaganosis analysis</h1>', unsafe_allow_html=True)
        sql2="""SELECT
                    Diagnosis,  
                    count(Diagnosis) as Diagnosis_count
                    FROM healthcare
                GROUP BY Diagnosis
                ORDER BY count(Diagnosis) DESC
                LIMIT 5;"""

        mycursor.execute(sql2)
        data=mycursor.fetchall()
        df2 = pd.DataFrame(data, columns=["Diagnosis","Diagnosis_count"])


        st.bar_chart(df2.set_index('Diagnosis')['Diagnosis_count'])

        st.dataframe(df2)

    # 3. Bed Occupancy Analysis
    if choice=='Bed_Occupancy analysis':

        st.markdown('<h1 style="color: red;">Bed_Occupancy analysis</h1>', unsafe_allow_html=True)
        sql3="""SELECT 
                    Bed_Occupancy, 
                    count(Patient_ID) AS Occupancy_Count
                    FROM healthcare
                GROUP BY Bed_Occupancy
                ORDER BY count(Patient_ID) DESC;"""

        mycursor.execute(sql3)
        data=mycursor.fetchall()
        df3= pd.DataFrame(data, columns=["Bed_Occupancy","Occupancy_Count"])

        fig = px.pie(df3, names="Bed_Occupancy", values="Occupancy_Count", title="Bed Occupancy Proportions")
        st.plotly_chart(fig)

        st.dataframe(df3)


    # 4. Length of Stay Distribution
    if choice==' Length of Stay Distribution ':


        st.markdown('<h1 style="color: red;"> Length of Stay Distribution </h1>', unsafe_allow_html=True)

        sql4="""SELECT
                    AVG(DATEDIFF(Discharge_Date, Admit_Date)) AS Average_Length_of_Stay,
                    MAX(DATEDIFF(Discharge_Date, Admit_Date)) AS Maximum_Length_of_Stay
            FROM healthcare;"""

        mycursor.execute(sql4)
        data=mycursor.fetchall()
        df4 = pd.DataFrame(data, columns=["Average_Length_of_Stay","Maximum_Length_of_Stay"])

        st.bar_chart(df4, stack=False)

        st.dataframe(df4)

    # 5. Seasonal Admission Patterns 
    if choice==' Seasonal Admission Patterns':

        st.markdown('<h1 style="color: red;"> Seasonal Admission Patterns</h1>', unsafe_allow_html=True)
        sql5="""SELECT 
                    MONTH(Admit_Date) AS Month, 
                    COUNT(Patient_ID) AS Monthly_Admissions
                    FROM healthcare
                GROUP BY MONTH(Admit_Date)
                ORDER BY MONTH(Admit_Date);"""
        mycursor.execute(sql5)
        data=mycursor.fetchall()
        df5 = pd.DataFrame(data, columns=["Month","Monthly_Admissions"])

        st.line_chart(df5,x="Month", y="Monthly_Admissions")
        st.dataframe(df5)

    # 6. Doctor Analysis
    if choice==' Doctor Analysis ':

        st.markdown('<h1 style="color: red;"> Doctor Analysis </h1>', unsafe_allow_html=True)
        sql6="""SELECT 
                    Doctor,
                    COUNT(Patient_ID) AS Number_Of_Patients
                    FROM healthcare
                GROUP BY Doctor
                ORDER BY Number_Of_Patients;"""
        mycursor.execute(sql6)
        data=mycursor.fetchall()
        df6= pd.DataFrame(data, columns=["Doctor","Number_Of_Patients"])

        fig = px.pie(df6, names="Doctor", values="Number_Of_Patients", title="Doctor's No Of Patients Proportions")
        st.plotly_chart(fig)

        st.dataframe(df6)

    

    # 7. Average Length of Stay by Diagnosis
    if choice==' Average Length of Stay by Diagnosis ':

        st.markdown('<h1 style="color: red;"> Average Length of Stay by Diagnosis </h1>', unsafe_allow_html=True)
        sql7="""SELECT 
                    Diagnosis, 
                    AVG(DATEDIFF(Discharge_Date, Admit_Date)) AS Avg_Length_of_Stay
                    FROM healthcare
                GROUP BY Diagnosis;"""

        mycursor.execute(sql7)
        data=mycursor.fetchall()
        df7 = pd.DataFrame(data, columns=["Diagnosis","Avg_Length_of_Stay"])

        st.bar_chart(df7,x="Diagnosis",y="Avg_Length_of_Stay")

        st.dataframe(df7)

    # 8. Doctor's Average Billing
    if choice=='  Doctor Average Billing ':

        st.markdown('<h1 style="color: red;">  Doctor Average Billing </h1>', unsafe_allow_html=True)

        sql8="""SELECT 
                    Doctor,
                    AVG(`Billing Amount`) AS Average_Billing
                    FROM healthcare
                GROUP BY Doctor;"""
        mycursor.execute(sql8)
        data=mycursor.fetchall()
        df8 = pd.DataFrame(data, columns=["Doctor","Average_Billing"])

        fig = px.pie(df8, names="Doctor", values="Average_Billing", title="Doctor's Average Billing Proportions")
        st.plotly_chart(fig)

        st.dataframe(df8)

    # 9. Total Billing by Diagnosis
    if choice==' Total Billing by Diagnosis ':

        st.markdown('<h1 style="color: red;"> Total Billing by Diagnosis </h1>', unsafe_allow_html=True) 

        sql9="""SELECT 
                    Diagnosis,
                    SUM(`Billing Amount`) AS Total_Billing
                    FROM healthcare
                GROUP BY Diagnosis
                ORDER BY Total_Billing DESC;"""
        mycursor.execute(sql9)
        data=mycursor.fetchall()
        df9 = pd.DataFrame(data, columns=["Diagnosis","Total_Billing"])
        st.bar_chart(df9,x="Diagnosis",y="Total_Billing")

        st.dataframe(df9)

    # 10. Average Billing by Bed Occupancy

    if choice==' Average Billing by Bed Occupancy ':

        st.markdown('<h1 style="color: red;"> Average Billing by Bed Occupancy </h1>', unsafe_allow_html=True)


        sql10="""SELECT 
                    Bed_Occupancy,
                    AVG(`Billing Amount`) AS Average_Billing
                    FROM healthcare
                GROUP BY Bed_Occupancy
                ORDER BY Average_Billing DESC;"""
        mycursor.execute(sql10)
        data=mycursor.fetchall()
        df10 = pd.DataFrame(data, columns=["Bed_Occupancy","Average_Billing"])
        fig = px.pie(df10, names="Bed_Occupancy", values="Average_Billing", title="Bed's Average Billing Proportions")
        st.plotly_chart(fig)

        st.dataframe(df10)



    # 11. Bed Occupancy Count per Diagnosis

    if choice==' Bed Occupancy Count per Diagnosis ':

        st.markdown('<h1 style="color: red;"> Bed Occupancy Count per Diagnosis </h1>', unsafe_allow_html=True)

        sql11="""SELECT 
                    Diagnosis, 
                    Bed_Occupancy,
                    COUNT(Patient_ID) AS Occupancy_Count
                    FROM healthcare
                GROUP BY Diagnosis, Bed_Occupancy
                ORDER BY Occupancy_Count DESC;"""
        mycursor.execute(sql11)
        data=mycursor.fetchall()
        df11 = pd.DataFrame(data, columns=["Diagnosis","Bed_Occupancy","Occupancy_Count"])

        fig1 = px.bar(
            df11,
            x='Diagnosis',           
            y='Occupancy_Count',     
            color='Bed_Occupancy',   
            title="Bed Occupancy Count per Diagnosis",
            labels={"Diagnosis": "Diagnosis", "Occupancy_Count": "Occupancy Count", "Bed_Occupancy": "Bed Occupancy Type"},
            barmode='stack',         
            height=600              
        )
        st.plotly_chart(fig1)

        st.dataframe(df11)

    # 12. Test Count per Diagnosis 

    if choice=='Test Count per Diagnosis  ':

        st.markdown('<h1 style="color: red;">Test Count per Diagnosis  </h1>', unsafe_allow_html=True)


        sql12="""SELECT 
                    Test, 
                    COUNT(Patient_ID) AS Test_Count
                    FROM healthcare
                GROUP BY Test
                ORDER BY Test_Count DESC;"""
        mycursor.execute(sql12)
        data=mycursor.fetchall()
        df12 = pd.DataFrame(data, columns=["Test","Test_Count"])
        st.line_chart(df12,x="Test", y="Test_Count")

        st.dataframe(df12)

    # 13. Test Count per Diagnosis and Test Type

    if choice==' Test Count per Diagnosis and Test Type ':


        st.markdown('<h1 style="color: red;"> Test Count per Diagnosis and Test Type </h1>', unsafe_allow_html=True)

        sql13="""SELECT 
                    Diagnosis, 
                    Test, 
                    COUNT(Patient_ID) AS Test_Count
                    FROM healthcare
                GROUP BY Diagnosis, Test
                ORDER BY Test_Count DESC;"""
        mycursor.execute(sql13)
        data=mycursor.fetchall()
        df13 = pd.DataFrame(data, columns=["Diagnosis","Test","Test_Count"])
        fig = px.bar(
            df13, 
            x='Test',  
            y='Test_Count',  
            color='Diagnosis',  
            title="Test Count per Diagnosis and Test Type",
            labels={"Test": "Test Type", "Test_Count": "Test Count", "Diagnosis": "Diagnosis"},
            barmode='stack', 
            height=600  
        )
        st.plotly_chart(fig)

        st.dataframe(df13)


    # 14. Total Health Insurance by Bed Occupancy 

    if choice==' Total Health Insurance by Bed Occupancy  ':

        st.markdown('<h1 style="color: red;"> Total Health Insurance by Bed Occupancy  </h1>', unsafe_allow_html=True)


        sql14="""SELECT 
                    Bed_Occupancy,
                    SUM(`Health Insurance Amount`) AS Total_Insurance
                    FROM healthcare
                GROUP BY Bed_Occupancy
                ORDER BY Total_Insurance DESC;"""
        mycursor.execute(sql14)
        data=mycursor.fetchall()
        df14 = pd.DataFrame(data, columns=["Bed_Occupancy","Total_Insurance"])
        st.bar_chart(df14,x="Bed_Occupancy",y="Total_Insurance")

        st.dataframe(df14)


    # 15. Total Health Insurance by Diagnosis

    if choice==' Total Health Insurance by Diagnosis ':

        st.markdown('<h1 style="color: red;"> Total Health Insurance by Diagnosis </h1>', unsafe_allow_html=True)


        sql15="""SELECT 
                    Diagnosis,
                    SUM(`Health Insurance Amount`) AS Total_Insurance
                    FROM healthcare
                GROUP BY Diagnosis
                ORDER BY Total_Insurance DESC;"""
        mycursor.execute(sql15)
        data=mycursor.fetchall()
        df15 = pd.DataFrame(data, columns=["Diagnosis","Total_Insurance"])
        fig = px.pie(df15, names="Diagnosis", values="Total_Insurance", title="Diagnosis to total Inaurance Proportions")
        st.plotly_chart(fig)

        st.dataframe(df15)





   
page = st.sidebar.radio("Navigation", ["Home", "Business Case Study"])
if page == "Home":
    HOME()
elif page == "Business Case Study":
    Business_case_study()   



