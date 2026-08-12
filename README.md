# QA Automation Framework — SauceDemo

**Python · Selenium WebDriver · PyTest · Page Object Model · GitHub Actions**

[![CI Pipeline](https://img.shields.io/badge/CI-GitHub%20Actions-2088FF?logo=githubactions\&logoColor=white)]()
[![Python](https://img.shields.io/badge/Python-3.12%2B-3776AB?logo=python\&logoColor=white)]()
[![Selenium](https://img.shields.io/badge/Selenium-4.24-43B02A?logo=selenium\&logoColor=white)]()
[![PyTest](https://img.shields.io/badge/PyTest-8.3-0A9EDC?logo=pytest)]()
[![Allure](https://img.shields.io/badge/Reports-Allure-FF6E00)]()
[![License](https://img.shields.io/badge/License-MIT-lightgrey)]()

A portfolio-ready **end-to-end web automation framework** built using Python, Selenium WebDriver, and PyTest against the [SauceDemo](https://www.saucedemo.com/) e-commerce application.

The framework demonstrates real-world QA automation practices including **Page Object Model (POM), explicit waits, data-driven testing, cross-browser testing, automated screenshots, logging, test reporting, Git/GitHub, and CI/CD with GitHub Actions**.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Application Under Test](#application-under-test)
3. [Objectives](#objectives)
4. [Key Features](#key-features)
5. [Technology Stack](#technology-stack)
6. [Test Coverage](#test-coverage)
7. [Framework Architecture](#framework-architecture)
8. [Project Structure](#project-structure)
9. [Prerequisites](#prerequisites)
10. [Installation](#installation)
11. [Configuration](#configuration)
12. [How to Run the Project](#how-to-run-the-project)
13. [Test Reports](#test-reports)
14. [Screenshots](#screenshots)
15. [CI/CD](#cicd)
16. [Design Decisions](#design-decisions)
17. [Future Improvements](#future-improvements)
18. [License](#license)

---

# Project Overview

This project is an automated testing framework designed to validate the major workflows of the SauceDemo e-commerce application.

The framework follows a **Page Object Model architecture** where:

* Test files contain business-level test scenarios.
* Page classes contain page-specific elements and actions.
* Utility classes provide reusable framework functionality.
* PyTest manages test execution, fixtures, assertions, and parameterization.
* Allure and pytest-html generate test reports.
* GitHub Actions executes the tests automatically in CI/CD.

The current test suite covers the complete user journey:

**Login → Inventory → Cart → Checkout → Logout**

---

# Application Under Test

**Website:** https://www.saucedemo.com/

SauceDemo is used as the primary application for practicing and demonstrating Selenium automation.

The framework automates scenarios related to:

* User login
* Invalid login
* Product inventory
* Product sorting
* Add/remove products
* Shopping cart
* Checkout
* Order completion
* Logout
* Negative scenarios
* Data-driven login testing

---

# Objectives

The main objectives of this project are to demonstrate practical knowledge of:

* Selenium WebDriver
* Web element interaction
* Selenium locators
* Explicit waits
* PyTest
* Fixtures
* Assertions
* Parameterization
* Page Object Model
* Data-driven testing
* Cross-browser testing
* Automated screenshots
* Logging
* Test reporting
* Git/GitHub
* CI/CD automation

---

# Key Features

| Feature                  | Implementation         |
| ------------------------ | ---------------------- |
| **Automation Tool**      | Selenium WebDriver     |
| **Programming Language** | Python                 |
| **Test Framework**       | PyTest                 |
| **Design Pattern**       | Page Object Model      |
| **Browsers**             | Chrome, Firefox, Edge  |
| **Synchronization**      | Explicit waits         |
| **Data-Driven Testing**  | OpenPyXL + Excel       |
| **Test Data Generation** | Faker                  |
| **Assertions**           | PyTest assertions      |
| **Fixtures**             | PyTest fixtures        |
| **Reporting**            | Allure + pytest-html   |
| **Screenshots**          | Automatic on failure   |
| **Logging**              | File + console logging |
| **Retry Mechanism**      | pytest-rerunfailures   |
| **Configuration**        | config.ini             |
| **Version Control**      | Git/GitHub             |
| **CI/CD**                | GitHub Actions         |
| **Dashboard**            | Custom HTML dashboard  |

---

# Technology Stack

### Programming

* Python 3.12+

### Automation

* Selenium WebDriver
* WebDriver Manager

### Testing

* PyTest
* PyTest Fixtures
* PyTest Parameterization
* pytest-rerunfailures
* pytest-xdist

### Test Data

* OpenPyXL
* Faker

### Reporting

* Allure
* pytest-html
* Custom HTML Dashboard

### DevOps

* Git
* GitHub
* GitHub Actions

---

# Test Coverage

The framework currently contains test suites for:

```text
Login
Inventory
Cart
Checkout
Logout
```

The project includes functional, negative, security-oriented, and data-driven scenarios.

### PyTest markers

The following markers are available:

```text
smoke
regression
login
inventory
cart
checkout
logout
negative
security
```

---

# Framework Architecture

```text
                    ┌─────────────────────┐
                    │      PyTest         │
                    │  Test Execution     │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Test Cases        │
                    │ tests/              │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Page Object Model   │
                    │ pages/              │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │     Utilities       │
                    │ Driver / Wait /     │
                    │ Config / Logging    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Selenium WebDriver  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │     SauceDemo       │
                    └─────────────────────┘
```

---

# Project Structure

```text
QA-Automation-Framework/
│
├── tests/
│   ├── test_login.py
│   ├── test_inventory.py
│   ├── test_cart.py
│   ├── test_checkout.py
│   └── test_logout.py
│
├── pages/
│   ├── base_page.py
│   ├── login_page.py
│   ├── inventory_page.py
│   ├── cart_page.py
│   ├── checkout_page.py
│   ├── checkout_overview_page.py
│   └── checkout_complete_page.py
│
├── utilities/
│   ├── config_reader.py
│   ├── driver_factory.py
│   ├── logger.py
│   ├── wait_utils.py
│   ├── screenshot_utils.py
│   ├── excel_utils.py
│   └── data_generator.py
│
├── config/
│   └── config.ini
│
├── testdata/
│   └── login_data.xlsx
│
├── screenshots/
│
├── logs/
│
├── reports/
│   ├── allure-results/
│   ├── allure-report/
│   ├── html-report/
│   └── dashboard/
│       └── index.html
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── conftest.py
├── requirements.txt
├── pytest.ini
├── README.md
└── .gitignore
```

---

# Prerequisites

Before running the project, make sure the following are installed.

### 1. Python

Python **3.12 or higher**

Check your installation:

```bash
python --version
```

Expected output:

```text
Python 3.12.x
```

---

### 2. Git

Check Git:

```bash
git --version
```

---

### 3. Browser

Install at least one supported browser:

* Google Chrome
* Mozilla Firefox
* Microsoft Edge

The framework uses WebDriver Manager, so manual browser-driver downloads are not required.

---

# Installation

## Step 1 — Clone the Repository

```bash
git clone https://github.com/<your-username>/QA-Automation-Framework.git
```

Move into the project directory:

```bash
cd QA-Automation-Framework
```

---

## Step 2 — Create a Virtual Environment

### Windows

```bash
python -m venv .venv
```

---

## Step 3 — Activate the Virtual Environment

### Windows CMD

```bash
.venv\Scripts\activate
```

### Windows PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

After activation, you should see something similar to:

```text
(.venv) C:\...\QA-Automation-Framework>
```

---

## Step 4 — Install Dependencies

```bash
pip install -r requirements.txt
```

Verify PyTest:

```bash
pytest --version
```

---

# Configuration

The main configuration file is:

```text
config/config.ini
```

Example:

```ini
[ENV]
active_env = qa

[qa]
base_url = https://www.saucedemo.com/
browser = chrome
headless = false
implicit_wait = 10
explicit_wait = 15
```

### Configuration options

| Option          | Description                    |
| --------------- | ------------------------------ |
| `base_url`      | Application URL                |
| `browser`       | Chrome, Firefox, or Edge       |
| `headless`      | Run browser with or without UI |
| `implicit_wait` | Implicit wait timeout          |
| `explicit_wait` | Explicit wait timeout          |

Configuration can also be overridden using PyTest command-line arguments.

---

# How to Run the Project

After installation and configuration, make sure the virtual environment is activated.

## 1. Run All Tests

```bash
pytest
```

This executes the complete test suite.

---

## 2. Run Tests in a Specific File

For example, to run login tests:

```bash
pytest tests/test_login.py
```

Run checkout tests:

```bash
pytest tests/test_checkout.py
```

---

## 3. Run a Specific Test

```bash
pytest tests/test_login.py::test_valid_login
```

Replace the test name with the actual test function you want to execute.

---

## 4. Run Smoke Tests

```bash
pytest -m smoke
```

---

## 5. Run Regression Tests

```bash
pytest -m regression
```

---

## 6. Run Tests on a Specific Browser

### Chrome

```bash
pytest --browser=chrome
```

### Firefox

```bash
pytest --browser=firefox
```

### Edge

```bash
pytest --browser=edge
```

---

## 7. Run in Headless Mode

To run Chrome without opening the browser window:

```bash
pytest --browser=chrome --headless=true
```

This is especially useful for CI/CD environments.

---

## 8. Override the Application URL

```bash
pytest --url=https://www.saucedemo.com/
```

---

## 9. Run Tests with Multiple Options

Example:

```bash
pytest --browser=firefox --headless=true
```

---

## 10. Run Tests in Parallel

If `pytest-xdist` is installed:

```bash
pytest -n auto
```

This allows PyTest to distribute tests across multiple workers.

---

## 11. Re-run Failed Tests

To run only the tests that failed during the previous execution:

```bash
pytest --lf
```

---

# Test Execution Flow

When you execute:

```bash
pytest
```

the framework follows this flow:

```text
pytest
   ↓
conftest.py
   ↓
Create WebDriver
   ↓
Load Configuration
   ↓
Execute Test
   ↓
Page Object
   ↓
Selenium WebDriver
   ↓
SauceDemo
   ↓
Assertion
   ↓
Test Result
   ↓
Screenshot if Failed
   ↓
Generate Reports
```

---

# Test Reports

The framework supports multiple reporting mechanisms.

## 1. Allure Report

After running the tests:

```bash
pytest
```

Allure results are generated in:

```text
reports/allure-results/
```

To open the report locally:

```bash
allure serve reports/allure-results
```

To generate a static report:

```bash
allure generate reports/allure-results -o reports/allure-report --clean
```

The generated report will be available at:

```text
reports/allure-report/
```

> Allure Commandline must be installed separately to use the `allure` command.

---

## 2. PyTest HTML Report

The HTML report is generated at:

```text
reports/html-report/report.html
```

Open the file in a browser after the test execution.

---

## 3. Custom Dashboard

The project also generates a custom execution dashboard:

```text
reports/dashboard/index.html
```

The dashboard displays information such as:

* Total tests
* Passed tests
* Failed tests
* Skipped tests
* Pass percentage
* Execution time

---

# Screenshots

Screenshots are automatically captured when a test fails.

They are stored in:

```text
screenshots/
```

Example:

```text
screenshots/
└── test_valid_login_2026-08-05_22-30-15.png
```

Screenshots are also attached to the Allure report for easier failure analysis.

---

# CI/CD

The project uses **GitHub Actions** for continuous integration.

Workflow file:

```text
.github/workflows/ci.yml
```

The CI pipeline can:

```text
Git Push / Pull Request
        ↓
GitHub Actions
        ↓
Install Python
        ↓
Install Dependencies
        ↓
Start Browser
        ↓
Run PyTest
        ↓
Generate Reports
        ↓
Upload Artifacts
```

The pipeline supports:

* Chrome
* Firefox
* Headless execution
* Smoke tests
* Regression tests
* Automatic retries
* Test reports
* Screenshots
* Logs
* Allure results

---

# Git Workflow

Typical development workflow:

```bash
git status
```

Add changes:

```bash
git add .
```

Commit changes:

```bash
git commit -m "Add login automation tests"
```

Push changes:

```bash
git push origin main
```

After pushing, GitHub Actions can automatically execute the test suite.

---

# Design Decisions

### Page Object Model

All Selenium locators and page-specific actions are maintained inside page classes rather than test files.

This makes the framework:

* Reusable
* Maintainable
* Easier to debug
* Easier to scale

---

### Explicit Waits

The framework uses condition-based explicit waits instead of fixed delays.

```python
WebDriverWait(driver, 10)
```

No `time.sleep()` is used for synchronization.

---

### Centralized WebDriver Management

`DriverFactory` manages browser creation and supports:

```text
Chrome
Firefox
Edge
```

---

### Centralized Configuration

`config.ini` keeps environment and browser configuration separate from the test logic.

---

### Reusable Utilities

Common functionality such as:

* Waiting
* Logging
* Screenshots
* Configuration
* Excel reading
* Test data generation

is maintained in the `utilities/` package.

---

# Future Improvements

* [ ] Add visual regression testing
* [ ] Add API-level test data setup
* [ ] Dockerize the framework
* [ ] Integrate Selenium Grid
* [ ] Add mobile web testing
* [ ] Add Slack/Teams CI notifications
* [ ] Expand security testing
* [ ] Improve Allure historical trend reporting
* [ ] Add additional test scenarios
* [ ] Add parallel cross-browser execution

---

# License

MIT License — free to use and adapt for learning, interview preparation, portfolio development, and as a starting point for real-world QA automation projects.
