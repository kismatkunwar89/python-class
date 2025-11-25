# Customer Management Portal

A Flask-based web application for managing customer information.

## Features

- **Search Customers** - Find customers by number or name
- **View All Customers** - Browse complete customer list with sorting
- **Add Customer** - Register new customer records
- **Edit Customer** - Update existing customer information
- **Delete Customer** - Remove customer records

## Tech Stack

- **Backend**: Flask, Python 3, PyMySQL
- **Frontend**: Semantic UI, jQuery
- **Database**: MySQL (chargerstore database)

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure database connection in `web.py` (lines 8-12)

3. Run the application:
```bash
python web.py
```

4. Access at: `http://127.0.0.1:5000`

## Project Structure

```
web-python-class/
├── web.py                          # Main Flask application
├── templates/
│   ├── base.html                   # Base template with navigation
│   ├── home.html                   # Homepage with search and action cards
│   ├── customers_list.html         # Customer list table
│   ├── create_customer.html        # New customer form
│   ├── edit_customer.html          # Edit customer form
│   ├── result.html                 # Customer search results
│   └── macros/
│       └── customer_form.html      # Reusable form macro
├── requirements.txt                # Python dependencies
└── test_db.py                      # Database connection test
```

## Database Schema

Table: `customers`
- customerNumber (PK)
- customerName
- contactLastName, contactFirstName
- phone
- addressLine1, addressLine2
- city, state, postalCode, country
- salesRepEmployeeNumber
- creditLimit

## License

Educational project for Python class.
