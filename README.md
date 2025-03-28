<p align="center">
  <img src="docs/logo.svg" alt="shellsmith" width="50%">
</p>

<p align="center">
  <a href="https://github.com/ptrstn/shellsmith/actions/workflows/test.yaml"><img src="https://github.com/ptrstn/shellsmith/actions/workflows/test.yaml/badge.svg" alt="Test"></a>
  <a href="https://codecov.io/gh/ptrstn/shellsmith"><img src="https://codecov.io/gh/ptrstn/shellsmith/branch/main/graph/badge.svg" alt="codecov"></a>
  <a href="https://pypi.org/project/shellsmith"><img src="https://img.shields.io/pypi/v/shellsmith?color=%2334D058" alt="PyPI - Version"></a>
  <a href="https://github.com/astral-sh/ruff"><img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json" alt="Ruff"></a>
</p>

Shellsmith is a Python toolkit and CLI for managing Asset Administration Shells (AAS), Submodels, and related resources. 
It is designed to interact with [Eclipse BaSyx](https://www.eclipse.org/basyx/), a middleware platform for AAS that follows the [Industry 4.0 standard](https://industrialdigitaltwin.org/en/content-hub/aasspecifications).

### Features

- Python API for CRUD operations on shells, submodels, and submodel elements
- CLI interface for quick scripting
- `.env`-based configuration

## 🚀 Installation

```bash
pip install shellsmith
```

**Requires**: Python 3.10+

## 🔧 Configuration

The default AAS environment host is:

```
http://localhost:8081
```

You can override it by setting the `SHELLSMITH_BASYX_ENV_HOST` environment variable, or by creating a `.env` file in your project root with:

```bash
SHELLSMITH_BASYX_ENV_HOST=http://your-host:1234
```

## 🛠️ Usage

```bash
aas --help
```

Common commands:

```bash
aas info                  # Show all shells and submodels
aas upload <file|folder>  # Upload AAS file or folder

aas shell delete <id>     # Delete a shell
aas submodel delete <id>  # Delete a submodel

aas sme get <id> <path>               # Get Submodel element value
aas sme patch <id> <path> <new_value> # Set Submodel element value
```

Use `--cascade` or `--unlink` to control deletion behavior:

```bash
aas shell delete <id> --cascade      # Also delete referenced submodels
aas submodel delete <id> --unlink    # Remove references from shells
```

## 📡 API Usage

You can also use `shellsmith` as a Python package:

```python
import shellsmith

# Get all available shells
shells = shellsmith.get_shells()

# Get a specific shell by ID (automatically base64-encoded)
shell = shellsmith.get_shell("example_aas_id")

# Disable base64 encoding if your ID is already encoded
submodel = shellsmith.get_submodel("ZXhhbXBsZV9hYXNfaWQ=", encode=False)

# Use a custom AAS environment host
submodel_refs = shellsmith.get_submodel_refs("example_aas_id", host="http://localhost:8081")
```

> ℹ️ `shell_id` and `submodel_id` are automatically base64-encoded unless you set `encode=False`. This is required by the BaSyx API for identifier-based URLs.

The tables below show the mapping between BaSyx AAS REST API endpoints and the implemented client functions.

> 📚 See [Plattform_i40 API reference](https://app.swaggerhub.com/apis/Plattform_i40/Entire-API-Collection) for endpoint details.

### Shells

| Method | BaSyx Endpoint                                               | Shellsmith Function   |
|--------|--------------------------------------------------------------|-----------------------|
| GET    | `/shells`                                                    | `get_shells`          |
| POST   | `/shells`                                                    | `post_shell`          |
| GET    | `/shells/{aasIdentifier}`                                    | `get_shell`           |
| PUT    | `/shells/{aasIdentifier}`                                    | `put_shell`           |
| DELETE | `/shells/{aasIdentifier}`                                    | `delete_shell`        |
| GET    | `/shells/{aasIdentifier}/submodel-refs`                      | `get_submodel_refs`   |
| POST   | `/shells/{aasIdentifier}/submodel-refs`                      | `post_submodel_ref`   |
| DELETE | `/shells/{aasIdentifier}/submodel-refs/{submodelIdentifier}` | `delete_submodel_ref` |

### Submodels

| Method | BaSyx Endpoint                              | Shellsmith Function     |
|--------|---------------------------------------------|-------------------------|
| GET    | `/submodels`                                | `get_submodels`         |
| POST   | `/submodels`                                | `post_submodel`         |
| GET    | `/submodels/{submodelIdentifier}`           | `get_submodel`          |
| PUT    | `/submodels/{submodelIdentifier}`           | `put_submodel`          |
| DELETE | `/submodels/{submodelIdentifier}`           | `delete_submodel`       |
| GET    | `/submodels/{submodelIdentifier}/$value`    | `get_submodel_value`    |
| PATCH  | `/submodels/{submodelIdentifier}/$value`    | `patch_submodel_value`  |
| GET    | `/submodels/{submodelIdentifier}/$metadata` | `get_submodel_metadata` |

### Submodel Elements

| Method | BaSyx Endpoint                                                           | Shellsmith Function            |
|--------|--------------------------------------------------------------------------|--------------------------------|
| GET    | `/submodels/{submodelIdentifier}/submodel-elements`                      | `get_submodel_elements`        |
| POST   | `/submodels/{submodelIdentifier}/submodel-elements`                      | `post_submodel_element`        |
| GET    | `/submodels/{submodelIdentifier}/submodel-elements/{idShortPath}`        | `get_submodel_element`         |
| PUT    | `/submodels/{submodelIdentifier}/submodel-elements/{idShortPath}`        | `put_submodel_element`         |
| POST   | `/submodels/{submodelIdentifier}/submodel-elements/{idShortPath}`        | `post_submodel_element`        |
| DELETE | `/submodels/{submodelIdentifier}/submodel-elements/{idShortPath}`        | `delete_submodel_element`      |
| GET    | `/submodels/{submodelIdentifier}/submodel-elements/{idShortPath}/$value` | `get_submodel_element_value`   |
| PATCH  | `/submodels/{submodelIdentifier}/submodel-elements/{idShortPath}/$value` | `patch_submodel_element_value` |

### Upload

| Method | BaSyx Endpoint | Shellsmith Function                                 |
|--------|----------------|-----------------------------------------------------|
| POST   | `/upload`      | `upload.upload_aas` <br> `upload.upload_aas_folder` |

> ℹ️ Upload functions are available under the `shellsmith.upload` submodule.

## ⚙️ Development

```bash
git clone https://github.com/ptrstn/shellsmith
cd shellsmith
python -m venv .venv
source .venv/bin/activate    # or .venv\Scripts\activate on Windows
pip install -e .[test]
```

### ✅ Testing

Before running the tests, make sure the BaSyx stack is up and running:

```bash
docker compose up -d
```

Then run the test suite with coverage:

```bash
pytest --cov
```

To view a detailed, visual coverage report:

```bash
pytest --cov --cov-report=html
```

Then open `htmlcov/index.html` in your web browser to explore which lines are covered and which are missing.

### 🧼 Code Quality

We use [Ruff](https://docs.astral.sh/ruff/) for linting, formatting, and import sorting.

Check code style:

```bash
ruff check
```

Auto-fix issues:

```bash
ruff check --fix
```

Format code:

```bash
ruff format
```

## Resources

- https://github.com/eclipse-basyx/basyx-java-server-sdk
- https://github.com/admin-shell-io/aas-specs-api
- https://app.swaggerhub.com/apis/Plattform_i40/Entire-API-Collection
