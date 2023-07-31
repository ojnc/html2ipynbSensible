#| **Skip to Content**
#|  __
#| SAP Community Log-in Update
#| In a few months, SAP Community will switch to SAP Universal ID as the only option to login. Don’t wait, create your SAP Universal ID
#| now\! If you have multiple S- or P- accounts, use the Consolidation Tool to merge your content.
#| Get started with SAP Universal ID
#|  __
#|   - Home
#|   - Community
#|   - Ask a Question
#|   - Write a Blog Post
#|   - Login / Sign-up
#|   -
#| ###### Technical Articles
#| Andreas Forster
#| __
#| July 27, 2020 21 minute read
#| # Hands-On Tutorial: Automated Predictive \(APL\) in SAP HANA Cloud
#| __14 __37 __7,162
#| SAP HANA Cloud now includes the Automated Predictive Library \(APL\). Find out how to train ML models within SAP HANA Cloud
#| automatically, without having to extract the data. Use the familiar SAP HANA Python Client API for ML to trigger the required
#| calculations in the SAP HANA Cloud straight from your preferred Python environment. Most of the code is also relevant for SAP HANA
#| on-premise.
#| If you are in a hurry, you can read through this blog to become familiar with this concept. If you want to dig deep, you can follow
#| the implementation steps and learn hands-on.
#| This blog was written by both Marc Daniau \(Product Expert, SAP\) and Andreas FORSTER \(Global Center of Excellence, SAP\).
#| Therefore, the term "we" in this blog refers to ourselves, Marc and Andreas, and not necessarily SAP. There is no guarantee or
#| support for any information or code in this blog. Please test any content that you may want to use yourself.
#| Our thanks go to Frank Gottfried, Christoph Morgen and Raymond Yao for their help in putting this tutorial together\!
#| # Table of contents
#|   - Introduction / Use case
#|   - Setup SAP HANA Cloud
#|   - Setup local Python
#|   - Create SAP HANA user
#|   - Data upload
#|   - Data exploration
#|   - Train ML model
#|   - Apply ML model
#|   - Deployment
#|   - Summary
#| # Introduction / Use case
#| SAP HANA Cloud is the latest evolution of SAP HANA. Released in March 2020, it combines the technology known from the on-premise
#| version of SAP HANA with cloud benefits such as scalability.
#| It contains many of the known SAP HANA engines, such as the Automated Predictive Library \(APL\). The APL, which is a highly
#| automated ML framework, has also been evolving and now includes a "Gradient Boosting Classification". This new Gradient Boosting
#| Classification automates the process of finding an ML model, similar to the previous APL. The new Gradient Classification approach
#| however tends to result in stronger models. Since the APL product group is focussing further improving this approach, we suggest
#| working with the new "Gradient Boosting Classification", as we do in this blog.
#| The APL can be called through SQL or directly from Python. In this blog we make use of Python and the corresponding library
#| hana\_ml, which simplifies the calling of SAP HANA functionality. We will call the APL, but the library can also call the Predictive
#| Algorithm Library \(PAL\).
#| As example to work with the Gradient Boosting Classification, we will predict the affinity of a Banking customer to sign up for a
#| term deposit, in which money can be locked for a certain period and accrues higher interest rates.
#| # Setup SAP HANA Cloud
#| To implement this Bank Marketing scenario you need access to SAP HANA Cloud. This SAP HANA Cloud with the following configuration:
#|   - It must have at least 3 virtual CPUs \(vCPUs\). The current SAP HANA Cloud Trial comes only with 2 vCPUs. In that trial it is not possible to increase the number of vCPUs. Therefore you must create your own instance of SAP HANA Cloud in the SAP Cloud Platform Cockpit as described in this playlist from the SAP HANA Academy, which also contains plenty of additional material.
#|   - Your SAP HANA Cloud must have the Script Server enabled to be able to use the Automated Predictive Library \(APL\). For a new SAP HANA Cloud instance the Script Server can be enabled when creating the instance. For existing sytems, the Script Server can be activated with a Service Request.
#|   - Your SAP HANA Cloud must permit connections from your IP address, e.g. by selecting "Allow all IP addresses".
#| The "Getting Started with SAP HANA Cloud" guide also gives an excellent overview, just bear in mind that you cannot use the trial
#| environment to implement this blog's hands-on scenario. Denys van Kempen has also put together a huge collection of SAP HANA Cloud
#| material. In case you might be a little puzzled about the different version of SAP HANA that have been around, Denys has also
#| created a SAP \(HANA\) Cheat Sheet.
#| There is also a Learning Article on Using Jupyter Notebooks with SAP HANA Cloud that helps with the first steps.
#| To continue hands-on, you need to know:
#|   - The SAP HANA Cloud endpoint \(e.g. xyz.hanacloud.ondemand.com\)
#|   - The HTTPS port, which is always 443
#|   - The password for the DBADMIN user
#| # Setup local Python
#| You need an environment to execute Python code. In case you already have an environment to work with, please use it. In case you are
#| new to Python, we suggest installing Anaconda, which will install and configure everything that is needed.
#| Once you have downloaded and installed Anaconda, open the Anaconda Navigator and select JupyterLab.
#| An alternative, and much faster, approach to open JupyterLab is through the Anaconda Prompt. Open the Anaconda Prompt, then type:
#| jupyter lab
#| If you haven't worked with JupyterLab so far, not to worry It's easy to find your way around. One very useful introduction for the
#| first steps is this tutorial from the California Institute of Technology \(Caltech\).
#| With Python at your fingertips, create a new Python 3 Notebook and install SAP's hana\_ml library, which provides the connectivity
#| and push-down to the SAP HANA Cloud.
!pip install hana_ml
#| After installation, check on the version that has been installed.
import hana_ml
print(hana_ml.__version__)
#| You should have at least version 2.5.20062605 for connecting to SAP HANA Cloud. This tutorial was tested with version 2.5.20062609.
#| # Create SAP HANA user
#| Test the connectivity by running a very simple SELECT statement. You will need the SAP HANA Cloud endpoint, HDB port and the DBADMIN
#| user's password. Here we see the password in clear text only for a quick test. Later on, we will securely store the passwords.
import hana_ml.dataframe as dataframe
# Instantiate connection object
conn = dataframe.ConnectionContext(address = 'yourendpoint',
                                   port = 443,
                                   user = 'DBADMIN',
                                   password = 'yourpassword',
                                   encrypt = 'true',
                                   sslValidateCertificate = 'false'
                                  )
