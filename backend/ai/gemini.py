import google.generativeai as genai
import os
import dotenv
import json

# Load environment variables from .env file
dotenv.load_dotenv()


def generate_ai_content(prompt: str):
    # Retrieve the API key from the environment variable
    api_key = os.getenv("GEMINI_API")
    if not api_key:
        raise ValueError("GEMINI_API environment variable is not set.")

    # Configure the API with the provided key
    genai.configure(api_key=api_key)

    # Instantiate the model (ensure "gemini-1.5-flash" is valid)
    model = genai.GenerativeModel("gemini-1.5-flash")

    # Prepare the prompt to request 10 slides in JSON format
    slide_prompt = f"""
    You are a helpful, intelligent assistant. You are experienced with PowerPoint.

    Create the slides for a presentation on the given topic.
    Include main headings for each slide, detailed bullet points for each slide.
    Add relevant, detailed content to each slide. When relevant, add one or two EXAMPLES to illustrate the concept.
    For two or three important slides, generate the key message that those slides convey.

    Identify if a slide describes a step-by-step/sequential process, then begin the bullet points with a special marker >>.
    Limit this to max two or three slides.

    Also, add at least one slide with a double column layout by generating appropriate content based on the description in the JSON schema provided below.
    In addition, for each slide, add image keywords based on the content of the respective slides.
    These keywords will be later used to search for images from the Web relevant to the slide content.

    In addition, create one slide containing 4 TO 6 icons (pictograms) illustrating some key ideas/aspects/concepts relevant to the topic.
    In this slide, each line of text will begin with the name of a relevant icon enclosed between [[ and ]], e.g., [[machine-learning]] and [[fairness]].
    Insert icons only in this slide.

    Your output, i.e., the content of each slide should be VERBOSE, DESCRIPTIVE, and very DETAILED.
    Each bullet point should be detailed and explanatory, not just short phrases.

    ALWAYS add a concluding slide at the end, containing a list of the key takeaways and an optional call-to-action if relevant to the context.
    Unless explicitly instructed with the topic, create 10 TO 12 SLIDES in total. You must never create more than 15 slides.

    ### Topic:
    {prompt}

    The output must be only a valid and syntactically correct JSON adhering to the following schema:
    {{
        "title": "Presentation Title",
        "slides": [
            {{
                "heading": "Heading for the First Slide",
                "bullet_points": [
                    "First bullet point",
                    [
                        "Sub-bullet point 1",
                        "Sub-bullet point 2"
                    ],
                    "Second bullet point"
                ],
                "key_message": "",
                "img_keywords": "a few keywords"
            }},
            {{
                "heading": "Heading for the Second Slide",
                "bullet_points": [
                    "First bullet point",
                    "Second bullet item",
                    "Third bullet point"
                ],
                "key_message": "The key message conveyed in this slide",
                "img_keywords": "some keywords for this slide"
            }},
            {{
                "heading": "A slide illustrating key ideas/aspects/concepts (Hint: generate an appropriate heading)",
                "bullet_points": [
                    "[[icon name]] Some text",
                    "[[another icon name]] Some words describing this aspect",
                    "[[icon]] Another aspect highlighted here",
                    "[[an icon]] Another point here"
                ],
                "key_message": "",
                "img_keywords": ""
            }},
            {{
                "heading": "A slide that describes a step-by-step/sequential process",
                "bullet_points": [
                    ">> The first step of the process (begins with special marker >>)",
                    ">> A second step (begins with >>)",
                    ">> Third step"
                ],
                "key_message": "",
                "img_keywords": ""
            }},
            {{
                "heading": "A slide with a double column layout (useful for side-by-side comparison/contrasting of two related concepts, e.g., pros & cons, advantages & risks, old approach vs. modern approach, and so on)",
                "bullet_points": [
                    {{
                        "heading": "Heading of the left column",
                        "bullet_points": [
                            "First bullet point",
                            "Second bullet item",
                            "Third bullet point"
                        ]
                    }},
                    {{
                        "heading": "Heading of the right column",
                        "bullet_points": [
                            "First bullet point",
                            "Second bullet item",
                            "Third bullet point"
                        ]
                    }}
                ],
                "key_message": "",
                "img_keywords": ""
            }}
        ]
    }}

    ### Output:
    ```json
    """

    try:
        # Send the slide generation request to the model
        response = model.generate_content(slide_prompt)

        # Check if the response contains text
        if response and hasattr(response, "text"):
            content = response.text
            content = content.replace("```json", "").replace("```", "").strip()
            return content
        else:
            return "Error: No content generated."

    except Exception as e:
        # Return the error message in case of any issues
        return f"Error during API request: {e}"
