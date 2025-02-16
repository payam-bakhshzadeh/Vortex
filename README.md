# Vortex Project

## Dependency Visualization

### Using pydeps

1. Install `pydeps`:
    ```sh
    pip install pydeps
    ```

2. Navigate to the project directory and generate the dependency graph:
    ```sh
    cd /e:/Pyton_3_12_8/My_Python_Projects/Vortex
    pydeps .
    ```

### Using pyreverse

1. Install `pylint`:
    ```sh
    pip install pylint
    ```

2. Install Graphviz:
    ```sh
    sudo apt-get install graphviz
    ```
    or on Windows:
    ```sh
    choco install graphviz
    ```

3. Ensure that each directory containing Python modules has an `__init__.py` file:
    ```sh
    touch /e:/Pyton_3_12_8/My_Python_Projects/Vortex/__init__.py
    ```

4. Navigate to the project directory and generate the class diagrams:
    ```sh
    cd /e:/Pyton_3_12_8/My_Python_Projects/Vortex
    pyreverse -o png -p Vortex .
    ```

5. If you encounter the `SKIPPING ILLEGAL MODULE_NAME` error, try using the following command instead:
    ```sh
    pyreverse -o png -p Vortex -m y .
    ```

6. If the `png` format is not supported, try using `dot` or `pdf` format:
    ```sh
    pyreverse -o pdf -p Vortex .
    ```


