import discord
from discord.ext import commands
import os
import json
import os

# Intents necesarios
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Bot con prefijo "!" y comandos habilitados
bot = commands.Bot(command_prefix="!", intents=intents)

# Diccionario donde se guardan los perfiles (en memoria)
if os.path.exists("perfiles.json"):
    with open("perfiles.json", "r") as f:
        perfiles = json.load(f)
else:
    perfiles = {}



# -------------------------------------
# COMANDO: PERFIL
# -------------------------------------
perfiles = {}  # Cambiar a perfiles[server_id][user_id]

@bot.command()
async def perfil(ctx):
    server_id = str(ctx.guild.id)
    user_id = str(ctx.author.id)

    if server_id not in perfiles:
        perfiles[server_id] = {}

    if user_id in perfiles[server_id]:
        await ctx.send("📝 Ya tienes un perfil registrado.")
        return

    # Resto del código...

    perfiles[server_id][user_id] = {
        # ...
    }


    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    await ctx.send("👤 Vamos a crear tu perfil. Responde con sinceridad.")

    await ctx.send("📅 ¿Cuál es tu edad?")
    edad = await bot.wait_for("message", check=check)

    await ctx.send("🌍 ¿De qué país eres?")
    pais = await bot.wait_for("message", check=check)

    await ctx.send("⚧️ ¿Cuál es tu género?")
    genero = await bot.wait_for("message", check=check)

    await ctx.send("🏳️‍🌈 ¿Cuál es tu orientación sexual?")
    orientacion = await bot.wait_for("message", check=check)

    await ctx.send("💘 ¿Qué tipo de personas te interesan?")
    interesado_en = await bot.wait_for("message", check=check)

    perfiles[server_id][user_id] = {
        "nombre": ctx.author.name,
        "edad": edad.content,
        "pais": pais.content,
        "genero": genero.content,
        "orientacion": orientacion.content,
        "interesado_en": interesado_en.content
    }
  with open("perfiles.json", "w") as f:
    json.dump(perfiles, f, indent=4)



    await ctx.send("✅ ¡Tu perfil ha sido creado con éxito! Usa `!buscar` para encontrar personas.")

# -------------------------------------
# COMANDO: BUSCAR
# -------------------------------------
@bot.command()
async def buscar(ctx):
    server_id = str(ctx.guild.id)
    user_id = str(ctx.author.id)

    if server_id not in perfiles or user_id not in perfiles[server_id]:
        await ctx.send("❌ No tienes un perfil. Usa `!perfil` para registrarte primero.")
        return

    # Obtener todos los usuarios del mismo servidor (menos tú)
    candidatos = [uid for uid in perfiles[server_id] if uid != user_id]

    if not candidatos:
        await ctx.send("😔 No hay más personas registradas todavía. Intenta más tarde.")
        return

    # Mostrar el primer perfil encontrado
    perfil = perfiles[server_id][candidatos[0]]
    embed = discord.Embed(
        title=f"🔎 Encontrado: {perfil['nombre']}",
        description=f"Edad: {perfil['edad']}\n"
                    f"País: {perfil['pais']}\n"
                    f"Género: {perfil['genero']}\n"
                    f"Orientación: {perfil['orientacion']}\n"
                    f"Interesado en: {perfil['interesado_en']}",
        color=discord.Color.pink()
    )
    await ctx.send(embed=embed)


# -------------------------------------
# COMANDO: HELP
# -------------------------------------
@bot.command()
async def ayuda(ctx):
    embed = discord.Embed(
        title="📖 Comandos disponibles",
        description="Aquí tienes una lista de comandos:",
        color=discord.Color.blue()
    )
    embed.add_field(name="!perfil", value="Crear tu perfil de citas", inline=False)
    embed.add_field(name="!buscar", value="Buscar personas compatibles", inline=False)
    embed.add_field(name="!help", value="Mostrar esta ayuda", inline=False)
    await ctx.send(embed=embed)

# -------------------------------------
# INICIAR EL BOT
# -------------------------------------
TOKEN = os.getenv("TOKEN")
if TOKEN is None:
    print("❌ ERROR: No se encontró el token. Asegúrate de tener la variable secreta 'TOKEN'.")
else:
    from keep_alive import keep_alive
    keep_alive()
    bot.run(TOKEN)
    TOKEN = os.getenv("TOKEN")

if TOKEN is None:
    print("❌ ERROR: TOKEN no está definido")
    exit(1)

print(f"TOKEN recibido: {TOKEN[:5]}...")  # Ahora sí es seguro porque TOKEN no es None

