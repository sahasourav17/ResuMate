# ResuMate

AI-powered resume screening app using Streamlit, OpenAI, and LlamaIndex. Automate candidate evaluation and boost hiring efficiency.

## Features:
- Generates Criteria Decisions and reasoing based on job descriptions and selection criteria
- Fact Checking (Though it need to be improved and suggestions are welcome)
- Resume Rating (scale of 10)

![ResuMate Homepage](./images//resumate_home.png)

## Guidelines to follow

For now, please separate your requirements by `\n`.<br>
Example:

```
{requirement 1}\n
{requirement 2}\n
{requirement 3}\n
```

Installation Instructions:

1. Clone this repo
2. Create a `.env` file in the root directory and configure `OPENAI_API_KEY`.
3. Create a virtual environment
4. `pip install -r requirements.txt`
5. After successful installation, run `streamlit run main.py`

If you have docker installed on your system then Skip step 3,4 and 5 and  run `docker-compose up`
