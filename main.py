import discord
import os
import random
#import asyncio
# Bot token
TOKEN = ''
# Create bot instance with intents
intents = discord.Intents.all()
bot = discord.Client(intents=intents)

gute_wörter = ["redlich", "töft", "schnaft"]
schlechte_wörter = ["töricht", "verlottert", "antischnaft"]
schlechte_begriffe = ["Kleingeistern", "Knabbuben"]
# Event for bot ready
async def create_strebergarten_if_not_available(garten, streber, message, create=True):
    if not os.path.exists(f"strebergaerten/{streber}/{garten}.txt"):
       if create:
        await message.channel.send(f"{streber.capitalize()} hat nun einen {garten.capitalize()}strebergarten")
        await message.channel.send("Strebergartengröße: 1m²")
        with open(f"strebergaerten/{streber}/{garten}.txt", "w") as f:
           f.write("1")
           pass
       else:
         await message.channel.send(f"{streber.capitalize()} hat keinen {garten.capitalize()}strebergarten, der zerstört werden kann")
       return True
    else:
        return False
async def rmalias(alias):
    with open("aliasfile", "r") as f:
        lines = []
        for line in f.readlines():
            lines.append(line.rstrip("\n"))
    i = -1
    for line in lines:
        i+=1
        if line.split(">")[0]==alias:
            del lines[i]
            break
    with open("aliasfile", "w") as f:
        for line in lines:
            f.write(line+"\n")
        
async def add_to_aliasfile(alias, user):
    with open("aliasfile", "a") as f:
        f.write(alias+">"+user)
        f.write("\n")
        
async def get_user_names(guild):
    user_names = []
    for member in guild.members:
        if not member.bot:
            user_names.append(member.name)
    return user_names

@bot.event
async def on_ready():
    if not os.path.exists("aliasfile"):
        with open("aliasfile", "w") as f:
            pass
        print("Alias-File created")
    if not os.path.exists("strebergaerten"):
        os.mkdir("strebergaerten")
        print("Strebergartenordner erstellt")
    print(f'{bot.user.name} has connected to Discord!')

# Event for message received
async def remove_strebergarten(streber, garten):
    os.remove(f"strebergaerten/{streber}/{garten}.txt")
async def list_users():
    return os.listdir("strebergaerten")
async def write_strebergarten_area(streber, garten, newarea):
    with open(f"strebergaerten/{streber}/{garten}.txt", "r") as f:
        lines = f.readlines()
    lines[0] = str(newarea)+"\n"
    with open(f"strebergaerten/{streber}/{garten}.txt", "w") as f:
        for line in lines:
            f.write(line)
async def get_strebergarten_area(streber, garten):
    with open(f"strebergaerten/{streber}/{garten}.txt", "r") as f:
        return int(f.readlines()[0].rstrip("\n"))
async def strebergarten_vergroesern(streber, garten, message):
    area = await get_strebergarten_area(streber, garten)
    rannum = random.randint(5,15)
    area = area+rannum
    await message.channel.send(f"{random.choice(vergroeßert_message)} {streber.capitalize()}s {garten.capitalize()}strebergarten wurde um {rannum}m² vergrößert")
    await write_strebergarten_area(streber, garten, area)
async def get_alias(alias):
    with open("aliasfile", "r") as f:
        for line in f.readlines():
           line=line.rstrip("\n")
           if line.split(">")[0] == alias:
               return line.split(">")[1].lower()
        return "notfound"
async def strebergarten_verkleinern(streber, garten, message):
    area = await get_strebergarten_area(streber, garten)
    rannum = random.randint(5,15)
    area = area-rannum
    if area<=0:
        await message.channel.send(f"{streber.capitalize()}s {garten.capitalize()}strebergarten wurde zerstört.")
        await remove_strebergarten(streber, garten)
        return "zerstört"
    else:
        await message.channel.send(f"{random.choice(verkleinert_message)} {streber.capitalize()}s {garten.capitalize()}strebergarten wurde um {rannum}m² verkleinert")
    await write_strebergarten_area(streber, garten, area)
