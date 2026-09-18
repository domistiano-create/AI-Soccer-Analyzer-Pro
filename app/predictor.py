import json
import urllib.request
from fastapi import APIRouter, HTTPException, status
from app.database import get_db_connection

router = APIRouter(prefix="/analytics", tags=["AI Soccer Engine"])

API_TOKEN = "free-tier-token-placeholder"

def fetch_live_team_stats(team_name: str) -> dict:
    """Calls Football-Data.org to gather team standings metrics."""
    url = "https://football-data.org"
    req = urllib.request.Request(url)
    req.add_header("X-Auth-Token", API_TOKEN)
    
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode())
            for table in data.get("standings", [{}])[0].get("table", []):
                current_team = table.get("team", {}).get("name", "").lower()
                if team_name.lower() in current_team or current_team in team_name.lower():
                    played = table.get("playedGames", 1)
                    won = table.get("won", 0)
                    goals_for = table.get("goalsFor", 0)
                    goals_against = table.get("goalsAgainst", 0)
                    
                    return {
                        "form": round(1.0 + ((won / played) * 4.0), 1),
                        "attack_strength": goals_for / played,
                        "defense_weakness": goals_against / played
                    }
    except Exception:
        pass
    return {"form": 3.0, "attack_strength": 1.4, "defense_weakness": 1.2}

@router.post("/predict-match-advanced")
def predict_match_advanced(username: str, home_team: str, away_team: str):
    """Advanced prediction engine returning Double Chance, Over/Under 2.5, and Live Decimal Odds."""
    username = username.strip()
    COST = 2.0
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT balance FROM wallets WHERE username = ?", (username,))
    row = cursor.fetchone()
    
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Wallet account not found.")
        
    current_balance = row["balance"]
    if current_balance < COST:
        conn.close()
        raise HTTPException(status_code=402, detail="Insufficient funds.")
        
    new_balance = current_balance - COST
    cursor.execute("UPDATE wallets SET balance = ? WHERE username = ?", (new_balance, username))
    conn.commit()
    conn.close()
    
    home_stats = fetch_live_team_stats(home_team)
    away_stats = fetch_live_team_stats(away_team)
    
    # 1. Calculate Standard Probabilities
    total_form = home_stats["form"] + away_stats["form"]
    home_win_pct = round((home_stats["form"] / total_form) * 100, 1)
    away_win_pct = round((away_stats["form"] / total_form) * 100, 1)
    draw_pct = round(100.0 - (home_win_pct + away_win_pct), 1)
    
    # 2. Compute Double Chance & Over/Under
    double_chance_1X = round(home_win_pct + draw_pct, 1)
    double_chance_X2 = round(away_win_pct + draw_pct, 1)
    recommended_double_chance = "1X" if double_chance_1X > double_chance_X2 else "X2"
    
    total_projected_goals = (home_stats["attack_strength"] + away_stats["defense_weakness"] + 
                             away_stats["attack_strength"] + home_stats["defense_weakness"]) / 2
    over_under_market = "OVER 2.5 Goals" if total_projected_goals > 2.5 else "UNDER 2.5 Goals"
    
    # 3. LIVE ODDS ENGINE CALCULATION (Implied Inverse Probability Pricing Coefficients)
    # Bookmaker Odds = 1 / Probability (with a small safety margin margin added)
    home_odds = round(95.0 / home_win_pct, 2) if home_win_pct > 0 else 5.0
    draw_odds = round(95.0 / draw_pct, 2) if draw_pct > 0 else 3.5
    away_odds = round(95.0 / away_win_pct, 2) if away_win_pct > 0 else 5.0
    
    # Map double chance coefficient line odds markers
    recommended_dc_odds = round(95.0 / max(double_chance_1X, double_chance_X2), 2)

    return {
        "status": "success",
        "fixture": f"{home_team} vs {away_team}",
        "probabilities": {
            "1 (Home Win)": f"{home_win_pct}%",
            "X (Draw)": f"{draw_pct}%",
            "2 (Away Win)": f"{away_win_pct}%"
        },
        "live_decimal_odds": {
            "home_win_odds": home_odds,
            "draw_odds": draw_odds,
            "away_win_odds": away_odds,
            "recommended_dc_odds": recommended_dc_odds
        },
        "betting_markets": {
            "double_chance": {
                "1X_probability": f"{double_chance_1X}%",
                "X2_probability": f"{double_chance_X2}%",
                "recommended_pick": recommended_double_chance
            },
            "total_goals_2.5": {
                "projected_total_goals": round(total_projected_goals, 2),
                "recommended_pick": over_under_market
            }
        },
        "transaction_details": {
            "credits_deducted": COST,
            "remaining_balance": new_balance
        }
    }
