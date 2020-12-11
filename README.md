# KDD-HigherEduBR

[![Build Status](https://travis-ci.com/renan-cunha/KDD-HigherEduBR.svg?token=HVUZn2CgFZmexfaxxwwt&branch=master)](https://travis-ci.com/renan-cunha/KDD-HigherEduBR) [![codecov](https://codecov.io/gh/renan-cunha/KDD-HigherEduBR/branch/master/graph/badge.svg?token=WZZTE0Y1A6)](https://codecov.io/gh/renan-cunha/KDD-HigherEduBR)


Data Mining in Brazilian Higher Education

### Prerequisities

* Python 3.6.9+
* Linux

Install required packages by:

```bash
pip install -r requirements.txt
```

### Usage

#### Get the data

```bash
cd data/
bash get_data.sh
```

#### View/Run the analysis

```
jupyter notebook main.ipynb
```

#### Running the Tests

```bash
pytest-3 tests/
```

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/renan-cunha/KDD-HigherEduBR/blob/master/LICENSE) file 
for details.
