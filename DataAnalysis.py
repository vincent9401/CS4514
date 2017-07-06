class DataAnalysis:

    def scikit(self):
        # Import `datasets` from `sklearn`
        from sklearn import datasets

        # Load in the `digits` data
        digits = datasets.load_digits()

        # Print the `digits` data
        print(digits)