@bot.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == bot.user:
        return
    if message.content.startswith("!"):
        if message.author.id != 789073929925951529:
            await message.channel.send(f"{random.choice(schlechte_wörter).capitalize()}en {random.choice(schlechte_begriffe).capitalize()} ist das benutzen des {random.choice(gute_wörter).capitalize()}en Strebergarten-Bots nicht gestattet")
            return

    if message.content.startswith("!help"):
        await message.channel.send("!alias <alias> <account>\n!generiere_strebergartenwiesen\n!rmalias <alias>\n!strebergarten <account oder alias> <strebergartenname> <+/->")
    if message.content.startswith("!generiere_strebergartenwiesen"):
        server = message.guild
        users = await get_user_names(server)
        for user in users:
            if not os.path.exists(f"strebergaerten/{user}"):
                os.mkdir(f"strebergaerten/{user}")
                await message.channel.send(f"{user} Strebergartenwiese wurde erstellt")
    if message.content.startswith('!alias'):
        part1 = message.content.split(" ")[1]
        part2 = message.content.split(" ")[2]
        users = await list_users()
        if part2.lower() not in users:
           await message.channel.send(f"Nutzer {part2} existiert nicht. {random.choice(schlechte_wörter).capitalize()}.")
           return
        else:
           await add_to_aliasfile(part1,part2)        
           await message.channel.send(f"Alias hinzugefügt ({part1} --> {part2})")
    if message.content.startswith("!rmalias"):
        await rmalias(message.content.split(" ")[1])
        await message.channel.send(f"Alias {message.content.split(' ')[1]} entfernt")
    if message.content.startswith("!strebergarten"):
        split = message.content.split(" ")
        streber = split[1].lower()
        garten = split[2].lower()
        op = split[3]
        users = await list_users()
        if streber not in users:
           streber = await get_alias(streber)
           if streber=="notfound":
               await message.channel.send("Dieser Nutzer existiert gar nicht, sapperlot")
               return
           
        if "-" in op:
            has_been_created = await create_strebergarten_if_not_available(garten, streber, message, False)
            if has_been_created: return
        elif "+" in op:
            has_been_created = await create_strebergarten_if_not_available(garten, streber, message)
            if has_been_created: return
        else:
            await message.channel.send("Verlotterter Knabbub")
            return
        if "-" in op:
            for i in range(0, len(op)):
               result = await strebergarten_verkleinern(streber, garten, message)
               if result == "zerstört":
                  return
             
            await message.channel.send(f"Strebergartengröße: {await get_strebergarten_area(streber,garten)}m²")
        if "+" in op:
            for i in range(0, len(op)):
               result = await strebergarten_vergroesern(streber, garten, message)
            await message.channel.send(f"Strebergartengröße: {await get_strebergarten_area(streber,garten)}m²")
vergroeßert_message = ["Beeindrucked!", "Fabelhaft!", "Fantastisch!", "Turboschnaft!", "Schöne neue Hängepflanze", "Der Maulwurf hatte keine Chance!", "Schnafter neuer Springbrunnen! ", "Der Bär wurde erschossen!", "Der Fuchs wurde erschossen", "Der Igel wurde erschossen!", "Das Unkrauft wurde mit der Planierraupe platt gemacht!", "Die dreckigen Blattläuse wurden zermatscht!", "Schöne neue Statue!", "Gut das der verloterte Rasen mal gemäht wurde!", "Schnaft das Laub weggefegt", "Mit dem Rechen die kackenden Vögel vom Himmel geholt!", "Der Maulwurfshügel hatte keine Chance gegen die Dampfwalze!", "Der Raubvogel wurde gescharfschützengewehrt!", "Schöne neue Bank!", "Dieser neue Gartenweg ist sehr schnaft!", "Gegen den Schaufelradbager konnten die Engerlinge nichts ausrichten!", "Durch den Flammenwerfer sind die Stechmücken jetzt weg!", "Gut, dass der Teich jetzt Libellenlarvenfrei ist!", "Das Unkraut wurde mit Benzin übergossen und angezündet!", "Schön das Unkraut mit der Axt vernichtet!", "Schnaft die wucherende Hecke mit der Heckenschere gestutzt!", "Toll, dass der Unkrautbaum jetzt brennt!", "Sehr schön das Eck mit den Maulwürfen mit dem Pflug umgegraben", "Krasse neue Fleischflessende Pflanze", "Die Wühlmeuse wurden knadenlos vom Polenböller ausgereuchert!"]

verkleinert_message = ["Oh weh, die Pflanze ist eingegangen.", "Die Fleischfressende Pflanze hat wohl leider nicht genug Fleisch bekommen.", "Die Hängepflanze ist runtergefallen und zerbrochen.", "In einer Ecke des schnaften Gartens ist ein Maulwurf zu hören.", "Wühlmäuse haben einen Teil des Gemüsebeets gefressen.", "Ein Bär wurde gesichtet", "Ein Fuchs wurde gesichtet", "Ein Wolf wurde gesichtet","Der trockene Rasen wurde von asozialen Kindern angezündet und ist abgebrannt.", "Dreckskinder sind mit ihrem Fahrrad durch das Blumenbeet gefahren.", "Die Bismarckstatue ist gegen den Komposter gefallen.", "Das Gartenhaus wurde von einem Terroristen gesprengt.", "Jemand hat über die Hecke Maulwürfe hineingeschmissen", "Das verlotterte Nachbarskind hat mit seinem Ball einen Gartenzwerge zerstört.", "Überall wächst Unkraut.", "5 Pflanzen sind erfroren", "Herr fester hat einen Rückdreher in den Goldfischteich gemacht.", "Tinas Reckinger hat einige Pflanzen mit Unkrautvernichter gegossen.", "Frau Petzhold hat eine Wurfbiebel auf den Salad geworfen.","Herr Fester hat Uranstaub in den Blumenkästen verteilt"]
# Run the bot
bot.run(TOKEN)
