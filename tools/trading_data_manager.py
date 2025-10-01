"""
Trading Data Manager for storing and combining trading analysis results
"""

import pandas as pd
from typing import List, Dict, Any
import json

class TradingDataManager:
    def __init__(self):
        self.trading_opportunities = []
        self.analysis_results = {}
    
    def add_stock_analysis(self, symbol: str, price: float, analysis_data: Dict[str, Any]):
        """Add analysis for a single stock"""
        self.analysis_results[symbol] = {
            'symbol': symbol,
            'current_price': price,
            'analysis': analysis_data
        }
    
    def get_stock_data(self, symbol: str) -> Dict[str, Any]:
        """Get stored analysis for a stock"""
        return self.analysis_results.get(symbol, {})
    
    def create_trading_opportunities(self) -> List[Dict[str, Any]]:
        """Create trading opportunities from stored analysis"""
        opportunities = []
        
        for symbol, data in self.analysis_results.items():
            if data and 'analysis' in data:
                analysis = data['analysis']
                opportunity = {
                    'symbol': symbol,
                    'price': data['current_price'],
                    'signal': analysis.get('signal', 'BUY'),
                    'entry': analysis.get('entry_price', data['current_price']),
                    'target': analysis.get('target_price', data['current_price'] * 1.02),
                    'stop_loss': analysis.get('stop_price', data['current_price'] * 0.99),
                    'risk_percent': analysis.get('risk_percent', 1.0),
                    'reward_percent': analysis.get('reward_percent', 2.0),
                    'probability': analysis.get('probability', 70),
                    'priority': analysis.get('priority', 'MEDIUM')
                }
                opportunities.append(opportunity)
        
        return opportunities
    
    def create_summary_table(self) -> str:
        """Create formatted summary table"""
        opportunities = self.create_trading_opportunities()
        
        if not opportunities:
            return "No trading opportunities available."
        
        # Create DataFrame
        df = pd.DataFrame(opportunities)
        
        # Format the table
        table = "📈 TRADING OPPORTUNITIES TABLE (5 OPPORTUNITIES):\n\n"
        table += "| # | Stock | Price | Signal | Entry | Target | Stop Loss | Risk% | Reward% | Prob% | Priority |\n"
        table += "|---|-------|-------|--------|-------|--------|-----------|-------|---------|-------|----------|\n"
        
        for i, opp in enumerate(opportunities, 1):
            table += f"| {i} | {opp['symbol']} | ₹{opp['price']:.2f} | {opp['signal']} | ₹{opp['entry']:.2f} | ₹{opp['target']:.2f} | ₹{opp['stop_loss']:.2f} | {opp['risk_percent']:.1f}% | {opp['reward_percent']:.1f}% | {opp['probability']}% | {opp['priority']} |\n"
        
        return table
    
    def get_analysis_summary(self) -> str:
        """Get summary of all analyses"""
        summary = []
        for symbol, data in self.analysis_results.items():
            if data and 'analysis' in data:
                analysis = data['analysis']
                summary.append(f"**{symbol}**: {analysis.get('summary', 'Analysis completed')}")
        
        return "\n".join(summary)
    
    def clear_data(self):
        """Clear all stored data"""
        self.trading_opportunities = []
        self.analysis_results = {}

# Global instance
trading_manager = TradingDataManager()
