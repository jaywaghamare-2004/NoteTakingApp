# Flask Note-Taking Application

This is a simple note-taking application built with Flask and MySQL.

## Prerequisites

* Python 3.x
* MySQL installed and running

## Installation

1.  Clone the repository:

    ```bash
    git clone https://github.com/jaywaghamare-2004/NoteTakingApp
    ```

2.  Navigate to the project directory:

    ```bash
    cd NoteTakingApp
    ```

3.  Create a virtual environment (recommended):

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On macOS/Linux
    venv\Scripts\activate  # On Windows
    ```
4.  Create a MySQL database and update your Flask app with the correct database credentials.

5.  Run the Flask application:

    ```bash
    python notes.py
    ```

6.  Open your web browser and go to `http://127.0.0.1:5000/`.

## Database Setup

* Make sure you have a MySQL database set up.
* Create the `users` and `notes` tables using the SQL queries provided in the `notes.py` file or the documentation.
* Update the database connection details in your Flask app to match your MySQL setup.

## Functionality

* Register and log in.
* Create, view, edit, and delete notes.
* Notes are stored in a MySQL database.
