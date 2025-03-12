import gradio as gr
import openai
import os

# Load OpenAI API key securely from environment variables
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("⚠️ OpenAI API key is missing! Please set it in Hugging Face Secrets.")

# Initialize OpenAI client (New API format)
client = openai.OpenAI(api_key=api_key)

# Set fine-tuned model ID (Replace with your actual model ID)
fine_tuned_model_id = "ft:gpt-3.5-turbo-0125:viddies::BADHydp0"

# Function to generate satirical headlines
def generate_satirical_headline(real_headline, temperature=0.7):
    try:
        response = client.chat.completions.create(
            model=fine_tuned_model_id,
            messages=[
                {"role": "system", "content": "You are an AI that rewrites news headlines in a satirical, humorous style similar to The Onion."},
                {"role": "user", "content": f"Real headline: {real_headline}"}
            ],
            temperature=temperature,
            top_p=0.8,
            max_tokens=50
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

# Create Gradio interface
iface = gr.Interface(
    fn=generate_satirical_headline,
    inputs=[
        gr.Textbox(label="Enter a Real News Headline"),
        gr.Slider(0.2, 1.2, value=0.7, step=0.1, label="Creativity (Temperature)")
    ],
    outputs="text",
    title="📰 Satirical Headline Generator",
    description="Enter a real news headline and get a satirical version inspired by The Onion!"
)

# Launch the Gradio app
iface.launch()

