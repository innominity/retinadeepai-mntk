class AnalysisResult:

    def __init__(self, label: str, score: float) -> None:
        self.label = label
        self.score = score
        self.percentage = "{:.2f}".format(score * 100)
