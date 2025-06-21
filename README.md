# Alx_DjangoLearnLab-1-new

This repository serves as a comprehensive learning lab for Django, created as part of my ALX Software Engineering program. It documents my practical journey and application of Django concepts, from foundational principles to more advanced topics like building REST APIs.

## Table of Contents

- [About The Project](#about-the-project)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [Contact](#contact)
- [Acknowledgements](#acknowledgements)

## About The Project

This repository is a collection of various Django sub-projects, exercises, and code examples. Each section or sub-directory within this lab is designed to explore and demonstrate specific aspects of Django web development.

My goal with this repository is to:
* Provide a structured and organized environment for my Django learning journey.
* Implement and practice core Django concepts, including models, views, URLs, and templates.
* Explore advanced topics such as REST API development using Django REST Framework.
* Document my solutions and thought processes for future reference and sharing.


## Getting Started

To get a local copy of this learning lab up and running on your machine, follow these simple steps.

### Prerequisites

* **Python 3.x:** Ensure you have Python 3.8 or a newer version installed.
* **pip:** Python's package installer, which usually comes bundled with Python.
* **venv:** Python's standard library module for creating virtual environments.

### Installation

1.  **Clone the repository:**
    If you haven't already, clone this repository to your local machine:
    ```bash
    git clone [https://github.com/EMIO24/Alx_DjangoLearnLab-1-new.git](https://github.com/EMIO24/Alx_DjangoLearnLab-1-new.git)
    cd Alx_DjangoLearnLab-1-new
    ```


2.  **Create and activate a virtual environment:**
    A virtual environment is highly recommended to manage project dependencies without affecting your system-wide Python installation.
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    # On Windows (Command Prompt): .\venv\Scripts\activate
    # On Windows (PowerShell): .\venv\Scripts\Activate.ps1
    ```

3.  **Install dependencies:**
    With your virtual environment activated, install all the necessary Python packages listed in `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Database Setup (for Django projects):**
    For each Django project within this lab that utilizes a database (like `api_project`), you'll need to apply database migrations.

    ```bash
    # Example for api_project:
    cd api_project/
    python3 manage.py migrate
    # If you need to access the Django admin interface, create a superuser:
    # python3 manage.py createsuperuser
    cd .. 
    ```
    *(Repeat the `cd project_name/` and `python3 manage.py migrate` steps for any other Django projects you have that require database initialization.)*

## Usage

Each sub-directory in this repository contains a separate Django project or a focused set of learning files. To run or interact with a specific Django project (e.g., `api_project`):

1.  **Activate your virtual environment** if it's not already active (you should see `(venv)` in your terminal prompt). If not, navigate to the `Alx_DjangoLearnLab-1-new` root and run `source venv/bin/activate`.
2.  **Navigate into the specific project's directory:**
    ```bash
    cd api_project/
    ```
3.  **Start the Django development server:**
    ```bash
    python3 manage.py runserver
    ```
    The server will typically become accessible at `http://127.0.0.1:8000/`. You can then open this URL in your web browser to interact with the project.

## Contributing

This repository is primarily a personal learning space and journal. Therefore, direct contributions in the form of pull requests are not generally expected. However, any constructive feedback, suggestions for improvements, or bug reports are welcome. Please feel free to [open an issue](https://github.com/EMIO24/Alx_DjangoLearnLab-1-new/issues) on this repository.


## Contact

Emmanuel Osarodion - emmanuelosarodion

Project Link: [https://github.com/EMIO24/Alx_DjangoLearnLab-1-new]
## Acknowledgements

* **ALX Software Engineering Program:** For providing the structured learning path and challenges.
* **Django Documentation:** An invaluable resource for all things Django.
* **Django REST Framework Documentation:** Essential for building robust APIs.