# Send basic SELECT statement and display the result
sql = 'SELECT 12345 FROM DUMMY'
df_remote = conn.sql(sql)
print(df_remote.collect())
#| If everything works as expected, the code should return the value 12345. Later on you will see how to keep the password secure. For
#| now we continue with the connection to create a user on the SAP HANA Cloud to call the Automated Predictive Library.
#| Create a user called ML, just change the password.
cursor = conn.connection.cursor()
cursor.execute('CREATE USER ML Password "YOURPASSWORD" SET USERGROUP DEFAULT;')
#| Keep things simple by specifying that the user does not have to change the password. Note that this is recommended only for
#| technical users.
cursor.execute('ALTER USER ML DISABLE PASSWORD LIFETIME;')
#| Grant the new ML user the right to call the Automated Predictive Library.
cursor.execute('GRANT "sap.pa.apl.base.roles::APL_EXECUTE" TO ML')
#| Grant the ML user the right to call the Predictive Algorithm Library. This right is needed in this tutorial only so that the Boxplot
#| that you will see later can be calculated in SAP HANA.
cursor.execute('GRANT "AFL__SYS_AFL_AFLPAL_EXECUTE_WITH_GRANT_OPTION" TO ML')
#| Close the connection that was established with the DBADMIN user. From now on, we will use only the ML user.
cursor.close()
#| However, we don't want to have the password visible in clear text. Use the Secure User Store from the SAP HANA client to securely
#| store the logon credentials.
#| Navigate in a command prompt \(cmd.exe\) to the folder that contains the hdbuserstore, e.g.
#| C:\Program Files\SAP\hdbclient
#| Then store the logon parameters in the Secure User Store, by calling the hdbuserstore application. In the example below the
#| parameters are saved under a key called MYHANACLOUD. You are free to chose your own name.
#| C:\Program Files\SAP\hdbclient>hdbuserstore -i SET MYHANACLOUD “YOURENDPOINT:PORT” ML
#| The password is not specified in the above command as you will be prompted for it. Just note that the logon credentials have not
#| been tested yet. They have only been saved.
#| Use the stored credentials to logon without having to show the password.
import hana_ml.dataframe as dataframe
# Instantiate connection object
conn = dataframe.ConnectionContext(userkey = 'MYHANACLOUD',
                                   encrypt = 'true')
