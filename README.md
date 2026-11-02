# Restaurant QR Ordering API

## Development

Install the application and development dependencies:

```shell
python -m pip install -r requirements-dev.txt
```

Run the API tests and generate the coverage report:

```shell
pytest
```

Run code-quality checks:

```shell
black --check app tests
isort --check-only app tests
ruff check app tests
mypy app
```

## Docker

Build and run the API image:

```shell
docker build -t restaurant-qr-ordering-api .
docker run --rm -p 8000:8000 restaurant-qr-ordering-api
```

Configure MongoDB with `MONGO_URI` and `MONGO_DATABASE` environment variables
when running the container. Do not copy a local `.env` file into the image.

## CI and security scans

The GitHub Actions workflow runs formatting, lint, type, dependency/source
security, test coverage, SonarQube, and Docker image checks. The SonarQube scan
is enabled by adding `SONAR_TOKEN` as a repository secret and `SONAR_HOST_URL`
as a repository variable. For SonarQube Cloud, also set the
`sonar.organization` property in `sonar-project.properties` to your
organization key.

SonarQube and Trivy initially report findings without failing CI so existing
issues can be reviewed and fixed before these scanners become blocking gates.
After the baseline is clean, enable SonarQube quality-gate waiting with
`-Dsonar.qualitygate.wait=true` and set both Trivy actions' `exit-code` to `"1"`
to enforce their findings.
