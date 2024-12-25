from PIL import Image, ImageDraw, ImageFont
import random
from openai import OpenAI
import requests
import os

#client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def add_caption_to_image(image_path, caption, output_path):
    image = Image.open(image_path)

    font = ImageFont.truetype("/Library/Fonts/Arial Unicode.ttf", 20)  # Replace with your font path
    width,height = image.size

    bottom = 100
    top = 10
    right = 10
    left = 10
    new_height = height + bottom + top
    new_width = width + right + left
    res = Image.new(image.mode,(new_width,new_height), (255, 255, 255))
    res.paste(image,(left,top))
    #res.save("Border_Demo.png")

    draw = ImageDraw.Draw(res)
    text_bbox = draw.textbbox((0, 0), caption, font=font)
    text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]

    # Add caption at the bottom
    image_width, image_height = res.size
    x = (image_width - text_width) / 2
    y = image_height - text_height - 10

    draw.text((x, y), caption, font=font, fill="black")

    res.save(output_path)


    """
    draw = ImageDraw.Draw(image)

    draw = ImageDraw.Draw(image)
    text_bbox = draw.textbbox((0, 0), caption, font=font)  # Bounding box of text
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    # Set additional space height
    caption_height = text_height + 20  # Add padding for better spacing
    new_height = image.height + caption_height
    new_width = image.width

    # Create a new image with white background
    new_image = Image.new("RGB", (new_width, new_height), "white")

    # Paste the original image at the top of the new canvas
    new_image.paste(image, (0, 0))

    # Draw the caption onto the new space
    draw = ImageDraw.Draw(new_image)
    text_x = (new_width - text_width) // 2  # Center the text horizontally
    text_y = image.height + 10  # Start text below the original image with padding
    draw.text((text_x, text_y), caption, fill="white", font=font)
    image.save(output_path)
    """




def generate_caption(theme):
    prompt = f"Write a single-panel comic caption in the style of Far Side Galleries. The text should fit the theme but should be succinct, much like how the comic Gary Larson writes his captions. The theme is: {theme}."
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a creative assistant specializing in Far Side-style captions."},
            {"role": "user", "content": prompt}
        ]

    )
    return response.choices[0].message.content

def generate_image(theme):
    response = client.images.generate(
        prompt = f"Generate a far-side gallery style comic that would fit the following caption: {theme}, but do not include the caption itself. Do not include any text in the image, "
                 f"the caption will be added later, and the image should be standalone. The image should be cartoony, and be in black and white. Remember - Far-side gallery-esque. BLACK AND WHITE",
        n = 1,
        size="512x512"  # Image resolution (options: 256x256, 512x512, 1024x1024)
    )
    image_url = response.data[0].url
    return image_url


if __name__ == "__main__":
    #images = load_images("path_to_image_folder")
    #random_image = random.choice(images)

    #Actual code, commented for testing on image
    """
    caption_prompt = input("Enter an idea for a caption, or select random: ")
    caption = generate_caption(caption_prompt)

    image_url = generate_image(caption)
    image_data = requests.get(image_url).content
    gen_path = "generated_comic.png"

    with open(gen_path, "wb") as file:
        file.write(image_data)

    print("Caption: " + caption)
    """




    test_caption = "I see faces in my latte foam, but now I cannot tell my latte apart"
    test_image_path = "generated_comic.png"
    add_caption_to_image(test_image_path, test_caption, "test_output_comic.png")

