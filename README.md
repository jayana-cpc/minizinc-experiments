
# Single Constant Multiplication and Integer Division Optimizations in MiniZinc

This repository contains the MiniZinc models and Python scripts related to single constant multiplication optimizations and integer division . This code was written during Intel Preceptorship 2024. Results were gathered on 10000 trials. They were run using the HiGHS 1.6.0 solver. 

- **baseModel.mzn:** Initial SCM Optimization
- **SCM_Expression_Reuse.mzn:** SCM Optimization with Expression Reuse
- **costModel2.mzn:** SCM Optimization weighted by k + 1
- **costModel3.mzn:** SCM Optimization with weighted subtraction by 1.5
- **costModel4.mzn:** SCM Optimization with Powers of 3
- **integerDivision.mzn:** Replication of integer division (RTZ) algorithm in [Correctly Rounded Constant Integer Division via Multiply-Add by Drane and Cheung](https://cas.ee.ic.ac.uk/people/gac1/pubs/TheoISCAS12.pdf) 

## [Presentation](https://docs.google.com/presentation/d/17Wscw-C7pN3tG13d2YIW3b1sMhvV9fXifpy5GlgVhH4/edit?usp=sharing)






