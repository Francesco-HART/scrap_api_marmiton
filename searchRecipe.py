import re

import requests
from bs4 import BeautifulSoup
from bleach import clean


class marmiScrap:
    def __init__(self):
        pass

    def getRecipe(self, nb_recipe):
        i = 1
        globalSoup = []
        while True:
            url = "https://www.marmiton.org/recettes/?page=" + str(i)
            res = requests.get(url)
            if res.status_code != 200:
                break
            soupInit = BeautifulSoup(res.text, 'html.parser')
            soup = soupInit.select('.recipe-card')
            link = soupInit.select("a", {"class": "recipe-card-link"})
            soup = str(soup)
            print('link',str(link))
            soup = soup.split("<div class=\"recipe-card\">")
            soup.pop(0)
            for i in range(len(soup) - 1):
                if(len(globalSoup) <  nb_recipe):
                    globalSoup.append(soup[i])
                else:
                    return globalSoup
        return globalSoup

    def getRecipeLink(self, nb_recipe):
        i = 2
        globalLink = []
        while True:
            url = "https://www.marmiton.org/recettes/?page=" + str(i)
            print(url)
            res = requests.get(url)
            if res.status_code != 200:
                break
            soupInit = BeautifulSoup(res.text, 'html.parser')
            for a in soupInit.find_all("a", {"class": "recipe-card-link" }):
                if (len(globalLink) < nb_recipe):
                    globalLink.append(a['href'])
                else:
                    return globalLink
            i += 1
        return globalLink



    def structurRecipe(self, recipes):
        allRecipes = []
        for i in recipes:
            try:
                url = i
                res = requests.get(url)
                if res.status_code != 200:
                    break
                soupInit = BeautifulSoup(res.text, 'html.parser')
                img = soupInit.find("img", {"class": "recipe-media-viewer-picture"})['src']
                title =  soupInit.find("h1", {"class" : "main-title" }).text
                nbPeople = soupInit.find("div", {"class" : "recipe-infos__quantity" }).text
                nbPeople = int(''.join(list(filter(str.isdigit, nbPeople))))
                ingredients = soupInit.find_all("li", {"class" : "recipe-ingredients__list__item" })
                ingredients = self.selectIngredient(ingredients)
                stepsPreparation =  soupInit.find_all("li", {"class" : "recipe-preparation__list__item" })
                stepsPreparation = self.selectPreparation(stepsPreparation)
                timePreparation = soupInit.find("div", {"class" : "recipe-infos__timmings__total-time title-4" }).text
                timePreparation = str(timePreparation).strip('\n').strip('\t')

                recipe = {
                    'image' : str(img),
                    'title' : str(title),
                    'peoples' : nbPeople,
                    'ingredients' : ingredients,
                    'steps_preparation' : stepsPreparation,
                    'timming': timePreparation
                }
                print(recipe)
                allRecipes.append(recipe)
            except :
                pass
        return allRecipes

    def selectIngredient(self, ingredients):
        allIngredients = []
        for i in ingredients:
            ingredient =  i.find("span", {"class" : "ingredient" }).text
            quantity = i.find("span", {"class" : "recipe-ingredient-qt"}).text
            allIngredients.append({ str(ingredient) : str(quantity) })
        return allIngredients

    def selectPreparation(self, steps):
        allSteps = []
        for i in steps:
            step = i.text
            step = str(step).strip('\n')
            step = step.strip("\t")
            allSteps.append(step)
        return allSteps

#recipeLinks = getRecipeLink(50)
#print(structurRecipe(recipes))


class recipe():
    def __init__(self, name ,recipe):
       self.body = { name : recipe}

def removearticles(text):
  text = re.sub("\s+(|miam|au|à|et|le|la|les|de|:|l'|aux|miam-mioum)(\s+)", '_', text)
  return text

scrap = marmiScrap()
recipeLinks = scrap.getRecipeLink(1)
recipes =  scrap.structurRecipe(recipeLinks)

for i in recipes:
    try:
        name = removearticles(i.get('title'))
        name = name.replace(' ', '_')
        name = name.replace("__", '_')
        name = name.replace("é", 'e')
        name = name.replace("l'", '_')
        new_recipe = recipe(name , i)
        print(new_recipe.body)
    except :
        pass