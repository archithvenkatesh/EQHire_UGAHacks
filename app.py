from flask import Flask, render_template, redirect, url_for, request, session
import openai
import requests, json
from serpapi import GoogleSearch

app = Flask(__name__)

openai.api_key = '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'


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/output")
def output():
    return render_template("output.html")

@app.route("/form", methods=["POST", "GET"])
def form():
    if request.method == "POST":
        minority = request.form.get("identification_drop")
        job = request.form.get("job_drop")
        prompt = "I am looking to work as a " + job + ". Find and describe a program from 5 companies tailored towards" + minority + " employees. In the last line of your output list the names of the companies seperated by ^"
        

        response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        
        ],
        temperature = 0.2
    )

        generated_text = response['choices'][0]['message']['content']
        
        companies = [] 
        companyString = ""
        chatGPTCompanies = generated_text 

        # Puts company names into an array
        count = len(chatGPTCompanies)
        while (len(companies) <= 5):
            count -= 1

            if (chatGPTCompanies[count] == ": " or chatGPTCompanies[count] == "\n"):
                companyString = companyString[::-1]
                companies.append(companyString)
                companyString = ""
                count -= 1
                break

            if chatGPTCompanies[count] == "^":
                companyString = companyString[::-1]
                companies.append(companyString)
                companyString = ""
                count -= 1
            companyString += chatGPTCompanies[count]
                

        bigLinks = []
        # API 2
        # Google Search API call
        for i in range(len(companies)):
            params = {
                "engine": "google",
                "q": companies[i] + " Company " + job + " Jobs",
                "api_key": "c1c52d0669b8527cd13124496f1ceaf7063267f4a2405c0e9760bb3f744b34c2",
                "num": 3
            }

            search = GoogleSearch(params)
            results = search.get_dict()
            organic_results = results["organic_results"]


            links = []
            for item in organic_results:
                link = item.get("link")
                if link:
                    links.append(link)

            # Append all the links
            for link in links:
                bigLinks.append(link)



        
        
        return render_template("output.html", generated_text=generated_text, bigLinks=bigLinks)


    return render_template("form.html")


if __name__ == "__main__":
    app.run(debug=True)

