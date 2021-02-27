import discord 
import os
import requests
import json
import random
from io import BytesIO
from replit import db
from keep_alive import keep_alive
import dbd_generator

client = discord.Client()

#constants
ENCOURAGEMENTS_NAME = "encouragements"
RESPONDING_NAME = "responding"

sad_words = ["sad","depressed","unhappy","angry","miserable","depressing"]


starter_encouragements = [
  "chale",
  "No se awite compa uwu",
  "unas guamas o que",
  "intenta de nuevo",
  "bienvenido al mundo de las mariguanas"
]

if RESPONDING_NAME not in db.keys():
  db[RESPONDING_NAME] = True



def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

def update_encouragements(encouraging_message):
  if ENCOURAGEMENTS_NAME in db.keys():
    encouragements = db[ENCOURAGEMENTS_NAME]
    encouragements.append(encouraging_message)
    db[ENCOURAGEMENTS_NAME] = encouragements
  else:
    db[ENCOURAGEMENTS_NAME] = [encouraging_message]

def delete_encourragement(index):
  encouragements = db[ENCOURAGEMENTS_NAME]
  if len(encouragements) > index:
    del encouragements[index]
  db[ENCOURAGEMENTS_NAME] = encouragements

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if(message.author == client.user):
    return

  msg = message.content

  if db[RESPONDING_NAME]:
    options = starter_encouragements
    if ENCOURAGEMENTS_NAME in db.keys():
      options = options + db[ENCOURAGEMENTS_NAME]
  
    if any(word in msg for word in sad_words):
      await message.channel.send(random.choice(options))

  if message.content.startswith('$inspire'):
      quote = get_quote()
      await message.channel.send(quote) 

  if msg.startswith("$new"):
    encouraging_message = msg.split("$new ",1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send("New encouraging message added.")
  
  if msg.startswith("$del"):
    encouragements = []
    if ENCOURAGEMENTS_NAME in db.keys():
      index = int(msg.split("$del",1)[1])
      delete_encourragement(index)
      encouragements = db[ENCOURAGEMENTS_NAME]
    await message.channel.send(encouragements)

  if msg.startswith("$list"):
    encouragements = []
    if ENCOURAGEMENTS_NAME in db.keys():
      encouragements = db[ENCOURAGEMENTS_NAME]
    await message.channel.send(encouragements)

  if msg.startswith("$responding"):
    value = msg.split("$responding ", 1)[1]

    if value.lower() == "true":
      db[RESPONDING_NAME] = True
      await message.channel.send("Responding is on.")
    else:
      db[RESPONDING_NAME] = False
      await message.channel.send("Responding is off.")

  if msg.startswith("=perks"):
    survivor_perks = dbd_generator.generateSurivorPerksBuild()
    with BytesIO() as image_binary:
      dbd_generator.generateBuildImage(survivor_perks).save(image_binary, 'PNG')
      image_binary.seek(0)
      await message.channel.send("Here is your Build!: \n- {0} \n- {1} \n- {2} \n- {3}  ".format(survivor_perks[0][0],survivor_perks[1][0],survivor_perks[2][0],survivor_perks[3][0]),file=discord.File(fp=image_binary, filename='image.png'))
    with BytesIO() as second_image_binary:
      dbd_generator.generatePerkImage(survivor_perks[4]).save(second_image_binary, 'PNG')
      second_image_binary.seek(0)
      await message.channel.send("And for the wildcard:\n- {0}  ".format(survivor_perks[4][0]),file=discord.File(fp=second_image_binary, filename='image.png'))


keep_alive()
client.run(os.getenv('DISCORD_TOKEN'))
#print(os.getenv('COD_PASS'))