# Send basic SELECT statement and display the result
sql = 'SELECT 12345 FROM DUMMY'
df_remote = conn.sql(sql)
print(df_remote.collect())
# Close connection
conn.close()
#| The result of the SELECT statement has not changed of course. Now you are good to keep working with the ML user.
#| # Data upload
#| Your system is ready. Now you need to fill it with data to work with. We will be working with the "Bank Marketing Data Set" as
#| shared by the UC Irvine Machine Learning Repository. Download bank.zip and extract the file bank-full.csv.
#| Place the bank-full.csv into your JupyterLab environment, for example by uploading it through the File Browser.
#| Create another Python 3 Notebook and rename it to "10 data upload". Begin with loading the CSV file into a Pandas DataFrame.
import pandas as pd
df_data = pd.read_csv('bank-full.csv', sep = ';')
df_data.head(5)
#| Before uploading the data to SAP HANA Cloud, carry out a few transformations. Turn the column headers into upper case.
df_data.columns = map(str.upper, df_data.columns)
#| Drop the DURATION column. It tells how many minutes the calls lasted when the term deposit was promoted. This column cannot be used
#| as predictor to score a person's interest in signing up for the product. Before we call the person, we don't know the length of the
#| phone call. Hence remove it from the DataFrame.
df_data = df_data.drop(['DURATION'],
                       axis = 1)
#| The target column is currently called just 'Y'. Rename it to something more self-explanatory.
df_data = df_data.rename(index = str, columns = {'Y': 'PURCHASE'})
#| Add an ID column.
df_data.insert(0, 'CUSTOMER_ID', df_data.reset_index().index)
#| Preview a few rows of the transformed data.
df_data.head(5)
#| We are happy with the data, so upload it to SAP HANA Cloud. Establish a connection with the hana\_ml wrapper…
import hana_ml.dataframe as dataframe
conn = dataframe.ConnectionContext(userkey = 'MYHANACLOUD',
                                   encrypt = 'true')
#| … and upload the Pandas DataFrame into a table called BANKMARKETING.
df_remote = dataframe.create_dataframe_from_pandas(connection_context = conn,
                                                   pandas_df = df_data,
                                                   table_name = 'BANKMARKETING',
                                                   force = True,
                                                   replace = False)
#| Once we have trained a Machine Learning model, we want to apply it on new data. Therefore create a second table, in which you load
#| two rows of "invented" customers, whose behaviour will be predicted.
#| Create a new DataFrame, just without the target column.
df_topredict = pd.DataFrame(data = None,
                            columns = df_data.columns.drop('PURCHASE'))
for xx in df_topredict.columns:
    df_topredict[xx] = df_topredict[xx].astype(df_data[xx].dtypes.name)
#| Add the two imaginary customers.
df_topredict = pd.concat([df_topredict, pd.DataFrame({'CUSTOMER_ID': 1,
                                    'AGE': 40,
                                    'JOB': 'entrepreneur',
                                    'MARITAL': 'married',
                                    'EDUCATION': 'secondary',
                                    'DEFAULT': 'no',
                                    'BALANCE': 3000,
                                    'HOUSING': 'yes',
                                    'LOAN': 'no',
                                    'CONTACT': 'unknown',
                                    'DAY': 10,
                                    'MONTH': 'may',
                                    'CAMPAIGN': 1,
                                    'PDAYS': -1,
                                    'PREVIOUS': 0,
                                    'POUTCOME': 'unknown'}, index=[0])])
