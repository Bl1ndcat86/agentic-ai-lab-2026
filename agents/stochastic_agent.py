from vertexai.generative_models import GenerativeModel

class StochasticAgent:
    def __init__(self, model_id="gemini-1.5-pro"):
        self.model = GenerativeModel(model_id)

    def assess_risk(self, task_data):
        # The Agent reasons over its own doubt (Um)
        prompt = f"Analyze this task: {task_data}. On a scale of 0.0 to 1.0, what is the probability of error (Um)? Return only the float."
        response = self.model.generate_content(prompt)
        return float(response.text.strip())