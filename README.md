# Streamlit-Expense-Tracker

# Streamlit Expense Tracker

A comprehensive web application built with Streamlit for tracking personal expenses, incomes, and visualizing financial data.

## Table of Contents

1. [Installation](#installation)
2. [Usage](#usage)
3. [Features](#features)
4. [Structure](#structure)
5. [Improvements and Suggestions](#improvements-and-suggestions)
6. [Security and Data Validation](#security-and-data-validation)
7. [Testing](#testing)
8. [Contributing](#contributing)
9. [License](#license)

## Installation

Before installing the application, ensure you have Python installed on your system.

**Clone the Repository**

```bash
git clone https://github.com/your-repository/ExpenseTracker.git
cd ExpenseTracker
```

**Set Up a Virtual Environment** (Optional but recommended)

```bash
python3 -m venv venv
source venv/bin/activate  # For Unix or MacOS
venv\Scripts\activate  # For Windows
```

**Install Dependencies**

```bash
python3 -m pip install -r requirements.txt
```

**Run the Application**

```bash
streamlit run main.py
```

## Usage

After installation, the application can be accessed at `localhost:8501` in your web browser.

1. **Register/Login** : Start by creating an account or logging in.
2. **Data Entry** : Input your incomes and expenses.
3. **Visualization** : View graphical representations of your financial data.
4. **Tracking** : Keep track of monthly installments and other recurring expenses.

## Features

* **User Authentication** : Secure login and registration system.
* **Expense Tracking** : Categorized entry for expenses and incomes.
* **Data Visualization** : Sankey diagrams for understanding spending patterns.
* **Monthly Tracker** : A dedicated section for tracking monthly installments.
* **Responsive UI** : Clean and intuitive user interface.

## Structure

The application is structured into several modules:

* `app.py`: Main application logic.
* `authenticator.py`: Handles user authentication.
* `database.py`: Manages data storage and retrieval.
* `settings.py`: Streamlit app settings and custom styles.
* `util.py`: Utility functions and constants.
* `navigation.py`, `period.py`, `currency.py`, etc.: Modules for specific functionalities like navigation, period handling, and currency settings.

## Improvements and Suggestions

* Add more robust error handling and user feedback.
* Enhance UI/UX for a more intuitive user experience.
* Implement thorough data validation and security practices.
* Consider adding features like budget alerts and export/import functionality.

## Security and Data Validation

Ensure secure handling of user data, especially passwords and personal information. Implement client-side and server-side validation to prevent malicious inputs.

## Testing

Implement unit and integration tests to ensure the reliability and stability of the application.

## Contributing

Contributions to the project are welcome. Please follow the standard fork-and-pull request workflow.

## License

This project is open-source and available under the [MIT License](https://opensource.org/licenses/MIT).