df_topredict = pd.concat([df_topredict, pd.DataFrame({'CUSTOMER_ID': 2,
                                    'AGE': 65,
                                    'JOB': 'management',
                                    'MARITAL': 'single',
                                    'EDUCATION': 'tertiary',
                                    'DEFAULT': 'no',
                                    'BALANCE': 3000,
                                    'HOUSING': 'no',
                                    'LOAN': 'no',
                                    'CONTACT': 'telephone',
                                    'DAY': 10,
                                    'MONTH': 'mar',
                                    'CAMPAIGN': 1,
                                    'PDAYS': -1,
                                    'PREVIOUS': 12,
                                    'POUTCOME': 'success'}, index=[0])])
#| Upload the new Pandas DataFrame into a table called BANKMARKETING\_TOPREDICT.
df_remote = dataframe.create_dataframe_from_pandas(connection_context = conn,
                                                   pandas_df = df_topredict,
                                                   table_name = 'BANKMARKETING_TOPREDICT',
                                                   force = True,
                                                   replace = False)
#| # Data exploration
#| Now the real fun can start. Begin the Data Science part by exploring the data that we have to work with. Create a new Python 3
#| Notebook called "20 Data exploration".
#| Connect to SAP HANA Cloud.
import hana_ml.dataframe as dataframe
conn = dataframe.ConnectionContext(userkey = 'MYHANACLOUD',
                                   encrypt = 'true')
#| Create a SAP HANA dataframe and point it to the table with the uploaded data. Sort the dataframe to ensure reproducibility.
df_remote = conn.table(table = 'BANKMARKETING', schema = 'ML').sort('CUSTOMER_ID', desc = False)
df_remote.head(5).collect()
#| Alternatively, you can also base the SAP HANA dataframe on a SELECT statement.
df_remote = conn.sql('SELECT * FROM "ML"."BANKMARKETING" ORDER BY "CUSTOMER_ID" ASC')
df_remote.head(5).collect()
#| Start exploring with the basics. How many rows are in the source?
df_remote.count()
#| 45211\. This value was calculated by SAP HANA. Only the final outcome was transferred back to Python.
#| What are the names and types of the data columns?
df_remote.dtypes()
#| Each column is listed with its name, type and size. The last two values are relevant when the data type is DECIMAL or SPATIAL.
#| Now get some detailed column statistics, similar to how Pandas describes a DataFrame.
df_remote.describe().collect()
#| It's not obvious by looking at this table, but each cell was calculated in SAP HANA Cloud. The massive SQL statement that was
#| created by the hana\_ml wrapper can be retrieved.
df_remote.describe().select_statement
#| Look closer at the target variable. How many people bought the product? And how much is that in percent?
top_n = 5
variable_name = 'PURCHASE'
# Get Top N categories
total_count = df_remote.count()
df_remote_col_frequency = df_remote.agg([('count', variable_name, 'COUNT')],  group_by = variable_name)
df_col_frequency = df_remote_col_frequency.sort("COUNT", desc = True).head(top_n).collect()
df_col_frequency['PERCENT'] = round(df_col_frequency['COUNT'] / total_count, 2)
df_col_frequency.style.format({'COUNT':'{0:,.0f}', 'PERCENT':'{0:,.1%}'}).hide(axis='index')
#| A plot also helps to quickly understand the numbers.
%matplotlib inline
df_col_frequency.plot.bar(x = 'PURCHASE', y = 'COUNT', title = 'Top ' + str(top_n));
#| Use a box plot to compare the buyers from the non-buyers based on the balance in their bank account.
import matplotlib.pyplot as plt
from hana_ml.visualizers.eda import EDAVisualizer
f = plt.figure()
ax1 = f.add_subplot(111) # 111 refers to 1x1 grid, 1st subplot
eda = EDAVisualizer(ax1)
ax, cont = eda.box_plot(data = df_remote, column = 'BALANCE', groupby = 'PURCHASE', outliers = True)
#| That's a bit of a surprise. The contacts with the highest balances did not sign up for the term deposit. We are ready to train our
#| Machine Learning model.
#| # Train ML model
#| Create a new Python 3 Notebook called “30 Train ML model”.
#| Connect to SAP HANA Cloud.
import hana_ml.dataframe as dataframe
conn = dataframe.ConnectionContext(userkey = 'MYHANACLOUD',
                                   encrypt = 'true')
