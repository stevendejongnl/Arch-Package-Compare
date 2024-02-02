# arch-package-compare

## Overview
arch-package-compare is a Python script designed for Arch Linux users to compare installed packages between the official repository and the Arch User Repository (AUR). It helps users track changes in their package installations by identifying newly installed packages and removed packages since the last comparison.

## Features
- Compares installed packages between Arch Linux's official repository and the AUR.
- Identifies newly installed packages and removed packages since the last comparison.
- Provides a clear summary of package changes.

## Installation
1. Clone this repository to your local machine:

```bash
git clone git@github.com:stevendejongnl/arch-package-compare.git
```

2. Navigate to the cloned directory:
```bash
cd arch-package-compare
```

## Usage
1. Run the script to compare installed packages:

```bash
python main.py
```

2. The script will display newly installed packages and removed packages since the last comparison.

## Requirements
- Python 3.x
- Arch Linux (pacman and AUR utilities must be installed)

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
