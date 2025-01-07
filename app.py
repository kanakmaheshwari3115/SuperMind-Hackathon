import streamlit as st
from transformers import AutoProcessor, BlipForConditionalGeneration, AutoTokenizer
import openai
from itertools import cycle
from PIL import Image
import torch
import os
from dotenv import load_dotenv

processor = AutoProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
tokenizer = AutoTokenizer.from_pretrained("Salesforce/blip-image-captioning-base")
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

load_dotenv()
openai.api_key = os.environ.get('API_KEY')
openai_model = "text-davinci-002"

def caption_generator(des):
    caption_prompt = (
        f"""Please generate three unique and creative captions to use on Instagram for a photo that shows 
        {des}. The captions should be fun and creative.
        Captions:
        1.
        2.
        3.
        """
    )
    response = openai.Completion.create(
        engine=openai_model,
        prompt=caption_prompt,
        max_tokens=175 * 3,
        n=1,
        stop=None,
        temperature=0.7,
    )
    caption = response.choices[0].text.strip().split("\n")
    return caption

def hashtag_generator(des):
    hashtag_prompt = (
        f"""Please generate ten relevant and accurate hashtags that will help the photo 
        reach a larger audience on Instagram and Twitter for a photo that shows {des}. The hashtags
        can be funny and creative. Please also provide them in this format.
        Hashtags:
        #[Hashtag1] #[Hashtag2] #[Hashtag3] #[Hashtag4] #[Hashtag5] #[Hashtag6] #[Hashtag7] #[Hashtag8] #[Hashtag9] #[Hashtag10]
        """
    )
    response = openai.Completion.create(
        engine=openai_model,
        prompt=hashtag_prompt,
        max_tokens=20 * 10,
        n=1,
        stop=None,
        temperature=0.7,
    )
    hashtag = response.choices[0].text.strip().split("\n")
    return hashtag

def prediction(img_list):
    max_length = 30
    num_beams = 4
    gen_kwargs = {"max_length": max_length, "num_beams": num_beams}

    img = []

    for image in img_list:
        i_image = Image.open(image)
        st.image(i_image, width=200)

        if i_image.mode != "RGB":
            i_image = i_image.convert(mode="RGB")

        img.append(i_image)

    pixel_val = processor(images=img, return_tensors="pt").pixel_values
    pixel_val = pixel_val.to(device)

    output = model.generate(pixel_val, **gen_kwargs)
    predict = tokenizer.batch_decode(output, skip_special_tokens=True)
    predict = [pred.strip() for pred in predict]

    return predict

def sample():
    sp_images = {
        'Sample 1': "/Users/manyavalecha/Downloads/Image-Captioning-and-Hashtag-Generator-main/image/beach.png",
        'Sample 2': "/Users/manyavalecha/Downloads/Image-Captioning-and-Hashtag-Generator-main/image/coffee.png",
        'Sample 3': "/Users/manyavalecha/Downloads/Image-Captioning-and-Hashtag-Generator-main/image/footballer.png",
        'Sample 4': "/Users/manyavalecha/Downloads/Image-Captioning-and-Hashtag-Generator-main/image/mountain.jpg"
    }

    colms = cycle(st.columns(3))

    for sp in sp_images.values():
        next(colms).image(sp, width=150)

    for i, sp in enumerate(sp_images.values()):
        if next(colms).button("Generate", key=i):
            description = prediction([sp])
            st.subheader("Description for the Image:")
            st.write(description[0])

            st.subheader("Captions for this image are:")
            captions = caption_generator(description[0])
            for caption in captions:
                st.write(caption)

            st.subheader("#Hashtags")
            hashtags = hashtag_generator(description[0])
            for hash in hashtags:
                st.write(hash)

def upload():
    with st.form("uploader"):
        image = st.file_uploader("Upload Images", accept_multiple_files=True, type=["jpg", "png", "jpeg"])
        submit = st.form_submit_button("Generate")

        if submit and image:
            description = prediction(image)

            st.subheader("Description for the Image:")
            for i, caption in enumerate(description):
                st.write(caption)

            st.subheader("Captions for this image are:")
            captions = caption_generator(description[0])
            for caption in captions:
                st.write(caption)

            st.subheader("#Hashtags")
            hashtags = hashtag_generator(description[0])
            for hash in hashtags:
                st.write(hash)

def main():
    st.set_page_config(page_title="Caption and Hashtag generation")
    st.title("Get Captions and Hashtags for your Image")

    tab1, tab2 = st.tabs(["Upload Image", "Sample"])

    with tab1:
        upload()

    with tab2:
        sample()

if __name__ == '__main__':
    main()