#| Create a SAP HANA dataframe and point it to the table with the uploaded data. Sort the dataframe to ensure reproducibility.
#| Alternatively, you can also base the SAP HANA dataframe on a SELECT statement as shown in the above "Data exploration" chapter.
df_remote = conn.table(table = 'BANKMARKETING', schema = 'ML').sort('CUSTOMER_ID', desc = False)
df_remote.head(5).collect()
#| Create an object of type GradientBoostingBinaryClassifier, which will train the APL model.
from hana_ml.algorithms.apl.gradient_boosting_classification import GradientBoostingBinaryClassifier
gbapl_model = GradientBoostingBinaryClassifier()
#| Specify the target variable and the value the model should predict. By default the model will predict the occurrence of the less
#| frequent value. Even though we want to predict the less common behaviour. it's prudent to be specific, which also helps document the
#| model behaviour.
col_target = 'PURCHASE'
target_value = 'yes'
#| Specify the ID column.
col_id = 'CUSTOMER_ID'
#| Specify the predictor columns. Just remove the target and id columns.
col_predictors = df_remote.columns
col_predictors.remove(col_target)
col_predictors.remove(col_id)
col_predictors
#| Further configure how the model will be trained.
gbapl_model.set_params(eval_metric = 'AUC') # Metric used to evaluate the model performance
gbapl_model.set_params(cutting_strategy = 'random with no test') # Internal splitting strategy
gbapl_model.set_params(other_train_apl_aliases={'APL/VariableAutoSelection': 'true',
                                                'APL/Interactions': 'true',
                                                'APL/InteractionsMaxKept': 10,
                                                'APL/TargetKey': target_value})
#| Start the learning process. This might take a minute to calculate. The APL is now automatically going through the steps a Data
#| Scientist would have to carry out manually. It is pre-processing the data, e.g. with binning, grouping or imputation, before
#| calculating and testing different Gradient Boosting models.
gbapl_model.fit(data = df_remote,
                key = col_id,
                features = col_predictors,
                label = col_target)
#| When the model has been found, look at it's quality metric.
import pandas as pd
list_performance = gbapl_model.get_performance_metrics()
df_performance = pd.DataFrame(list(list_performance.items()), columns=['METRIC', 'VALUE'])
df_performance.loc[df_performance['METRIC'].isin(['AUC', 'BestIteration'])].style.hide(axis='index')
#| We have an AUC of 0.82. The model was found in iteration number 276 in our case. A lot more information is available about the
#| model. Looks at the basics, how many variables and records were used?
df_summary = gbapl_model.get_summary().filter("KEY in ('ModelVariableCount', 'ModelSelectedVariableCount', 'ModelRecordCount', 'ModelBuildDate')").collect()
df_summary = df_summary[['KEY','VALUE']]
df_summary['KEY'] = df_summary['KEY'].str.replace('Model', '').str.replace('Selected', 'Selected ')
df_summary['KEY'] = df_summary['KEY'].str.replace('Count', ' Count').str.replace('Date', ' Date')
df_summary.style.hide(axis='index')
#| All records from the dataset were used of course. You had provided 15 different variables for the model to consider. Plus the target
#| variable \(PURCHASE\) and the ID \(CUSTOMER\_ID\) in total 17 variables were touched.
#| Before looking deeper at the variables that were selected for the models, which ones have been excluded?
df_excluded = gbapl_model.get_indicators().filter("KEY like 'VariableExclusion%'").collect()
df_excluded = df_excluded[['VARIABLE','VALUE']]
df_excluded.columns = ['Excluded Variable', 'Reason']
df_excluded.style.hide(axis='index')
#| Three predictor variables were dropped. But how important are the chosen / remaining variables for the model? The APL provides
#| detailed information about the model that helps understand the model's behaviour. This is often called Global Explainable ML / AI. A
#| Data Scientist might be interested to know, that the feature importance is based on Shapley.
list_contributions = gbapl_model.get_feature_importances()['ExactSHAP']
df_contribution = pd.DataFrame(list(list_contributions.items()), columns=['VARIABLE', 'CONTRIBUTION'])
df_contribution['CUMULATIVE'] = df_contribution['CONTRIBUTION'].cumsum()
format_dict = {'CONTRIBUTION':'{0:,.2%}','CUMULATIVE':'{0:,.2%}'}
df_contribution.style.format(format_dict).hide(axis='index')
#| Most important is the CONTACT variable, followed by the MONTH in which the customer was contacted.
#| A pareto plot helps see the importance of the variables. First ensure, that the seaborn package, which is used for the charting, is
#| actually installed.
!pip install seaborn
#| Now the plot can be created.
import matplotlib.pyplot as plt
import seaborn as sns
from  matplotlib.ticker import PercentFormatter
f = plt.figure()
ax1 = f.add_subplot(111) # 111 refers to 1x1 grid, 1st subplot
ax2 = ax1.twinx()
sns.barplot(data = df_contribution,
             x = 'VARIABLE',
             y = 'CONTRIBUTION',
             color = '#1f77b4',
             ax=ax1)
sns.lineplot(data = df_contribution, sort=False,
             x = 'VARIABLE',
             y = 'CUMULATIVE',
             color = 'red',
             ax=ax2)
ax1.set_xticklabels(ax1.get_xticklabels(),rotation=30)
ax1.yaxis.set_major_formatter(PercentFormatter(1))
ax2.yaxis.set_major_formatter(PercentFormatter(1))
ax2.set_ylim(0, 1)
plt.show();
#| So far we see which variables are most important to the model. You might be wondering though, what information is correlating with
#| the behaviour you are looking for. During which months for example were the Marketing activities most successful. We can look into
#| each variable and understand their behaviour in more detail.
#| Obtain the detailed variable contribution for the MONTH.
variable_name = 'MONTH'
df_category_profit = gbapl_model.get_indicators().filter("KEY = 'GroupNormalProfit' and VARIABLE = '" + variable_name + "'").collect()
df_category_profit = df_category_profit[['VARIABLE', 'TARGET', 'DETAIL', 'VALUE']]
df_category_profit['VALUE'] = df_category_profit['VALUE'].astype(float)
df_category_profit.columns = ['Predictor', 'Target','Category','Profit']
df_category_profit = df_category_profit.sort_values(by = ['Profit'], ascending = False)
df_category_profit.style.format({'Profit':'{0:,.2%}'}).hide(axis='index')
#| And bring these details into a plot.
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
plt.figure()
bplot = sns.barplot(data = df_category_profit, x = 'Category', y = 'Profit', color = '#1f77b4')
bplot.set_title(variable_name)
bplot.set_xticklabels(bplot.get_xticklabels(), rotation = 45);
bplot.yaxis.set_major_formatter(PercentFormatter(1))
#| Categories on the left hand side in the above chart have the highest proportion of the target population. This means the purchasing
#| affinity \(influence\) was highest when the customer was contacted in March, September, October or December.
#| The categories are sorted in descending order of the proportion / influence. When the influence \(y-axis\) becomes negative, the
#| target proportion of the category is lower than the overall's population. This means people were less likely to purchase. People
#| were not keen to buy the product in May. In summary: the further left the category on the x-axis, the higher the affinity.
#| Plot the category significance for some other variables. AGE is interesting for example. The relationship between age and purchasing
#| affinity is not linear.
#| For those who want to look a little deeper into the model, view the correlations between the input variables. The APL can calculate
#| a full correlation matrix, as all input variables are encoded numerically. APL can deal with highly correlation variables, so you
#| don't have to go this deep. However, in case there are highly correlated variables you can consider dropping these from the input
#| variables to speed up the calculation time.
df_correlations = gbapl_model.get_indicators().filter("KEY = 'CorrelatedVariable'").collect()
df_correlations = df_correlations[['VARIABLE', 'DETAIL', 'VALUE']]
df_correlations['VALUE'] = df_correlations['VALUE'].astype(float).round(3)
df_correlations.columns = ['1st Variable', '2nd Variable', 'Coefficient']
df_correlations = df_correlations.sort_values(by = ['Coefficient'], ascending = False)
df_correlations.style.hide(axis='index')
#| There is nothing that would concern us here, but these three variables have fairly strong correlations to each other.
#| Another optional deep-dive is a look at the interactions, which the model found between the variables.
df_interactions = gbapl_model.get_indicators().filter("KEY = 'InteractionValue' and to_char(VALUE) <> '0'").collect()
df_interactions = df_interactions[['VARIABLE', 'DETAIL', 'VALUE']]
df_interactions['VALUE'] = df_interactions['VALUE'].astype(float).round(3)
df_interactions.columns = ['1st Variable', '2nd Variable', 'Interaction']
df_interactions = df_interactions.sort_values(by = ['Interaction'], ascending = False)
df_interactions.style.format({'Interaction':'{0:,.3f}'}).hide(axis='index')
#| No strong interactions were found. We are just showing them here for you to know, that the APL's new
#| GradientBoostingBinaryClassifier captures these automatically. These interactions can also be very relevant in interpreting the
#| model's logic.
#| Let's have a look at one further detail, that we can use later on. The model will be using SHAP scores for the predictions. With the
#| complete trained model still available at the moment, we can find out the threshold score, which will be used to separate positive
#| and negative predictions.
df_threshold = gbapl_model.get_indicators().filter("KEY = 'Threshold'").collect()
df_threshold = df_threshold[['VARIABLE', 'VALUE']]
df_threshold['VALUE'] = df_threshold['VALUE'].astype(float)
df_threshold.columns = ['Target', 'Score Treshold']
df_threshold.style.hide(axis='index')
#| Scores below -1.15998 will lead to negative predictions. Scores above will lead to positive predictions.
#| This score can be converted to the corresponding probability value:
import math
score = df_threshold.iloc[0, 1]
1 / (1 + math.exp(-score))
#| We are now familiar with the model and could use it right away for predictions. However, it's also a good moment to save the model
#| first to the SAP HANA Cloud.
from hana_ml.model_storage import ModelStorage
MODEL_SCHEMA = 'ML' # HANA schema in which models are to be saved
model_storage = ModelStorage(connection_context=conn, schema = MODEL_SCHEMA)
gbapl_model.name = 'Bank Marketing Model'
model_storage.save_model(model=gbapl_model, if_exists = 'replace')
#| # Apply ML model
#| Let's use the model to create predictions\! Create a new Python 3 Notebook called “40 Apply ML model”.
#| Connect to SAP HANA Cloud.
import hana_ml.dataframe as dataframe
conn = dataframe.ConnectionContext(userkey = 'MYHANACLOUD',
                                   encrypt = 'true')
