
<a href="https://sssingh-human-resource-data-analysis-streamlit-srcapp-6qnlbm.streamlit.app/"  target="_blank"><img src="https://img.shields.io/badge/open_app_in_streamlit-FFFFFF?style=for-the-badge&logo=streamlit&logoColor=red" /></a>


# Human Resource Analysis
In this `Data Analysis` project, we examine raw HR data to learn more about how organizational policies influence employee behaviors such as `attrition` and `job-satisfaction` plus staff `promotions` and `layoffs`. The company's human resources policies shall then be amended based on the insights obtained.

<img src="https://github.com/sssingh/human-resource-data-analysis-streamlit/blob/main/images/title.png?raw=true" width="1000" height="500" /> <br><br>

## Features
⚡Multipage Interactive Dashboard  
⚡Deployed on cloud [Report accessible on the web]  
⚡Streamlit  
⚡Plotly    
⚡Pandas    

## Table of Contents
- [Introduction](#introduction) 
- [Objective](#objective)
- [Dataset](#dataset)
- [Solution Approach](#solution-approach)
- [How To Use](#how-to-use)
- [License](#license)
- [Credits](#credits)
- [Get in touch](#get-in-touch)


## Introduction
* `Datamatrix-ml Inc.` is one of the top financial research firms, specializing in cutting-edge financial market research. It has over 1400 employees.
* The R&D department of the company creates the exclusive financial research reports and advice papers
* The company's sales division is in charge of finding the customers for its research goods.
* The HR department is actively gathering data through internal questionnaires, interviews, and HR employment records to evaluate the efficacy of the workforce given the human-centric aspect of the corporate work culture.

## Requirements
As part of their yearly evaluation of the employees and HR policies, the HR department has requested us to undertake a confidential data analysis project in order to gain insights into its workforce management. The questions that the HR department is seeking answers to are listed below.....

|Requirement ID|For Whom|Requirement Description|
|:--|:---|:--|
HR-DA01-REQ-1|Executive Committee|How gender-balanced is our workforce today? <br> Should we concentrate on employing more employees of a certain gender in the upcoming fiscal year?
HR-DA01-REQ-2|Executive Committee|Do you think our organization is young or aging? <br> Should we concentrate on hiring people in a specific age and gender group?
HR-DA01-REQ-3|Executive Committee|How evenly distributed in terms of marital status is the work force?
HR-DA01-REQ-4|Executive Committee|Does the gender distribution of employees at the departmental level match that of the entire company?
HR-DA01-REQ-5|Executive Committee|Does the gender distribution of employees at the departmental level match that of the entire company?
HR-DA01-REQ-6|Executive Committee|How is each department performing on average in terms of "overtime," "manager's employee retention," and compensation?
HR-DA01-REQ-7|Executive Committee|Based on their job experience, are our employee distributions balanced? <br> Do we require targeted hiring for a specific spectrum of job experience? <br> Do employees wish to spend the majority of their careers working with our company?
HR-DA01-REQ-8|Rightsizing Team| How well are we doing on our 10% promotion goal? <br> Are we at or below the maximum 5% rate of performance-based layoffs? <br> Are the promotion and layoff rates at the departmental level consistent with those at the corporate level?
HR-DA01-REQ-9|Hiring & Retention Team| Do we have a higher-than-10% attrition rate? <br> What are the elements that cause attrition directly?
HR-DA01-REQ-10|Executive Committee <br> Rightsizing Team <br> Hiring & Retention Team| Need ability to filter and drill-down into data by `Gender`, `Department`, `Education`, `Job Role`, `Age` and `Work Experience`

***Table-1 : Requirements***

## Dataset
* The HR department collects and maintains the dataset. The relevant employee-related data attributes are provided by HR as a CSV dataset, and. 
* The dataset is anticipated to be evaluated and updated yearly in the same manner before being fed into the suggested data-analysis solution. 
* The `input_data` folder in the project repository contains the [raw dataset](https://github.com/sssingh/human-resource-data-analysis-streamlit/blob/main/input_data/raw_hr_data.csv).
* Along with raw data the HR departments has supplied the `business-rules` to be used to compute employee's `promotion-rate`, `retrenchment-rate` and `attrition-rate`

|Data Item|Rule  
|:--|:---
| Promotion % Rate | [Count of to-be-promoted] = <br> &nbsp;&nbsp;&nbsp;&nbsp; (if [yrs-since-last-promotion] >= 10 yrs and [performance-rating] is > 2) <br> **[promotion-rate]** = [Count of to-be-promoted] / [total-employee]) * 100 
| Retrenchment % Rate  | [Count of to-be-retrenched] = <br> &nbsp;&nbsp;&nbsp;&nbsp;(if [Not-to-be-promoted] and ((if [years-in-current-role] is between 3 to 10 years and [performance-rating] is > 2) <br> OR (If [years-in-current-role] is >= 10 years and [performance-rating] < 3)) <br> **[retrenchment-rate]** = [Count of to-be-retrenched] / [total-employee]) * 100
| Attrition % Rate | **[attrition-rate]** = [Count of employee left] / [total-employee] * 100 

***Table-2 : Rate Computation Rules***


## Solution Approach 
The solution uses the 'Streamlit' and 'plotly' libraries to construct a fully interactive web-based cloud-hosted report dashboard. In order to gain insights and provide answers to the queries specified in [Table-1: Requirements](#requirements), the report includes the pertinent plots and tables. By zooming in on and filtering out a certain plot, users can interact with plotly plots. Additionally, the solution offers a group of global data filters that users can utilize to filter data throughout the entire application. These filters also dynamically change the visuals to reflect the data that remains after filtering. Users now have the option to explore specific areas of interest in the dataset by cutting, dicing, and drilling down.


|Requirement ID|Solution ID|Proposed Solution|
|:--|:---|:--|
|HR-DA01-REQ-1 <br> HR-DA01-REQ-2 <br> HR-DA01-REQ-3 <br> HR-DA01-REQ-4 <br> HR-DA01-REQ-5 <br> HR-DA01-REQ-6 <br> HR-DA01-REQ-7|HR-DA01-SOL-1|To assist in providing answers to queries in the appropriate requirements, <br> a dedicated dashboard with interactive visualizations at the summary level <br> will be constructed|
|HR-DA01-REQ-8 <br> HR-DA01-REQ-9|HR-DA01-SOL-2|To assist in providing answers to queries regarding respective <br> requirements, a dedicated dashboard comprising interactive <br> visualizations relating to promotions and layoffs (capacity) will be created.|
|HR-DA01-REQ-10|HR-DA01-SOL-3|To assist in addressing queries on pertinent requirements, a dedicated <br> dashboard including dynamic visuals relevant to attrition will be constructed.|


### Exploratory Data Analysis (EDA) and Feature Engineering [pandas]:
The EDA and feature-engineering have been done using `pandas` to comprehend, become comfortable with, and verify the sanity of the given data. Using the pandas Python library, the `data-exploration,` `data-cleaning,` and `feature-engineering` have been completed. We are generally checking...
* Presence of any missing values 
 * Any unusual value (outliers) 
 * Incorrect values (e.g., sales column, we see -ve numbers)
 * Determine `categorical` and `numeric` columns
 * Determine dimensions of categorical columns and range of numeric columns
 * Create new features required to show relevant data/numbers in the report 

### Report Creation [Streamlit, pandas, plotly]:
To put the suggested idea into practice, three interactive report dashboards (report tabs) will be developed. For specific requirements and the related proposed solution, see [Table-3: Proposed Solution](#solution-approach).  
There are several graphics on each report dashboard, divided into expandable and collapsible sections. Each section provides the queries we're attempting to address along with any pertinent insights gained from the illustrations.  

#### 1. Executive Summary Dashboard [HR-DA01-SOL-1]:
'Gender', 'Age', 'Marital Status', 'Department', and 'Work Experience' are all examined in this high-level summary dashboard. This dashboard includes the sections below...
##### *Gender & Age and Marital Status Statistics:* <br><br>
<img src="https://github.com/sssingh/human-resource-data-analysis-streamlit/blob/main/images/summary-01.png?raw=true" width="1000" height="500" /><br><br>


##### *Department & Work Experience:* <br><br>
<img src="https://github.com/sssingh/human-resource-data-analysis-streamlit/blob/main/images/summary-02.png?raw=true" width="1000" height="500" /><br><br>


#### 2. Capacity Dashboard [HR-DA01-SOL-2]:
This dashboard emphasizes the size and capabilities of the company's staff. This analysis will aid the business in its "rightsizing" decision in near future. This dashboard includes the sections below...
##### *Summary level & Department level promotion and layoffs statistics:* <br><br>
<img src="https://github.com/sssingh/human-resource-data-analysis-streamlit/blob/main/images/capacity-all.png?raw=true" width="1000" height="500" /><br><br>

  
#### 3. Attrition Dashboard [HR-DA01-SOL-3]:
This dashboard looks at the company's capacity for employee retention and determines what variables are at play if attrition rates are higher than anticipated. The corporation may change its practices to better manage attrition in light of the findings. <br><br>
 
<img src="https://github.com/sssingh/human-resource-data-analysis-streamlit/blob/main/images/attrition-all.png?raw=true" width="1000" height="500" />


## How To Use
### Read-only direct access via the web (Recommended):
<a href="https://sssingh-human-resource-data-analysis-streamlit-srcapp-6qnlbm.streamlit.app/"  target="_blank"><img src="https://img.shields.io/badge/open_app_in_streamlit-FFFFFF?style=for-the-badge&logo=streamlit&logoColor=red" /></a> <br>
and explore the fully functional interactive report. <br><br>

### Run the application locally:
To run (and modify) the application locally follow below steps...
1. Clone this repo
2. From within the root folder of the application install all dependencies by running
    ```python...
    pip install requirements.txt  
    ```
3. From within the root folder of the application run the application...
    ```python...
    streamlit run src/app.py  
    ```
4. Copy and paste the `localhost:<port-no>` web-address displayed by above command in your browser to open and application.


## License
[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)

## Get in touch
[![website](https://img.shields.io/badge/web_site-8B5BE8?style=for-the-badge&logo=ko-fi&logoColor=white)](https://www.datamatrix-ml.com)
[![twitter](https://img.shields.io/badge/twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white)](https://twitter.com/@thesssingh)
[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/sssingh/)


[Back To The Top](#human-resource-analysis)


