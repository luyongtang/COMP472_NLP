## Team: By the way (Yongtang Lu, 40010468 & Manpreet Singh, 27517378)
URL: https://github.com/luyongtang/comp472_NLP

Instructions to run from computer lab using Anaconda command line:

  1. Install the necessary packages: `conda install --file requirements.txt `
  2. For the required model, please run `required_model.py` app with providing 3 necessary arguments: `python required_model.py <Vocabulary (V)> <Size of n-grams (n)> <Smoothing value (δ)>`
     
     Example: `python required_model.py 2 2 0.3`
  3. For the own model, please run `byom.py` app with providing 3 necessary arguments: `python byom.py <Vocabulary (V)> <Penalty weight (P)> <Smoothing value (δ)>`
     
     Example: `python byom.py 2 10 0.5`
