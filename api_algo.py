from typing import Dict, Any
from fastapi import APIRouter, HTTPException
import ast
import numpy as np
from datetime import datetime, timedelta

from fetch_prices import fetch_historical_prices
from graei_strategy import GraeiStrategy
from graei_simulator import GraeiSimulator

router = APIRouter()

def validate_algorithm(code: str) -> bool:
    """Validate the Python code for safety and correctness."""
    try:
        parsed = ast.parse(code)
        # Check for required functions
        required_functions = {'initialize', 'analyze_market', 'should_trade', 'execute_trade'}
        found_functions = {node.name for node in ast.walk(parsed) if isinstance(node, ast.FunctionDef)}
        
        if not required_functions.issubset(found_functions):
            missing = required_functions - found_functions
            raise HTTPException(
                status_code=400,
                detail=f"Missing required functions: {', '.join(missing)}"
            )
            
        return True
    except SyntaxError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Syntax error in code: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error validating code: {str(e)}"
        )

def simulate_algorithm(code: str) -> Dict[str, Any]:
    """Run a simulation of the trading algorithm."""
    try:
        # Create a namespace for the algorithm
        namespace = {}
        exec(code, namespace)
        
        # Get historical price data for simulation
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)  # Last 30 days
        prices = fetch_historical_prices('BTC', start_date, end_date)
        
        initial_balance = 10000  # $10,000 USD
        strategy = GraeiStrategy()
        simulator = GraeiSimulator(strategy, initial_balance)
        
        # Run simulation
        trades = []
        equity_curve = [initial_balance]
        balance = initial_balance
        
        for i in range(1, len(prices)):
            # Get market data for analysis
            market_data = {
                'price': prices[i],
                'prev_price': prices[i-1],
                'timestamp': datetime.now() - timedelta(days=30-i)
            }
            
            # Run algorithm analysis
            analysis = namespace['analyze_market'](market_data)
            should_trade = namespace['should_trade'](analysis)
            
            if should_trade:
                # Execute trade
                trade_result = namespace['execute_trade'](analysis)
                trades.append(trade_result)
                
                # Update balance based on trade result
                if trade_result.get('type') == 'buy':
                    balance -= trade_result.get('amount', 0)
                else:
                    balance += trade_result.get('amount', 0)
                    
            equity_curve.append(balance)
        
        # Calculate performance metrics
        equity_array = np.array(equity_curve)
        roi = ((equity_array[-1] - equity_array[0]) / equity_array[0]) * 100
        
        # Calculate drawdown
        peak = np.maximum.accumulate(equity_array)
        drawdown = (peak - equity_array) / peak * 100
        max_drawdown = np.max(drawdown)
        
        # Calculate win rate
        if trades:
            winning_trades = sum(1 for t in trades if t.get('profit', 0) > 0)
            win_rate = (winning_trades / len(trades)) * 100
        else:
            win_rate = 0
            
        return {
            'roi': roi,
            'trades': len(trades),
            'winRate': win_rate,
            'drawdown': max_drawdown,
            'equity': equity_curve
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Simulation failed: {str(e)}"
        )

@router.post("/simulate")
async def simulate_trading(request: Dict[str, str]):
    """Endpoint to simulate a trading algorithm."""
    code = request.get('code')
    if not code:
        raise HTTPException(
            status_code=400,
            detail="No code provided"
        )
        
    if not validate_algorithm(code):
        return
        
    return simulate_algorithm(code)

@router.post("/ai-assist")
async def ai_assist(request: Dict[str, str]):
    """Endpoint to get AI assistance for algorithm improvement."""
    code = request.get('code')
    user_request = request.get('request')
    
    if not code or not user_request:
        raise HTTPException(
            status_code=400,
            detail="Both code and request must be provided"
        )
        
    try:
        # Analyze the code and provide suggestions
        # This is a placeholder - you would integrate with your AI service here
        suggestion = "# Enhanced version of your code\n"
        suggestion += code  # For now, just return the original code
        
        explanation = "Here's how we can improve your algorithm..."
        
        return {
            "suggestion": suggestion,
            "explanation": explanation
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"AI assistance failed: {str(e)}"
        )