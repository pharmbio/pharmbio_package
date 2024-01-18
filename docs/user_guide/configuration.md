# Configuration

After successfully installing `pharmbio`, the next essential step is configuring your environment to ensure seamless interaction with the necessary resources. Before using the package, it's imperative to set the database URI as an environment variable. This configuration is crucial as the package requires a connection to the image database. The proper setup of the database URI ensures that your instance of `pharmbio` is connected to the correct server, allowing you to fully utilize its features and functionalities.

## Setting the Database URI Environment Variable

You have two options for setting the database URI as an environment variable:

**Using Jupyter Notebook's %env Magic Command**

If you are using Jupyter Notebook, you can use the `%env` magic command to set environment variables within your notebook:

```python
%env DB_URI=your_database_uri_here
```

!!! Info No Quotation

    Note that in this method you must avoid quotation and use the URI without putting it in ' or "!

**Using Python's `os` Library**

Alternatively, you can use Python's built-in `os` library to set the environment variable in your script or notebook:

```python
import os
os.environ["DB_URI"] = "your_database_uri_here"
```

!!! Info "DB_URI"

    For security reasons, the actual URI is not disclosed in this documentation. You will need to replace `your_database_uri_here` with the actual URI that you should have received from system administrator or through internal protocols.


## Setting Environment Variables in the Operating System

Another method to set the database URI environment variable for [Your Package Name] is by directly configuring it in your operating system. This approach is particularly useful when you want the environment variable to be globally accessible across various applications and scripts, or when you prefer not to include environment-specific code in your Python scripts or Jupyter Notebooks.


### For Windows:

1. **Using System Properties:**
      - Open the Start Search, type "Environment Variables" and select "Edit the system environment variables."
      - In the System Properties window, click on "Environment Variables."
      - Under "User variables" or "System variables," click "New" to create a new environment variable.
      - Enter `DB_URI` as the variable name and your database URI in the variable value field.
      - Click OK to save the changes. You might need to restart your system or the command prompt to apply these changes.

2. **Using Command Line with `setx` Command:**
      - Open Command Prompt and use the `setx` command:
        ```
        setx DB_URI "your_database_uri_here"
        ```
      - This command sets the `DB_URI` environment variable to your database URI. The changes will apply from the next session of the Command Prompt.

### For Unix/Linux:

- **Using Shell Configuration Files:**
      - Edit your shell configuration file (like `.bashrc`, `.bash_profile`, `.profile`, or `.zshrc` for macOS) in your home directory.
      - Add the following line at the end of the file:
        ```
        export DB_URI="your_database_uri_here"
        ```
      - Save the file and source it to apply the changes immediately:
        ```
        source ~/.bashrc
        ```
      - These changes will be applied the next time you log in.


!!! Info "Advantages of Setting Environment Variables in the OS"

    - **Global Access:** Variables set in this way are accessible by all Python scripts and applications running under your user account, providing a consistent environment across your work.
    - **Security:** Keeping sensitive information like database URIs out of your source code enhances security, especially when your code is shared or stored in version control systems.
    - **Flexibility:** This method allows for different configurations across various environments (development, testing, production) by simply changing the environment variables in each respective system.

!!! Warning "Important Considerations"

    - **Privacy and Security:** Be cautious about setting sensitive data as global environment variables, especially on shared or public machines.
    - **Session Persistence:** For Unix/Linux, changes made in shell configuration files are persistent across sessions. In contrast, using `setx` in Windows or setting variables in a terminal session (without editing configuration files) typically affects only the current session or new sessions, respectively.
    - **System Access:** Modifying system-level environment variables may require administrative privileges.

By setting the `DB_URI` environment variable directly in the operating system, you create a stable and secure configuration foundation for `pharmbio`, ensuring it operates seamlessly with the necessary database connections across different execution environments.

## Choose the right server as your workspace

`Pharmbio`'s infrastructure comprises multiple servers, each serving different purposes. It is vital to ensure that your workspace is located on the correct server to access the necessary file repositories. This is especially crucial for retrieving cell painting data, which is essential for `Pharmbio`'s functionality.

!!! warning "Is Your Workspace on the Correct Server for Accessing File Repositories?"

     The package relies on specific directories that may only be available on certain servers. If you are uncertain about whether your workspace is on the appropriate server, or if you find that you do not have access to the required data, please contact server administrators. They can assist in relocating your workspace to the correct server or provide the necessary access rights, ensuring that you can work effectively with `Pharmbio`.