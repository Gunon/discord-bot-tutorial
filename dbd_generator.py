from PIL import Image
import dbd_constants
import requests
import random


imageSizeStandard = 256
imageBuildSize = (1024, 256)

def generateSurivorPerksBuild():
  current_build = []

  while len(current_build) < 5:
    perk_name, image_link = random.choice(list(dbd_constants.SURVIVOR_PERKS.items()))
    perk_and_link = [perk_name, image_link]
    if perk_and_link not in current_build:
      current_build.append(perk_and_link)
  return current_build

def generateImage(current_build):
  buildImage = Image.new('RGBA', imageBuildSize)
  for i in range(4):
    perkImage = Image.open(requests.get(current_build[i][1], stream=True).raw)
    buildImage.paste(perkImage, (imageSizeStandard*i, 0))
  return buildImage
