# QDET App

> A web application analysing the question assurance of exam MCQs

---

## Table of Contents

- [Project Description](#project-description)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)

---

## Project Description

The QDET App is meant to be a web application designed to perform automated quality assurance (QA) on multiple-choice questions (MCQs). The primary focus is to evaluate the relevance and effectiveness of distractors (incorrect answer options) using various metrics, providing educators with data-driven insights into question quality.

---

## Features

- CRUDs for MCQs: Users can upload contexts, questions in regards to the contexts, and different possible answers.
- AI model training: Using the text2props library, users can train a pre-defined AI model on their MCQs, choosing a specific parameter (difficulty, discrimination, facility).
- AI Evaluation: Users can select an existing AI model, and run the evaluation on their own MCQs to obtain a predicted value per MCQ, based on the trained parameter.
- Dashboard: Beautiful and intuitive dashboard meant to display to the users the results of the AI analysis through graphs, tables, and statistical values.

---

## Tech Stack

- Framework: [Django](https://www.djangoproject.com/)
- CSS: [Bootstrap](https://getbootstrap.com/)


## Getting Started


### Prerequisites

Make sure you have the following installed on your system:

- **Python** (>= 3.10 recommended)
- **gcc compiler** (>= 13.3.0 recommended)
- **pip** (Python package manager)
- **virtualenv**
- **Git**

You can verify your Python, GCC and pip installation with:

```bash
python --version
gcc --version
pip --version
```

### Installation

1. Clone the repository:

```bash
git clone https://github.com/xPlume/Cassiopee.git
```

2. Navigate to the project root:
```bash
cd Cassiopee
```

3. Create and activate a virtual environment.
```
python -m venv [VENV_NAME]
source [VENV_NAME]/bin/activate
```


4. Install the Python dependencies:
```bash
pip install -r requirements.txt
```

5. Navigate to the Project directory
```bash
cd Project
```

6. Apply database migrations:
```bash
python manage.py migrate
```

7. Create a superuser to access the Django admin:
```bash
python manage.py createsuperuser
```

8. Start the development server:
```bash
python manage.py runserver
```