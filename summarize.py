import google.generativeai as genai
import asyncio
from pyppeteer import launch

import config

async def scrape_reviews(url):
    reviews = []
    browser = await launch({"headless":True,"args":{"--window-size=800,3200"}})
    
    page = await browser.newPage()
    await page.setViewport({"width":800,"height":3200})
    await page.goto(url)
    await page.waitForSelector('.jftiEf')
    elements = await page.querySelectorAll('.jftiEf')
    for element in elements:
        try: 
                await page.waitForSelector(".w8nwRe")
                more_btn = await element.querySelector(".w8nwRe")
                if more_btn is not None:
                    await page.evaluate("button => button.click()",more_btn)
                    await page.waitFor(5000)
        except:
            pass
    
        await page.waitForSelector('.MyEned')
        snippet = await element.querySelector('.MyEned')
        text = await page.evaluate('selected => selected.textContent',snippet)
        reviews.append(text)
            
        
    await browser.close()

    return reviews

def summarize(reviews, model):
    prompt = "I collected some reviews of a place I was considering visiting.  Can you summarize the reviws for me?"
    
    for review in reviews:
        prompt += "\n"+review


    response = model.generate_content(prompt)
    return response.text


genai.configure(api_key=config.API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

url = input("Enter a URL: ")

reviews = asyncio.get_event_loop().run_until_complete(scrape_reviews(url))

response = summarize(reviews, model)
print(response)