<!-- PROJECT SHIELDS -->
[![arXiv][arxiv-shield]][arxiv-url]
[![finalpaper][finalpaper-shield]][finalpaper-url]
[![MIT License][license-shield]][license-url]
[![Webpage][webpage-shield]][webpage-url]
[![ReseachGate][researchgate-shield]][researchgate-url]

# Sample Complexity Bounds for Linear System Identification from a Finite Set 
This repository contains the code from our paper "Sample Complexity Bounds for Linear System Identification from a Finite Set" which can be acessed [here](https://ieeexplore.ieee.org/abstract/document/10787218) (Preprint available [here](https://arxiv.org/abs/2409.18010)). 

If you use this project for academic work, please consider citing our publication 

    Chatzikiriakos, N., & Iannelli, A. (2024). 
    Sample complexity bounds for linear system identification from a finite set. 
    IEEE Control Systems Letters.

## Installation
To install all relevant packages execute 
```bash 
pip install -r requirements.txt
```

## Running Experiments
To run Experiment 1 (2, 3) navigate to the src folder and execute 
``` terminal
python main.py --exp=1
```
The experiment will then be run which might take some time. This will create a data folder (if necessary) and safe the results inside.

## Contact
🧑‍💻 Nicolas Chatzikiriakos 

📧 [nicolas.chatzikiriakos@ist.uni-stuttgart.de](mailto:nicolas.chatzikiriakos@ist.uni-stuttgart.de)


[license-shield]: https://img.shields.io/badge/License-MIT-T?style=flat&color=blue
[license-url]: https://github.com/col-tasas/2024-bounds-finite-set-ID/blob/main/LICENSE
[finalpaper-shield]: https://img.shields.io/badge/IEEE-Paper-T?style=flat&color=blue
[finalpaper-url]: https://ieeexplore.ieee.org/abstract/document/10787218
[webpage-shield]: https://img.shields.io/badge/Webpage-Nicolas%20Chatzikiriakos-T?style=flat&logo=codementor&color=green
[webpage-url]: https://nchatzikiriakos.github.io
[arxiv-shield]: https://img.shields.io/badge/arXiv-2409.11141-t?style=flat&logo=arxiv&logoColor=white&color=red
[arxiv-url]: https://arxiv.org/abs/2409.11141
[researchgate-shield]: https://img.shields.io/badge/ResearchGate-Nicolas%20Chatzikiriakos-T?style=flat&logo=researchgate&color=darkgreen
[researchgate-url]: https://www.researchgate.net/profile/Nicolas-Chatzikiriakos
