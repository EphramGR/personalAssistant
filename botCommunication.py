import openai

name = "Jolene"

personalitySettings = {"texan": f"You're a personal assistant named is {name}. Your personality is sassy and outgoing, and you use texan slang. ",
						"pirate": f"You're a pirate named is {name}. Your personality is rebellious and unconventional, and you use pirate slang. ",
						}

openai.api_key = 'insert your key here'
model_id = 'gpt-3.5-turbo'

goal = "You will respond in 1-2 sentences, as if we are having a conversation."
personality = personalitySettings["texan"] + goal



conversation = []

def ChatGPT_conversation(conversation):
    while True:
        try:
            response = openai.ChatCompletion.create(
                model=model_id,
                messages=conversation
            )
            break
        except:
            print("oops")
    # api_usage = response['usage']
    # print('Total token consumed: {0}'.format(api_usage['total_tokens']))
    # stop means complete
    # print(response['choices'][0].finish_reason)
    # print(response['choices'][0].index)
    conversation.append({'role': response.choices[0].message.role, 'content': response.choices[0].message.content})
    return conversation


#roles: system (starts new session), user (me), assistant
def initializeCoversation():
	global conversation
	conversation = []
	conversation.append({'role': 'system', 'content': personality})
	conversation = ChatGPT_conversation(conversation)
	#print('{0}: {1}\n'.format(conversation[-1]['role'].strip(), conversation[-1]['content'].strip()))
	return (conversation[-1]['content'].strip())

def sendMessage(prompt):
	global conversation
	conversation.append({'role': 'user', 'content': prompt})
	conversation = ChatGPT_conversation(conversation)
	#print('{0}: {1}\n'.format(conversation[-1]['role'].strip(), conversation[-1]['content'].strip()))
	return (conversation[-1]['content'].strip())


def setName(newName):
    global name, personalitySettings, personality
    
    for key in personalitySettings:
    	personalitySettings[key] = personalitySettings[key].replace(name, newName)

    personality = personality.replace(name, newName)

    name = newName

    

def setPersonality(title):
	global personality
	personality = personalitySettings[title] + goal