# Capital-Inflow-and-Outflow-Forecast
阿里云——资金流入流出预测 apr/2019

Methods
The Applied Data Mining Algorithms
	As we said before, we use regression analysis to formulize the whole problem. Regression analysis is a mathematical method to deal with the correlation between multi-variates. The correlation is different from the functional relationship, the latter reflects the strict dependence of variables, while the former shows a certain degree of volatility or randomness. For each value of independent variables, dependent variables can have multiple values corresponding to it. Regression analysis and correlation analysis can be used to study the correlation in statistics.
	To be specified, multi-variate linear regression analysis has been used to solve this problem. Its general form shows as below:
Y = a + b1X1 + b2X2 + b3X3 +……+ bkXk   (1)
	It is obvious that a stands for intercept, b1, b2, b3,... bK is the regression coefficient.
Specific Implementation Approaches
	In order to implement our mathematical idea, we program a script based on Python. In the appendix part we will attach the code. In this part we are going to describe some important methods used. Here are some important excerpts of the original code:
	windows_day = [1,3,5,7,14,21,27,34,45] # Build different time windows for 1 day, 3 days, 5 days, 45 days. Seek the 16 features
	for col in rd_tra_label_col: #Through the redemption data for the next 30 days, traverse, model, and predict
	for col in rd_tpm_label_col: # Tracing, modeling, and predicting the purchase data for the next 30 days
Evaluation
Output Data
	The output is the redemption and purchase data that I need to predict during this time. (From 20140901 to 20140930)
The Origin of Data
The origin data is from the csv file provided by the competition. To be clear, the most important one is from the user_balance_table.csv.
The title gives all the data from 20130701 to 20140831. At the beginning, we can get a simple understanding of the trend of the total purchase and redemption of 427 days in the past 14 months through drawing.
