### Fleximart Data Warehouse & Analytics Project

### Project Overview
This project implements a **Data Warehouse solution** for the Fleximart business using a **Star Schema architecture**.  
It supports analytical reporting such as sales performance, customer segmentation, and time-based analysis.

The repository contains:
- Database schema definitions
- Star schema design documentation
- Data loading scripts
- Analytical SQL queries for business insights

---
### Project Structure

.
├── warehouse_schema.sql        # Creates dimension and fact tables
├── warehouse_data.sql          # Inserts sample / processed data
├── star_schema_design.md       # Star schema documentation & explanation
├── analytics_queries.sql       # Business analytics SQL queries
└── README.md                   # Project documentation

### Technologies Used

SQL (MySQL / PostgreSQL compatible)

Data Warehouse Concepts

Star Schema Modeling

### Data Warehouse Architecture

Schema Type : Star Schema

### Fact Table:

fact_sales

### Dimension Tables:

dim_customer

dim_product

dim_date

The design enables efficient OLAP-style analytical queries such as aggregations, trends, and segmentation.

Detailed schema explanation is available in:
star_schema_design.md

## Setup Instructions

1. Create the database
2. Execute `warehouse_schema.sql` to create tables
3. Execute `warehouse_data.sql` to load data
4. Run queries from `analytics_queries.sql` for analysis

### Analytics & Reporting

All analytical queries are available in:
analytics_queries.sql

### Key Insights Covered:

 Top products by revenue

 Revenue contribution percentage

 Customer segmentation (High / Medium / Low value)

 Monthly, quarterly, yearly sales trends

 Total sales quantity analysis

These queries are optimized for data warehouse reporting using aggregations and joins.

### Sample Analytics Use Cases

Identify top-performing products

Analyze customer spending behavior

Track sales trends for 2024

Understand category-wise revenue contribution

### Documentation :

| File Name               | Description                     |
| ----------------------- | ------------------------------- |
| `warehouse_schema.sql`  | Defines fact & dimension tables |
| `warehouse_data.sql`    | Loads warehouse data            |
| `star_schema_design.md` | Explains schema design          |
| `analytics_queries.sql` | Analytical SQL queries          |

### Best Practices Followed

Star schema modeling

Separation of schema, data, and analytics

Readable and optimized SQL queries

Business-friendly analytical outputs


