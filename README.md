# Welcome to my portfolio!

Welcome to my data analyst portfolio! This repository showcases my skills, project experience, and approach to solving real-world data problems. Here, you'll find selected projects that demonstrate my expertise in data cleaning, transformation, modeling, and visualization. My goal is to provide clear, actionable insights through data-driven analysis.

---

## **About Me**

I'm an operations data analyst based in Stockholm, Sweden, with a passion for transforming raw data into meaningful insights. My background includes hands-on experience with data cleaning, Power BI (especially Power Query), and building models that support business decisions. I also enjoy table tennis, hiking, disc-golf and sci-fi.

---

## **Portfolio Projects**

Each project below includes a summary, objectives, data sources, tools used, and key outcomes.

### **1. Power BI / Operations Health Dashboard**

- **Summary:** The Operations Health Dashboard is a Power BI project designed to provide a unified view of infrastructure insights of a mid-sized software development company. By integrating data from multiple sources, the dashboard empowers operations managers to monitor key performance indicators (KPIs), identify bottlenecks, and drive data-informed decision-making.
- **Objectives:**  
  - Centralize Operations Data: Consolidate disparate operational data sources into a single, user-friendly dashboard.  
  - Monitor KPIs: Track critical metrics such as order fulfillment rates, inventory turnover, delivery lead times, and incident rates.  
  - Enable Proactive Management: Provide early warning signals for potential operational issues.
  - Enhance Data-Driven Culture: Facilitate regular performance reviews and continuous improvement initiatives.
- **Data:**  
  - Jira Project and Issue Management System
  - Incident records ( key, priority, incident_start, fault_caused_by, area, function, duration, response_time, turn_over_drop, change_caused_by )
- **Tools & Skills:**  
  - Power BI Desktop: For report and dashboard creation
  - Power Query: For data cleaning, transformation, and merging multiple data sources  
  - DAX (Data Analysis Expressions): For advanced calculations and KPI creation
  - Scheduled Data Refresh: Ensuring near real-time data availability
  - Custom Visuals: For intuitive, interactive data exploration
- **Key Outcomes:**  
  - Improved Visibility: Stakeholders gained a clear, at-a-glance view of operational health across departments.  
  - Faster Issue Resolution: Early detection of process bottlenecks led to a 20% reduction in incident response times.  
  - Data-Driven Decisions: Regular use of the dashboard in weekly meetings resulted in more targeted improvement initiatives.
  - Scalability: The modular design allows for easy integration of new data sources and KPIs as business needs evolve.

### **2. Python / Jira Data Extraction Pipeline**

- **Summary:** The 'Jira Data Extraction Pipeline' is a Python-based project designed to automate the extraction, transformation, and storage of issue tracking data from Jira. The pipeline streamlines reporting and analytics by providing clean, structured datasets ready for further analysis or visualization.
- **Objectives:**  
  - Automate Data Collection: Seamlessly extract issue data from Jira using its REST API.  
  - Data Cleaning & Transformation: Standardize and enrich raw data for consistency and usability.
  - Enable Analytics: Store processed data in a format suitable for Power BI dashboards and ad-hoc analysis.
  - Scalability: Build a modular pipeline that can be easily adapted to new Jira projects or data requirements.
- **Data:**  
  - Source: Jira Cloud REST API
  - Incident records ( key, priority, incident_start, fault_caused_by, area, function, duration, response_time, turn_over_drop, change_caused_by )
  - Format: JSON (raw), transformed to CSV/Parquet for downstream use
- **Tools & Skills:**  
  - Python Libraries: requests, pandas, pyyaml, sqlalchemy
  - ETL Orchestration: Modular scripts with logging and error handling
  - Storage: Processed data saved to local files
- **Key Outcomes:**  
  - Reduced manual data extraction time by 90%
  - Delivered clean, analysis-ready datasets for Power BI  
  - Created reusable codebase for future Jira analytics projects
  - Improved data quality and consistency for reporting

---

## **Data Sources**

- All data used is either open-source or anonymized for demonstration purposes

---

## **Future Work**

- Expand portfolio with more projects using Power BI and Python programming techniques
- Add interactive dashboards and real-time data analysis examples
- Explore new domains (e.g., sports analytics, sci-fi movie data)


