import os


def create_directory_structure():
    root_dir = "FarmManagementApp"
    backend_dir = os.path.join(root_dir, "backend")
    frontend_dir = os.path.join(root_dir, "frontend")

    # Create root directories
    os.makedirs(root_dir, exist_ok=True)
    os.makedirs(backend_dir, exist_ok=True)
    os.makedirs(frontend_dir, exist_ok=True)

    # Create backend directories and files
    backend_structure = {
        "app": {
            "__init__.py": "",
            "main.py": "",
            "models": {
                "__init__.py": "",
                "user.py": "",
                "farm.py": "",
            },
            "routers": {
                "__init__.py": "",
                "user.py": "",
                "farm.py": "",
            },
            "schemas": {
                "__init__.py": "",
                "user.py": "",
                "farm.py": "",
            },
            "services": {
                "__init__.py": "",
                "user_service.py": "",
                "farm_service.py": "",
            },
            "database": {
                "__init__.py": "",
                "database.py": "",
            },
            "config": {
                "__init__.py": "",
                "settings.py": "",
            },
        },
        "tests": {
            "__init__.py": "",
            "test_main.py": "",
            "test_user.py": "",
            "test_farm.py": "",
        },
        "requirements.txt": "",
        ".env": "",
        "README.md": "",
    }

    create_structure(backend_dir, backend_structure)

    # Create frontend directories and files
    frontend_structure = {
        "src": {
            "components": {
                "HomeScreen.js": "",
                "FarmList.js": "",
                "FarmDetail.js": "",
            },
            "screens": {
                "HomeScreen.js": "",
                "FarmListScreen.js": "",
                "FarmDetailScreen.js": "",
            },
            "navigation": {
                "AppNavigator.js": "",
            },
            "services": {
                "api.js": "",
            },
            "styles": {
                "globalStyles.js": "",
            },
            "App.js": "",
            "index.js": "",
        },
        "assets": {
            "images": {},
            "fonts": {},
        },
        "App.js": "",
        "index.js": "",
        "package.json": "",
        ".env": "",
        "README.md": "",
    }

    create_structure(frontend_dir, frontend_structure)

    # Create root files
    with open(os.path.join(root_dir, ".gitignore"), "w") as f:
        f.write(gitignore_content)
    with open(os.path.join(root_dir, "README.md"), "w") as f:
        f.write("")

def create_structure(base_path, structure):
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        if isinstance(content, dict):
            os.makedirs(path, exist_ok=True)
            create_structure(path, content)
        else:
            with open(path, "w") as f:
                f.write(content)

gitignore_content = """
# Ignore Python bytecode files
__pycache__/
*.pyc
*.pyo
*.pyd

# Ignore Python virtual environment
venv/
env/

# Ignore Node.js dependencies
node_modules/

# Ignore React Native packager cache
.expo/
.expo-shared/

# Ignore environment-specific files
.env

# Ignore macOS system files
.DS_Store

# Ignore logs
logs/
*.log

# Ignore database files
*.sqlite3
*.db

# Ignore build artifacts
build/
dist/
*.egg-info/

# Ignore IDE-specific files
.idea/
.vscode/

# Ignore test coverage reports
.coverage
htmlcov/

# Ignore Jupyter notebook checkpoints
.ipynb_checkpoints/

# Ignore FastAPI static files
static/

# Ignore React Native Metro bundler cache
.metro/

# Ignore React Native cache files
.cache/

# Ignore React Native bundle files
*.bundle
"""

if __name__ == "__main__":
    create_directory_structure()
