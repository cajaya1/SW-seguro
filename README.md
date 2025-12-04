# Security Vulnerability Scanner

An AI-powered tool for detecting security vulnerabilities in source code using machine learning techniques.

## Overview

This project implements a machine learning-based vulnerability scanner that analyzes source code files and predicts the likelihood of security vulnerabilities. The system uses static code analysis combined with machine learning to identify potentially dangerous code patterns.

## Features

- **AI-powered Analysis**: Uses Random Forest classifier to predict vulnerability probability
- **Multi-language Support**: Supports Python, JavaScript, TypeScript, and Java files
- **Static Code Analysis**: Leverages Lizard for complexity metrics and pattern matching
- **Local Scanning**: Performs analysis on local files without sending code to external servers
- **Training Pipeline**: Complete pipeline for training models on vulnerability datasets
- **Data Mining**: Tools for mining vulnerability data from Git repositories

## Project Structure

```
├── demo_scanner.py      # Interactive vulnerability scanner
├── entrenamiento.py     # Model training pipeline
├── mineria.py          # Data mining from repositories
├── seguro.py           # Example of secure coding practices
├── vulnerable.py       # Example of vulnerable code patterns
├── dataset_local.csv   # Training dataset (gitignored due to size)
├── repos_descargados/  # Cloned repositories for analysis
└── modelo_seguridad_final.pkl  # Trained model file
```

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd lab1p2v2
```

2. Install required dependencies:
```bash
pip install pandas numpy scikit-learn joblib matplotlib seaborn tqdm lizard pydriller flask
```

## Usage

### Quick Start - Vulnerability Scanner

Run the interactive scanner to analyze individual files:

```bash
python demo_scanner.py
```

Enter the path to a source code file when prompted. The scanner will output:
- Risk status (SECURE/HIGH RISK)
- Vulnerability probability percentage
- Detailed metrics

### Training a New Model

To train a new model with your own dataset:

```bash
python entrenamiento.py
```

This will:
1. Load the dataset from `dataset_local.csv`
2. Extract features using static analysis
3. Train a Random Forest classifier
4. Save the model as `modelo_seguridad_final.pkl`
5. Generate performance metrics and confusion matrix

### Mining Vulnerability Data

To collect training data from open source repositories:

```bash
python mineria.py
```

This will:
- Clone specified repositories
- Analyze commit messages for security-related keywords
- Extract before/after code samples from security fixes
- Generate labeled dataset for training

## Model Features

The scanner analyzes the following code characteristics:

- **Lines of Code (NLOC)**: Number of non-comment lines
- **Cyclomatic Complexity**: Code complexity metrics
- **Risk Keywords**: Presence of potentially dangerous functions
- **Code Content**: TF-IDF vectorization of source code

### Risk Patterns Detected

- **Python**: `eval()`, `exec()`, `subprocess`, `os.system`, SQL execution
- **JavaScript**: `eval()`, `innerHTML`, `document.write`, `dangerouslySetInnerHTML`
- **Java**: Dynamic SQL statements, `Runtime.exec()`, parameter concatenation

## Examples

### Secure vs Vulnerable Code

The project includes example files demonstrating:

- **seguro.py**: Secure coding practices (parameterized queries, input validation, etc.)
- **vulnerable.py**: Common vulnerability patterns (SQL injection, command injection, etc.)

## Performance

The trained model achieves:
- **Accuracy**: Varies by dataset (typically 85%+ on balanced datasets)
- **Risk Threshold**: 40% probability threshold for HIGH RISK classification
- **Processing Speed**: Analyzes files in milliseconds after model loading

## Security Considerations

- All analysis is performed locally
- No code is transmitted to external services
- Model predictions are probabilistic and should be verified manually
- Tool is designed for educational and security testing purposes

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is for educational purposes. Please ensure compliance with relevant security testing regulations in your jurisdiction.

## Limitations

- Static analysis cannot detect all vulnerability types
- Machine learning predictions may have false positives/negatives
- Requires pre-trained model for operation
- Limited to supported programming languages

## Future Enhancements

- Support for additional programming languages
- Integration with CI/CD pipelines
- Real-time code analysis in IDEs
- Enhanced deep learning models
- API endpoint for remote analysis

## Troubleshooting

### Common Issues

1. **Model file not found**: Run `entrenamiento.py` to train a new model
2. **Missing dependencies**: Install required packages using pip
3. **Dataset too large**: Use sampling in training script
4. **Memory issues**: Reduce `SAMPLE_SIZE` in configuration

### Performance Tips

- Use SSD storage for large datasets
- Increase RAM for processing large repositories
- Use multi-core systems for faster training
- Cache cloned repositories for repeated mining

## Contact

For questions or support, please open an issue in the repository.