#| Create the SAP HANA DataFrame, which points to the table with the entities that need to be predicted. Sort the data for
#| reproducibility.
df_remote_new = conn.table(table = 'BANKMARKETING_TOPREDICT', schema = 'ML').sort("CUSTOMER_ID", desc = False)
df_remote_new.head(5).collect()
#| Load the trained ML model.
from hana_ml.model_storage import ModelStorage
MODEL_SCHEMA = 'ML' # HANA schema from where models are to be loaded
model_storage = ModelStorage(connection_context = conn, schema = MODEL_SCHEMA)
gbapl_model = model_storage.load_model(name = 'Bank Marketing Model', version = 1)
#| Apply the model to predict the behaviour of the two customers. For each person we obtain an overall probability of purchasing the
#| product \(proba\_PURCHASE\) and the yes / no prediction.
gbapl_model.set_params(extra_applyout_settings =
                        {'APL/ApplyExtraMode': 'Advanced Apply Settings',
                         'APL/ApplyDecision': 'true',
                         'APL/ApplyProbability': 'true',
                         'APL/ApplyPredictedValue': 'false'
                        })
df_remote_predict = gbapl_model.predict(df_remote_new)
df_predict = df_remote_predict.head(10).collect()
df_predict.columns = [hdr.replace('gb_', '') for hdr in df_predict.columns] # shorten column names
df_predict.style.format({'proba_PURCHASE':'{0:,.3f}'}).hide(axis='index')
#| If you would like to understand which characteristics of a customer contributed towards a positive or negative prediction, you can
#| leverage the so called SHAP values.
gbapl_model.set_params(extra_applyout_settings={'APL/ApplyExtraMode': 'Individual Contributions'})
df_remote_predict = gbapl_model.predict(df_remote_new)
df_predict = df_remote_predict.head(10).collect()
df_predict.columns = [hdr.replace("gb_", "") for hdr in df_predict.columns] # Shorten column names
df_predict
#| Each prediction relates to a SHAP value \(score\_PURCHASE\), which itself is a sum of the SHAP values of the individual predictors,
#| which are also shown. The higher the overall score, the higher the probability the person will purchase the product. Earlier on we
#| saw the threshold that is used to differentiate between positive and negative predictions \(1.15998 in this case\).
#| If you want to better understand how the variables contributed to these individual predictions \(local explainable ML / AI, just
#| rearrange the data format and visualise them in a plot.
df_contributions_single = df_predict[df_predict['CUSTOMER_ID'] == 2]
df_contributions_single = df_contributions_single.melt(id_vars = ['CUSTOMER_ID', 'PREDICTED', 'score_PURCHASE'])
df_contributions_single.columns = ['CUSTOMER_ID', 'PREDICTED', 'SCORE', 'VARIABLE', 'CONTRIBUTION']
df_contributions_single = df_contributions_single.sort_values(by = ['CONTRIBUTION'], ascending = [False])
df_contributions_single.style.format({'CONTRIBUTION':'{0:,.3f}'})
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
%matplotlib inline
plt.figure()
bar_color = np.where(df_contributions_single['CONTRIBUTION'] > 0 ,'green', 'red')
bplot = sns.barplot(data = df_contributions_single, x = 'VARIABLE', y = 'CONTRIBUTION',  palette = bar_color.tolist())
bplot.set_title('Contributions')
bplot.set_xticklabels(bplot.get_xticklabels(), rotation = 90)
plt.axhline(y = 0, color = 'grey', linewidth = 1)
plt.ylim(-2.5, 2.5);
#| The above plot shows the variable's contribution for customer number 2. Towards the left the variables that contributed most
#| strongly to a positive prediction are shown. The "contrib\_constant\_bias" shown in the plot is not a variable. It is an element of
#| the trained model, which can be interpreted as an average, which is adjusted by the individual variables.
#| Write the predictions to a table in SAP HANA Cloud, where other processes or Analytical tools like SAP Analytics Cloud can pick them
#| up.
df_remote_predict.save(where=('ML', 'BANKMARKETING_PREDICTED'),
                       table_type = 'COLUMN',
                       force = True)
