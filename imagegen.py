import vertexai
from vertexai.preview.vision_models import ImageGenerationModel
import sys
import logging

logging.basicConfig(level=logging.DEBUG)

# Configure stdout for UTF-8 encoding
sys.stdout.reconfigure(encoding="utf-8")

try:
    logging.debug("Initializing Vertex AI...")
    # Initialize Vertex AI
    vertexai.init(project="gen-lang-client-0812952291", location="us-central1")

    # Retrieve prompt from command-line arguments
    if len(sys.argv) < 2:
        logging.error("Prompt is missing. Exiting.")
        print("[[[IMAGE_GENERATION_ERROR]]]")
        sys.exit(1)

    prompt = sys.argv[1]
    logging.debug(f"Prompt: {prompt}")

    # Generate the images
    model = ImageGenerationModel.from_pretrained("imagen-3.0-fast-generate-001")
    response = model.generate_images(
        prompt=prompt,
        number_of_images=1,
        language="en",
        aspect_ratio="1:1",
        safety_filter_level="block_few",
    )

    # Debugging the response
    logging.debug(f"Generated images response: {response}")

    # Check if the response contains images
    if not response or not response.images:
        logging.error("No images were returned by the model.")
        print("[[[IMAGE_GENERATION_ERROR]]]")
        sys.exit(1)

    # Iterate over the images and print their Base64 strings
    for i, image in enumerate(response.images):
        if hasattr(image, "_as_base64_string"):
            print(image._as_base64_string())
        else:
            logging.warning(f"Image {i + 1} does not have a Base64 string.")

except Exception as e:
    logging.exception("An error occurred:")
    print("[[[IMAGE_GENERATION_ERROR]]]")
    sys.exit(1)
