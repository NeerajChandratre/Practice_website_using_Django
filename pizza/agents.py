import google.generativeai as genai
import json
genai.configure(api_key="")

stock =  {
            "Mozzarella_cheese": 450, # cheese starts here
            "Asiago_cheese": 3000,
            "Blue_cheese": 5000,
            "Cheddar_cheese": 6000,
            "Colby_Jack_cheese":5000,
            "Cottage_cheese":2000,
            "Paneer_cheese":3000, #cheese ends here
            "bell_pepper": 120, # vegetables start here
            "capsicum": 150,
            "potato": 200,
            "onion":100,
            "ginger": 20,
            "garlic": 50,
            "corn":100,
            "tomato":300,
            "White_button_mushroom":100,
            "baby_corn":100,
            "green_chilli":100,   # vegetables end here
            "cinnamon":60,     # spices start here,
            "italian_seasoning":30,
            "basil":50,
            "oregano":60,
            "parsley":70,
            "rosemary":80,
            "black_pepper":90,
            "cumin":30,
            "paprika":80  # spices end here       
}

system_instruction = """
    "You are an AI pizza assistant responsible for checking ingredient availability. So rules are: 1. Match ingredients to stock (case-insensitive, fuzzy). 2. Ask the user to clarify if only a category is given. 3. Use the provided stock for all ingredient checks. 
   - If all ingredients are available when compared to stock and if clarification is not needed, output JSON:

    {
      "status": "ok",
      "ingredients": {...},
      "unavailable": [...]
    }

   - If anything is unavilable, output thing which is not available:

    {
      "status": "clarification",
      "message":"We don't have thing which is unavailable, see available stock "
    }

  - If clarification is needed, in message put what clarification you want and give output of it:

    {
      "status": "clarification",
      "message":
    }
    
  - If after THREE clarifications the user is still unclear and if anything is unavailable, output:

    {
      "status": "stop",
      "message": "Unable to determine the ingredients. Please contact customer care."
    }
            
"""
model = genai.GenerativeModel("gemini-2.5-flash",system_instruction=system_instruction,generation_config={"response_mime_type": "application/json"})

chat_history = [
    {
        "role": "user",
        "parts":[f"""Stock items are:
                {json.dumps(stock)}
                 Always base your availability decisions on this stock."""]
    }
]

def ai_choose_ingredents_step(prompt):
    global chat_history
    chat_session = model.start_chat(history=chat_history)
    print('dis part is clear')
    response = chat_session.send_message(prompt)
    chat_history.append({"role":"user","parts":[prompt]})
    chat_history.append({"role":"model","parts":[response.text]})

    ans = response.text

    data = json.loads(ans)

    if data.get("status") == "stop": # end the conversation
        print("\nend conversation")
        print(data["message"])
        chat_history = [
            {
                "role": "user",
                "parts":[f"""Stock items are:
                        {json.dumps(stock)}
                        Always base your availability decisions on this stock."""]
            }
        ]
        return json.loads(response.text)

    if data.get("status") == "ok" and len(data.get("unavailable")) == 0:  # end the conversation
        print("\nFinal selection:")
        chat_history = [
            {
                "role": "user",
                "parts":[f"""Stock items are:
                        {json.dumps(stock)}
                        Always base your availability decisions on this stock."""]
            }
        ]
        print(json.dumps(data, indent=2))
        return json.loads(response.text)
    return json.loads(response.text)

# prompt = "I want pizza with italian seasoning, capsicum, onion and tomato."
# ai_choose_ingredents(prompt)
#res = ai_choose_ingredents(prompt)
# print("ans below")
# print("spices below")
# print(res["spices"])
# print("vegetables below")
# print(res["vegetables"])
# print("cheese below")
# print(res["cheese"])


