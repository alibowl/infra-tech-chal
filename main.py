from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
import requests

app = FastAPI()

API_BASE_URL = "https://pokeapi.co/api/v2/pokemon/"

@app.get("/", response_class=HTMLResponse)
def form():
    html_content = """
    <html>
    <head>
        <title>Pokémon Stats</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            table { border-collapse: collapse; width: 50%; margin: auto; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: center; }
            th { background-color: #4CAF50; color: white; }
            tr:nth-child(even) { background-color: #f2f2f2; }
            tr:hover { background-color: #ddd; }
            h1 { text-align: center; }
            form { text-align: center; margin-bottom: 40px; }
        </style>
    </head>
    <body>
        <h1>Enter a Pokémon Name</h1>
        <form action="/pokemon" method="post">
            <input type="text" name="pokemon_name" placeholder="e.g. charizard" required>
            <button type="submit">Search</button>
        </form>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.post("/pokemon", response_class=HTMLResponse)
def get_pokemon(pokemon_name: str = Form(...)):
    pokemon_name = pokemon_name.lower().strip()
    try:
        response = requests.get(f"{API_BASE_URL}{pokemon_name}")
        response.raise_for_status()
        data = response.json()

        name = data.get("name", "Unknown").title()
        poke_id = data.get("id", "-")
        height = data.get("height", "-")
        weight = data.get("weight", "-")
        types = ", ".join([t["type"]["name"].title() for t in data.get("types", [])])
        abilities = ", ".join([a["ability"]["name"].title() for a in data.get("abilities", [])])

        html_content = f"""
        <html>
        <head>
            <title>{name} Stats</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                table {{ border-collapse: collapse; width: 50%; margin: auto; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: center; }}
                th {{ background-color: #4CAF50; color: white; }}
                tr:nth-child(even) {{ background-color: #f2f2f2; }}
                tr:hover {{ background-color: #ddd; }}
                h1 {{ text-align: center; }}
                form {{ text-align: center; margin-bottom: 40px; }}
            </style>
        </head>
        <body>
            <h1>{name} Stats</h1>
            <table>
                <tr><th>Attribute</th><th>Value</th></tr>
                <tr><td>ID</td><td>{poke_id}</td></tr>
                <tr><td>Height</td><td>{height}</td></tr>
                <tr><td>Weight</td><td>{weight}</td></tr>
                <tr><td>Types</td><td>{types}</td></tr>
                <tr><td>Abilities</td><td>{abilities}</td></tr>
            </table>
            <div style="text-align:center; margin-top:20px;">
                <a href="/">Search Another Pokémon</a>
            </div>
        </body>
        </html>
        """
        return HTMLResponse(content=html_content, status_code=200)

    except requests.exceptions.RequestException:
        return HTMLResponse(f"<h2>Pokémon '{pokemon_name}' not found. <a href='/'>Try again</a></h2>", status_code=404)