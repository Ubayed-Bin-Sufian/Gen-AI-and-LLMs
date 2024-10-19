#!/usr/bin/env python
# coding: utf-8

# In[ ]:


responses = {
    "hi": "Hello! Welcome to TechGadget Support. How can I assist you today?",
    "do you have smartwatches": "Yes, we have a variety of smartwatches. You can check them out on our products page.",
    "shipping time": "Shipping usually takes 3-5 business days.",
    "shipping methods": "We offer standard, expedited, and overnight shipping.",
    "return policy": "You can return products within 30 days of receipt for a full refund.",
    "how to return": "To return a product, please visit our returns page for a step-by-step guide.",
    "won’t turn on": "Make sure your gadget is charged. If it still won’t turn on, you can visit our troubleshooting page.",
    "reset device": "To reset your device, hold down the power button for 10 seconds. If that doesn't work, please check the manual for a factory reset.",
    "cancel order": "You can cancel your order by visiting the order history page and selecting 'Cancel Order'.",
    "track order": "You can track your order on our tracking page by entering your order number.",
    "product warranty": "Our products come with a 1-year warranty. Please refer to our warranty page for more details.",
    "exchange policy": "We offer exchanges within 30 days of purchase. Please visit our exchanges page for more information.",
    "payment methods": "We accept credit cards, debit cards, PayPal, and bank transfers.",
    "store hours": "Our stores are open from 9 AM to 9 PM, Monday to Saturday.",
    "contact": "You can reach us at support@techgadget.com or call us at 1-800-123-4567.",
    "bye": "Thank you for visiting TechGadget. If you have more questions, feel free to ask. Goodbye!"
}

def get_bot_response(user_input):
    user_input = user_input.lower()
    understood = False

    for keyword, response in responses.items():
        if keyword in user_input:
            understood = True
            return response

    return None if not understood else "I'm not sure how to respond to that. Can you try asking something else?"

# Keep track of failed responses
failed_attempts = 0

while True:
    user_input = input("You: ")
    
    if user_input.lower() in ["quit", "exit", "bye"]:
        print("Bot: Goodbye! If you have any more questions, we're here to help.")
        break
    
    response = get_bot_response(user_input)
    
    if response:
        print(f"Bot: {response}")
        failed_attempts = 0  # reset failed attempts if response is understood
    else:
        failed_attempts += 1
        if failed_attempts >= 3:
            print("Bot: I'm having trouble understanding. Let me connect you to a customer service representative.")
            break
        else:
            print("Bot: I'm not sure how to respond to that. Can you try asking something else?")


# In[ ]:




