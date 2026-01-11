# Contributing Guidelines

## Development Workflow

### 1. Fork and Clone
```bash
git clone <your-fork-url>
cd BRFSS-Dashboard
```

### 2. Create Feature Branch
```bash
git checkout -b feature/your-feature-name
```

### 3. Make Changes
- Follow PEP 8 style guide
- Add docstrings to functions
- Update tests if applicable
- Update documentation

### 4. Commit Changes
```bash
git add .
git commit -m "Description of changes"
```

### 5. Push and Create Pull Request
```bash
git push origin feature/your-feature-name
```

## Code Style

- Use type hints where appropriate
- Maximum line length: 100 characters
- Use descriptive variable names
- Comment complex logic

## Testing

- Add unit tests for new features
- Ensure all tests pass before submitting PR
- Test with sample data before using full dataset

## Documentation

- Update README.md if adding features
- Add docstrings to new functions
- Update API documentation if needed