#| Just close the connection, and you are done.
conn.close()
#| # Deployment
#| SAP Data Intelligence provides the platform to deploy HANA ML models into production. Its "ML Scenario Manager" for example combines
#| Jupyter Notebooks for creation with graphical pipelines for deployment.
#| You can deploy both the Automated Predictive Library \(APL\) and the Predictive Algorithm Library \(PAL\) as well as open source
#| like Python or R.
#| It is important that your HANA ML operators use a recent version of the Python library hana\_ml \(version 2.5.x\). This is already
#| the case with SAP Data Intelligence Cloud.
#| # Summary
#| Well done for making it to the end of this tutorial\! You have connected to SAP HANA Cloud, uploaded and explored data, before
#| training a Machine Learning model, whose logic you explored. Until eventually you applied the model to create predictions, whose
#| drivers you also looked at.
#| Hopefully you had fun along the way and want to work with this further\! You can continue with the next hands-on tutorial, in which
#| you score your APL model in stand-alone JavaScript. Independent of SAP HANA, this provides deployment flexibility. You could use the
#| model in an IoT scenario, directly at the edge. Or wherever JavaScript can run.
#| Here are some further links you might find useful.
#|   - SAP HANA Python Client API for Machine Learning Algorithms
#|   - Documentation SAP HANA Automated Predictive Library
#|   - Sample Notebooks for the Automated Predictive Library
#|   - Updates for the Data Scientist, building SAP HANA embedded Machine Learning scenarios from Python or R
#| Marc Daniau and Andreas Forster
#| Follow __Like __RSS Feed
