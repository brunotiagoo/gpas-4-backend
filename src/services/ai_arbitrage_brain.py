"""
GPAS 4.0 - CÉREBRO DE IA REVOLUCIONÁRIO
Sistema de IA que supera Tactical Arbitrage, SourceMogul e todos os outros
Funcionalidades que NENHUMA outra plataforma tem
"""

import requests # Keep for potential future direct API calls, though not used by scraper
import json
import time
import random
from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import List, Dict, Optional
import threading
import schedule
from .global_scraper import ScraperEngine # Import the scraper

@dataclass
class ArbitrageOpportunity:
    product_name: str
    source_platform: str
    source_price: float
    source_currency: str
    target_platform: str
    target_price: float
    target_currency: str
    profit: float # Net profit after estimated costs
    roi_percentage: float # ROI based on net profit and source price
    confidence_score: float # How confident is the AI/system in this opportunity
    risk_level: str # e.g., LOW, MEDIUM, HIGH
    shipping_time: int # Estimated shipping time from source in days
    category: str # Product category
    trend_score: float # 0-100 score indicating trendiness
    viral_potential: float # 0-1 score indicating viral potential
    auto_buy_recommended: bool # Whether the system recommends auto-purchasing
    # Optional fields from scraper
    source_url: Optional[str] = None
    target_url: Optional[str] = None
    notes: Optional[str] = None # To add context like "Data from live scrape" or "Simulated data"
    generative_insight: Optional[str] = None # For AI-generated text

@dataclass
class MarketTrend:
    product_category: str
    trend_direction: str  # 'rising', 'falling', 'stable'
    momentum: float  # 0-100
    seasonal_factor: float
    viral_indicators: List[str]
    predicted_peak: datetime

class AIArbitrageBrain:
    """
    Cérebro de IA que supera TODA a concorrência:
    - Tactical Arbitrage: Apenas encontra, nós EXECUTAMOS
    - SourceMogul: ML básico, nós temos IA GENERATIVA
    - AlgosOne: Apenas crypto, nós dominamos PRODUTOS FÍSICOS
    """
    
    def __init__(self):
        self.opportunities = [] # This might be deprecated if opportunities are generated on-the-fly per scan
        self.market_trends = {} # For storing market trend data
        self.auto_trading_enabled = True
        self.risk_tolerance = 0.7  # 0-1 scale
        self.min_roi = 25  # Minimum ROI target for an opportunity to be considered (as per GPAS 3.0 doc)
        self.max_investment_per_product = 1000  # USD
        self.total_daily_budget = 5000  # USD
        self.current_daily_spent = 0
        self.scraper = ScraperEngine() # Instantiate the scraper
        self.generative_ai_api_key = os.environ.get("GENERATIVE_AI_API_KEY") # Placeholder for API key
        self.generative_ai_endpoint = os.environ.get("GENERATIVE_AI_ENDPOINT") # Placeholder for API endpoint


        # Product list for scanning - can be dynamic or from a predefined list
        # For MVP, using the scraper's target products as a starting point
        self.products_to_scan = self.scraper.target_products

        # Define categories for products - this could be more dynamic in a real system
        self.product_categories = {
            "Xiaomi Mi Band 8": "electronics",
            "Anker PowerCore 10000": "electronics",
            # Add more product-to-category mappings as needed
        }

        # Information about platforms, including those the scraper targets
        # This can be expanded and made more dynamic
        self.platform_info = {
            'AliExpress.com': {
                'base_url': 'https://www.aliexpress.com',
                'currency': 'USD',
                'shipping_time_days': 20, # Average estimate
                'reliability_score': 0.8, # Subjective score
                'is_source': True
            },
            'Amazon.com': {
                'currency': 'USD',
                'platform_fees_percentage': 0.15, # Standard Amazon referral fee
                'shipping_time_days': 2, # Prime shipping estimate for selling
                'reliability_score': 0.9,
                'is_target': True
            },
            # Add more platforms as the scraper supports them or for simulation
            'SimulatedSource': {
                'currency': 'USD',
                'shipping_time_days': 15,
                'reliability_score': 0.7,
                'is_source': True
            },
            'SimulatedTarget': {
                'currency': 'USD',
                'platform_fees_percentage': 0.12,
                'shipping_time_days': 3,
                'reliability_score': 0.85,
                'is_target': True
            }
        }

    def get_product_category(self, product_name: str) -> str:
        return self.product_categories.get(product_name, "general")


    def predict_viral_products(self) -> List[Dict]: # Return type changed to List[Dict]
        """
        IA PREDITIVA - Funcionalidade que NENHUMA concorrência tem!
        Prediz produtos que vão explodir antes de mais ninguém descobrir
        """
        # This remains largely simulated for MVP
        # In a real system, this would involve complex data analysis, trend watching, etc.
        viral_indicators = [
            'TikTok trending', 'Instagram influencer mentions',
            'YouTube reviews spike', 'Reddit discussions increase',
            'Google Trends rising', 'Celebrity endorsements'
        ]
        
        simulated_trending_products = []
        # Use products_to_scan or a broader list for simulation
        for product_name in self.products_to_scan:
            category = self.get_product_category(product_name)
            viral_score = random.uniform(0, 100)
            if viral_score > 75:  # High viral potential
                simulated_trending_products.append({
                    'product': product_name,
                    'category': category,
                    'viral_score': viral_score,
                    'predicted_peak_date': (datetime.now() + timedelta(days=random.randint(7, 30))).isoformat(),
                    'prediction_confidence': random.uniform(0.7, 0.95),
                    'potential_reason': random.choice(viral_indicators)
                })

        return simulated_trending_products

    def analyze_market_sentiment(self, product_name: str) -> Dict:
        """
        ANÁLISE DE SENTIMENT - Outra funcionalidade única!
        Analisa sentiment em redes sociais para prever demanda
        """
        # This also remains largely simulated for MVP.
        # Real implementation would require NLP processing of social media, reviews, etc.
        sentiments = ['very_positive', 'positive', 'neutral', 'negative', 'mixed']
        # sentiment = random.choice(sentiments) # Corrected: Use chosen_sentiment below

        simulated_sentiment_scores = {
            'very_positive': {'score': random.uniform(0.8, 1.0), 'demand_impact_multiplier': 1.5},
            'positive': {'score': random.uniform(0.6, 0.8), 'demand_impact_multiplier': 1.2},
            'neutral': {'score': random.uniform(0.4, 0.6), 'demand_impact_multiplier': 1.0},
            'mixed': {'score': random.uniform(0.3, 0.7), 'demand_impact_multiplier': 1.0},
            'negative': {'score': random.uniform(0.0, 0.4), 'demand_impact_multiplier': 0.7}
        }
        
        chosen_sentiment = random.choice(sentiments)
        return {
            'product_name': product_name,
            'overall_sentiment': chosen_sentiment,
            'sentiment_score': simulated_sentiment_scores[chosen_sentiment]['score'],
            'demand_impact_multiplier': simulated_sentiment_scores[chosen_sentiment]['demand_impact_multiplier'],
            'simulated_positive_mentions': random.randint(50, 5000),
            'simulated_negative_mentions': random.randint(0, 1000),
            'analysis_source': "Simulated Social Media Scan"
        }

    def get_generative_insight(self, opportunity: ArbitrageOpportunity) -> Optional[str]:
        """
        Calls a generative AI API to get a brief insight on the arbitrage opportunity.
        This is a placeholder and needs a real API endpoint and key.
        For MVP, it will return a simulated insight if API key/endpoint is not set.
        """
        if not self.generative_ai_api_key or not self.generative_ai_endpoint:
            # Simulate if API key or endpoint is not configured
            simulated_insights = [
                f"O produto {opportunity.product_name} parece ter um bom potencial de ROI ({opportunity.roi_percentage:.2f}%).",
                f"A diferença de preço para {opportunity.product_name} entre {opportunity.source_platform} e {opportunity.target_platform} é notável.",
                "Considerar a liquidez e os custos de envio para esta oportunidade.",
                "Uma análise mais aprofundada das tendências de mercado para esta categoria é recomendada."
            ]
            return f"(Insight Simulado) {random.choice(simulated_insights)}"

        prompt = (
            f"Analise esta oportunidade de arbitragem e forneça um breve insight (1-2 frases) sobre o seu potencial. "
            f"Produto: '{opportunity.product_name}', "
            f"Comprar em: '{opportunity.source_platform}' por {opportunity.source_price} {opportunity.source_currency}, "
            f"Vender em: '{opportunity.target_platform}' por {opportunity.target_price} {opportunity.target_currency}, "
            f"ROI Estimado: {opportunity.roi_percentage:.2f}%. "
            f"Notas Adicionais: {opportunity.notes if opportunity.notes else 'N/A'}."
        )

        headers = {
            "Authorization": f"Bearer {self.generative_ai_api_key}",
            "Content-Type": "application/json"
        }
        # The payload structure depends heavily on the specific AI API being used.
        # This is a generic example. For Google's Gemini, it would be different.
        payload = {
            "prompt": prompt,
            "max_tokens": 60,
            "temperature": 0.7
        }

        try:
            print(f"🤖 Chamando API de IA generativa para insight sobre: {opportunity.product_name}")
            response = requests.post(self.generative_ai_endpoint, headers=headers, json=payload, timeout=15)
            response.raise_for_status() # Raises an exception for bad status codes (4xx or 5xx)

            response_data = response.json()
            # Again, parsing the response is API-specific.
            # Example: response_data.get('choices', [{}])[0].get('text', '').strip() for some OpenAI-like APIs
            # Example: response_data.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text') for Gemini

            # Placeholder for actual parsing logic based on the chosen API
            # For now, let's assume a simple structure for demonstration
            insight_text = response_data.get("generated_text_insight", "Não foi possível extrair o insight da resposta da API.")

            print(f"💡 Insight da IA recebido: {insight_text}")
            return insight_text.strip()

        except requests.exceptions.RequestException as e:
            print(f"❌ Erro ao chamar API de IA generativa: {e}")
            return "(Erro ao obter insight da IA)"
        except Exception as e:
            print(f"❌ Erro inesperado ao processar resposta da IA: {e}")
            return "(Erro ao processar insight da IA)"

    # This function can be called by the scraper's calculate_arbitrage_opportunity or be used here
    # For now, let's assume the scraper provides opportunities with net_profit and roi_percentage already calculated
    # based on its own cost estimations.
    # If we want AI brain to do its own ROI calc from raw prices, we'd need a function like this:
    def _calculate_opportunity_financials(self,
                                         product_name: str,
                                         source_platform_name: str,
                                         source_price: float,
                                         target_platform_name: str,
                                         target_price: float) -> Optional[Dict]:
        """
        Calculates profit, ROI, and other financial details for a potential opportunity.
        Uses platform_info for fees and shipping estimates.
        """
        source_platform_details = self.platform_info.get(source_platform_name)
        target_platform_details = self.platform_info.get(target_platform_name)

        if not source_platform_details or not target_platform_details:
            print(f"Missing platform details for {source_platform_name} or {target_platform_name}")
            return None

        if source_price <= 0 or target_price <= 0: # Basic sanity check
            return None

        # Estimated costs - these are highly variable and simplified for MVP
        # Shipping from source: could be a % of price, flat fee, or from scraper
        estimated_shipping_from_source = source_price * 0.10 # Default 10% if not provided
        
        # Target platform fees
        target_platform_fee_percentage = target_platform_details.get('platform_fees_percentage', 0.15)
        target_platform_fees = target_price * target_platform_fee_percentage
        
        # Other potential costs (simulated for now)
        payment_processing_fees = target_price * 0.03 # e.g., 3%
        misc_handling_costs = 1.0 # Small flat fee per item

        total_cost_of_goods = source_price + estimated_shipping_from_source
        total_selling_expenses = target_platform_fees + payment_processing_fees + misc_handling_costs

        net_profit = target_price - total_cost_of_goods - total_selling_expenses
        
        if net_profit <= 0:
            return None # Not profitable

        roi_on_investment = (net_profit / total_cost_of_goods) * 100 # ROI on COGS

        return {
            "product_name": product_name,
            "source_platform": source_platform_name,
            "source_price": source_price,
            "target_platform": target_platform_name,
            "target_price": target_price,
            "estimated_shipping_from_source": round(estimated_shipping_from_source,2),
            "estimated_target_platform_fees": round(target_platform_fees,2),
            "estimated_other_costs": round(payment_processing_fees + misc_handling_costs, 2),
            "net_profit": round(net_profit, 2),
            "roi_percentage": round(roi_on_investment, 2),
            "source_currency": source_platform_details.get('currency', 'USD'),
            "target_currency": target_platform_details.get('currency', 'USD'),
        }


    def auto_execute_purchase(self, opportunity: ArbitrageOpportunity) -> Dict:
        """
        EXECUÇÃO AUTOMÁTICA - A funcionalidade que VAI DESTRUIR a concorrência!
        Enquanto outros apenas "encontram", nós COMPRAMOS automaticamente!
        """
        # This remains heavily simulated as real auto-purchase is complex and risky for MVP
        if not self.auto_trading_enabled:
            return {'status': 'auto_trading_disabled', 'message': 'Auto-trading is currently disabled by the user.'}
        
        if self.current_daily_spent + opportunity.source_price > self.total_daily_budget:
            return {'status': 'budget_exceeded', 'message': f'Purchase of {opportunity.source_price} would exceed daily budget of {self.total_daily_budget}. Spent: {self.current_daily_spent}'}
        
        if opportunity.roi_percentage < self.min_roi: # Using the class's min_roi
            return {'status': 'roi_too_low', 'message': f'Opportunity ROI {opportunity.roi_percentage:.2f}% is below minimum threshold {self.min_roi}%'}
        
        # Risk assessment based on confidence score (could be more complex)
        if opportunity.confidence_score < self.risk_tolerance: # risk_tolerance is 0-1, higher means more tolerance
            return {'status': 'risk_too_high', 'message': f'Opportunity confidence score {opportunity.confidence_score:.2f} is below risk tolerance {self.risk_tolerance}'}
        
        # Simulate purchase attempt
        purchase_amount = min(opportunity.source_price, self.max_investment_per_product)
        print(f"🤖 Simulating purchase of '{opportunity.product_name}' from {opportunity.source_platform} for ${purchase_amount:.2f}")
        time.sleep(random.uniform(0.5, 1.5)) # Simulate API call latency
        
        # Simulate success/failure (e.g., stock issues, payment failure)
        simulated_success_rate = 0.85 # 85% chance of successful simulated purchase
        if random.random() < simulated_success_rate:
            self.current_daily_spent += purchase_amount
            return {
                'status': 'success',
                'message': f"Simulated purchase of '{opportunity.product_name}' for ${purchase_amount:.2f} was successful.",
                'product_name': opportunity.product_name,
                'purchased_amount': purchase_amount,
                'source_platform': opportunity.source_platform,
                'simulated_order_id': f'SIM_ORD_{random.randint(100000, 999999)}',
                'estimated_delivery_date': (datetime.now() + timedelta(days=opportunity.shipping_time)).isoformat(),
                'daily_budget_remaining': self.total_daily_budget - self.current_daily_spent
            }
        else:
            return {
                'status': 'failed',
                'message': f"Simulated purchase of '{opportunity.product_name}' failed. (e.g., out of stock, payment issue)",
                'product_name': opportunity.product_name,
                'attempted_amount': purchase_amount,
                'reason': random.choice(['Simulated out of stock', 'Simulated payment error', 'Simulated price change'])
            }

    def scan_global_opportunities(self) -> List[ArbitrageOpportunity]:
        """
        SCAN GLOBAL - Muito mais abrangente que Tactical Arbitrage ou SourceMogul
        Escaneia TODOS os mercados globais simultaneamente (integrating scraper)
        """
        all_generated_opportunities = []
        print(f"🌍 INICIANDO SCAN GLOBAL DE ARBITRAGEM (AI Brain)...")
        print(f"🧠 Produtos para scan: {self.products_to_scan}")

        for product_name_query in self.products_to_scan:
            print(f"\n🔍 Analisando produto: {product_name_query}")
            
            # 1. Get data from scraper
            # The scraper's run_scraping_cycle returns a dict with 'summary' and 'opportunities'
            # We are interested in the 'opportunities' found by the scraper for this product_name_query
            # For a single product query, we'd call scrape_all_sites_for_product
            scraped_data_list = self.scraper.scrape_all_sites_for_product(product_name_query)

            # The scraper's calculate_arbitrage_opportunity can find direct arbitrage paths
            # based on its predefined logic (e.g., AliE -> Amz)
            scraper_opportunities = self.scraper.calculate_arbitrage_opportunity(scraped_data_list, self.min_roi)

            if scraper_opportunities:
                print(f"    scraper encontrou {len(scraper_opportunities)} oportunidades para '{product_name_query}'")
                for opp in scraper_opportunities:
                    # Enhance scraper opportunity with AI Brain's simulated scores
                    category = self.get_product_category(opp['product_name_query'])
                    sentiment_analysis = self.analyze_market_sentiment(opp['product_name_query'])

                    # Confidence score can be a mix of scraper data quality and AI analysis
                    # For now, using a simulated score based on platform reliability (if available) and sentiment
                    source_platform_reliability = self.platform_info.get(opp['buy_from_platform'], {}).get('reliability_score', 0.7)
                    target_platform_reliability = self.platform_info.get(opp['sell_on_platform'], {}).get('reliability_score', 0.7)
                    confidence_score = round(
                        (source_platform_reliability * target_platform_reliability)**0.5 * \
                        sentiment_analysis['sentiment_score'], 2
                    )

                    risk_level = "MEDIUM" # Default
                    if opp['estimated_roi_percentage'] > 75 and confidence_score > 0.7:
                        risk_level = "LOW"
                    elif opp['estimated_roi_percentage'] < 30 or confidence_score < 0.4:
                        risk_level = "HIGH"

                    shipping_time = self.platform_info.get(opp['buy_from_platform'], {}).get('shipping_time_days', 20)

                    arbitrage_opp = ArbitrageOpportunity(
                        product_name=opp['product_name_query'], # or more specific title if available
                        source_platform=opp['buy_from_platform'],
                        source_price=opp['buy_price'],
                        source_currency=self.platform_info.get(opp['buy_from_platform'], {}).get('currency', 'USD'),
                        target_platform=opp['sell_on_platform'],
                        target_price=opp['sell_price'],
                        target_currency=self.platform_info.get(opp['sell_on_platform'], {}).get('currency', 'USD'),
                        profit=opp['estimated_net_profit'],
                        roi_percentage=opp['estimated_roi_percentage'],
                        confidence_score=confidence_score,
                        risk_level=risk_level,
                        shipping_time=shipping_time,
                        category=category,
                        trend_score=round(sentiment_analysis['sentiment_score'] * 100,1), # Example trend score
                        viral_potential=round(random.uniform(0.1, 0.8) * sentiment_analysis['demand_impact_multiplier'],2), # Simulated
                        auto_buy_recommended=(opp['estimated_roi_percentage'] > self.min_roi + 20 and confidence_score > 0.75), # Stricter for auto-buy
                        source_url=opp['buy_url'],
                        target_url=opp['sell_url'],
                        notes="Data primarily from live scrape."
                    )
                    # Get generative insight
                    arbitrage_opp.generative_insight = self.get_generative_insight(arbitrage_opp)
                    all_generated_opportunities.append(arbitrage_opp)
                    print(f"   ✅ Oportunidade REAL (com IA scores): {arbitrage_opp.product_name} ROI: {arbitrage_opp.roi_percentage:.2f}%")
                    if arbitrage_opp.generative_insight:
                        print(f"      🤖 Insight da IA: {arbitrage_opp.generative_insight}")


            else: # No direct arbitrage from scraper, try to simulate or find other paths
                print(f"   ℹ️ Scraper não encontrou oportunidades diretas para '{product_name_query}'. Considerar simulação ou análise de dados brutos.")
                # --- Simulation Logic (fallback or for products not covered by scraper's direct path) ---
                # This part can be more elaborate, trying to pair different source/target data points from scraped_data_list
                # or falling back to fully simulated data if scraped_data_list is empty for this product.
                
                # Fallback: If scraper found nothing or no arbitrage, generate a simulated opportunity for demo
                if not scraper_opportunities: # or even if scraped_data_list is empty
                    print(f"   ⚠️ Gerando oportunidade SIMULADA para '{product_name_query}' por falta de dados reais suficientes.")
                    sim_source_platform_name = 'SimulatedSource'
                    sim_target_platform_name = 'SimulatedTarget'

                    sim_source_price = random.uniform(10, 80)
                    # Ensure target price is higher for potential profit
                    sim_target_price = sim_source_price * random.uniform(1.5, 4.0)

                    financials = self._calculate_opportunity_financials(
                        product_name_query,
                        sim_source_platform_name,
                        sim_source_price,
                        sim_target_platform_name,
                        sim_target_price
                    )

                    if financials and financials['roi_percentage'] > self.min_roi:
                        category = self.get_product_category(product_name_query)
                        sentiment_analysis = self.analyze_market_sentiment(product_name_query)
                        source_platform_reliability = self.platform_info.get(sim_source_platform_name, {}).get('reliability_score', 0.6)
                        target_platform_reliability = self.platform_info.get(sim_target_platform_name, {}).get('reliability_score', 0.7)
                        confidence_score = round(
                            (source_platform_reliability * target_platform_reliability)**0.5 * \
                            sentiment_analysis['sentiment_score'], 2
                        )
                        risk_level = "MEDIUM"
                        if financials['roi_percentage'] > 75 and confidence_score > 0.7: risk_level = "LOW"
                        elif financials['roi_percentage'] < 30 or confidence_score < 0.4: risk_level = "HIGH"
                        
                        sim_shipping_time = self.platform_info.get(sim_source_platform_name, {}).get('shipping_time_days', 25)

                        sim_opportunity = ArbitrageOpportunity(
                            product_name=product_name_query,
                            source_platform=sim_source_platform_name,
                            source_price=financials['source_price'],
                            source_currency=financials['source_currency'],
                            target_platform=sim_target_platform_name,
                            target_price=financials['target_price'],
                            target_currency=financials['target_currency'],
                            profit=financials['net_profit'],
                            roi_percentage=financials['roi_percentage'],
                            confidence_score=confidence_score,
                            risk_level=risk_level,
                            shipping_time=sim_shipping_time,
                            category=category,
                            trend_score=round(sentiment_analysis['sentiment_score'] * 100,1),
                            viral_potential=round(random.uniform(0.1, 0.8) * sentiment_analysis['demand_impact_multiplier'],2),
                            auto_buy_recommended=(financials['roi_percentage'] > self.min_roi + 20 and confidence_score > 0.75),
                            notes="Data is SIMULATED."
                        )
                        # Get generative insight for simulated opportunity too
                        sim_opportunity.generative_insight = self.get_generative_insight(sim_opportunity)
                        all_generated_opportunities.append(sim_opportunity)
                        print(f"   💡 Oportunidade SIMULADA: {sim_opportunity.product_name} ROI: {sim_opportunity.roi_percentage:.2f}%")
                        if sim_opportunity.generative_insight:
                            print(f"      🤖 Insight da IA (Simulada): {sim_opportunity.generative_insight}")

        return all_generated_opportunities

    def generate_ai_insights(self, opportunities: List[ArbitrageOpportunity]) -> Dict:
        """
        INSIGHTS DE IA - Funcionalidade que deixa a concorrência no pó!
        Gera insights inteligentes que nenhuma outra plataforma oferece
        """
        if not opportunities:
            return {
                'summary_message': 'Nenhuma oportunidade de arbitragem processada para gerar insights.',
                'total_opportunities_processed': 0
            }
        
        total_opportunities_processed = len(opportunities)
        
        # Filter out opportunities with non-positive ROI for meaningful stats
        profitable_opportunities = [op for op in opportunities if op.roi_percentage > 0]

        if not profitable_opportunities:
            return {
                'summary_message': 'Nenhuma oportunidade lucrativa encontrada para análise detalhada.',
                'total_opportunities_processed': total_opportunities_processed,
                'real_data_opportunities': len([op for op in opportunities if op.notes == "Data primarily from live scrape."]),
                'simulated_data_opportunities': len([op for op in opportunities if op.notes == "Data is SIMULATED."])
            }

        avg_roi = sum(op.roi_percentage for op in profitable_opportunities) / len(profitable_opportunities)
        
        # Find the opportunity with the highest ROI
        # Ensure max_roi_opportunity is selected from profitable_opportunities
        max_roi_opportunity = max(profitable_opportunities, key=lambda x: x.roi_percentage)
        
        total_potential_profit = sum(op.profit for op in profitable_opportunities)
        
        category_stats = {}
        for op in profitable_opportunities:
            cat = op.category
            if cat not in category_stats:
                category_stats[cat] = {'count': 0, 'total_profit': 0, 'rois': []}
            category_stats[cat]['count'] += 1
            category_stats[cat]['total_profit'] += op.profit
            category_stats[cat]['rois'].append(op.roi_percentage)

        for cat_name, stats in category_stats.items():
            category_stats[cat_name]['avg_roi'] = sum(stats['rois']) / len(stats['rois']) if stats['rois'] else 0
            del category_stats[cat_name]['rois'] # Clean up temporary list

        auto_buy_recs = [op for op in profitable_opportunities if op.auto_buy_recommended]
        high_confidence_ops = [op for op in profitable_opportunities if op.confidence_score > 0.75] # Example threshold

        # Generate a textual recommendation
        ai_text_recommendation = self._generate_ai_text_recommendation(profitable_opportunities, category_stats, avg_roi)

        return {
            'summary_message': f"Análise completa. Processadas {total_opportunities_processed} potenciais oportunidades.",
            'total_profitable_opportunities': len(profitable_opportunities),
            'average_roi_of_profitable': round(avg_roi, 2),
            'best_opportunity_details': {
                'product': max_roi_opportunity.product_name,
                'roi': round(max_roi_opportunity.roi_percentage, 2),
                'profit': round(max_roi_opportunity.profit, 2),
                'source': max_roi_opportunity.source_platform,
                'target': max_roi_opportunity.target_platform,
                'notes': max_roi_opportunity.notes,
                'generative_insight': max_roi_opportunity.generative_insight
            },
            'total_potential_profit_from_profitable': round(total_potential_profit, 2),
            'performance_by_category': category_stats,
            'auto_buy_recommendations_count': len(auto_buy_recs),
            'high_confidence_opportunities_count': len(high_confidence_ops),
            'ai_text_recommendation': ai_text_recommendation,
            'real_data_opportunities_profitable': len([op for op in profitable_opportunities if op.notes == "Data primarily from live scrape."]),
            'simulated_data_opportunities_profitable': len([op for op in profitable_opportunities if op.notes == "Data is SIMULATED."])
        }

    def _generate_ai_text_recommendation(self, opportunities: List[ArbitrageOpportunity], category_stats: Dict, avg_roi: float) -> str:
        """Gera recomendação textual personalizada baseada em IA"""
        if not opportunities:
            return "Nenhuma oportunidade lucrativa para gerar recomendação. Tente ajustar filtros ou aguardar novo scan."

        # Find best category by average ROI or count
        best_category_name = "N/A"
        highest_avg_roi_in_cat = 0
        if category_stats:
            # Sort categories by average ROI, then by count if ROI is similar
            sorted_categories = sorted(category_stats.items(), key=lambda item: (item[1].get('avg_roi', 0), item[1].get('count',0)), reverse=True)
            if sorted_categories:
                best_category_name = sorted_categories[0][0]
                highest_avg_roi_in_cat = sorted_categories[0][1].get('avg_roi',0)

        recommendation = f"Análise de IA: {len(opportunities)} oportunidades lucrativas encontradas com ROI médio de {avg_roi:.2f}%. "

        if avg_roi > 75:
            recommendation += f"🚀 Mercado parece QUENTE! "
        elif avg_roi > 40:
            recommendation += f"💰 Boas oportunidades detectadas. "
        else:
            recommendation += f"📈 Oportunidades moderadas encontradas. "

        if best_category_name != "N/A" and highest_avg_roi_in_cat > avg_roi :
            recommendation += f"A categoria '{best_category_name}' destaca-se com um ROI médio de {highest_avg_roi_in_cat:.2f}%. Considere focar esforços aí. "
        
        auto_buy_count = len([op for op in opportunities if op.auto_buy_recommended])
        if auto_buy_count > 0:
            recommendation += f"{auto_buy_count} {'oportunidade é recomendada' if auto_buy_count == 1 else 'oportunidades são recomendadas'} para compra automática. "
        
        recommendation += "Reveja os detalhes e ajuste a sua estratégia conforme necessário."
        return recommendation

    def start_continuous_monitoring(self):
        """
        MONITORING CONTÍNUO 24/7 - Funcionalidade que NENHUMA concorrência tem!
        Sistema roda 24/7 procurando oportunidades e executando automaticamente
        """
        # This function, if called, would run indefinitely.
        # For Render free tier, long-running background tasks can be tricky.
        # Consider if this should be triggered by an external scheduler (e.g., Render Cron Job)
        # or if the app is expected to be always on.

        def _monitor_job():
            print(f"\n🤖 [{datetime.now().strftime('%H:%M:%S')}] Executando ciclo de monitoring e arbitragem...")
            opportunities = self.scan_global_opportunities() # This now uses the scraper
            
            if opportunities:
                insights = self.generate_ai_insights(opportunities)
                print(f"\n📊 INSIGHTS DE IA DO MONITORING:")
                print(f"   {insights.get('summary_message')}")
                print(f"   Oportunidades lucrativas: {insights.get('total_profitable_opportunities', 0)}")
                print(f"   Melhor ROI: {insights.get('best_opportunity_details', {}).get('roi', 0)}% para {insights.get('best_opportunity_details', {}).get('product', 'N/A')}")
                print(f"   Recomendação: {insights.get('ai_text_recommendation')}")

                # Simulate auto-execution based on new opportunities
                auto_executed_count = 0
                for opp in opportunities:
                    if opp.auto_buy_recommended:
                        if self.auto_trading_enabled: # Check global setting
                            purchase_result = self.auto_execute_purchase(opp)
                            print(f"      ↪️ Tentativa de Auto-Compra: {opp.product_name} - {purchase_result['status']}: {purchase_result['message']}")
                            if purchase_result['status'] == 'success':
                                auto_executed_count += 1
                        else:
                            print(f"      ℹ️ Auto-Compra para {opp.product_name} não executada (Auto-Trading desabilitado globalmente).")
                
                if auto_executed_count > 0:
                    print(f"\n🚀 {auto_executed_count} COMPRAS SIMULADAS EXECUTADAS AUTOMATICAMENTE NO CICLO!")
            else:
                print("   📉 Nenhuma oportunidade encontrada neste ciclo de monitoring.")
            
            # Reset daily budget at midnight (conceptual)
            # Actual reset might need to be handled more robustly depending on deployment
            if datetime.now().hour == 0 and datetime.now().minute < 5 : # Check a small window around midnight
                 if self.current_daily_spent > 0: # Only reset if it was used
                    print(f"💰 [{datetime.now().strftime('%H:%M:%S')}] ORÇAMENTO DIÁRIO RESETADO. Gasto anterior: ${self.current_daily_spent:.2f}")
                    self.current_daily_spent = 0


        print("🤖 [INFO] Sistema de Monitoring Contínuo Configurado (conceitualmente).")
        print("   -> Para execução real, agendar _monitor_job externamente ou executar em thread dedicada.")

        # Example of how it might run in a thread (commented out to prevent blocking main thread if not desired)
        # schedule.every(30).minutes.do(_monitor_job)
        # print("   -> Agendado para rodar a cada 30 minutos.")
        # while True:
        #     schedule.run_pending()
        #     time.sleep(1) # Check every second

# Main function for direct testing of the AI Brain
if __name__ == "__main__":
    print("🚀 Testando GPAS 4.0 - AI Arbitrage Brain 🚀")
    print("=" * 50)

    ai_brain_instance = AIArbitrageBrain()
    ai_brain_instance.auto_trading_enabled = True # Enable for testing auto-purchase logic
    ai_brain_instance.total_daily_budget = 200 # Smaller budget for testing

    # 1. Testar Previsões Virais (Simulado)
    print("\n🔮 Testando Previsões Virais...")
    viral_preds = ai_brain_instance.predict_viral_products()
    if viral_preds:
        print(f"   Encontradas {len(viral_preds)} previsões virais simuladas. Top 1:")
        print(f"   -> Produto: {viral_preds[0]['product']}, Score: {viral_preds[0]['viral_score']:.2f}")
    else:
        print("   Nenhuma previsão viral simulada gerada.")

    # 2. Testar Scan Global de Oportunidades (que usa o Scraper)
    print("\n🌍 Testando Scan Global de Oportunidades...")
    # This will run the scraper for products defined in ai_brain_instance.products_to_scan
    # which are by default the scraper's target_products
    opportunities_found = ai_brain_instance.scan_global_opportunities()
    print(f"   Scan concluído. {len(opportunities_found)} oportunidades potenciais geradas (reais + simuladas).")

    # 3. Testar Geração de Insights de IA
    if opportunities_found:
        print("\n💡 Testando Geração de Insights de IA...")
        insights_generated = ai_brain_instance.generate_ai_insights(opportunities_found)
        print(f"   {insights_generated.get('summary_message')}")
        best_opp = insights_generated.get('best_opportunity_details', {})
        print(f"   Melhor Oportunidade: {best_opp.get('product', 'N/A')} com ROI {best_opp.get('roi', 0):.2f}% ({best_opp.get('notes', '')})")
        print(f"   Recomendação da IA: {insights_generated.get('ai_text_recommendation')}")

        # 4. Testar Execução Automática de Compra (Simulada)
        print("\n💸 Testando Execução Automática de Compra (Simulada)...")
        if insights_generated.get('auto_buy_recommendations_count', 0) > 0:
            # Find the first auto-buy recommended opportunity
            auto_buy_opp = next((opp for opp in opportunities_found if opp.auto_buy_recommended), None)
            if auto_buy_opp:
                print(f"   Tentando auto-compra para: {auto_buy_opp.product_name} (ROI: {auto_buy_opp.roi_percentage:.2f}%)")
                purchase_status = ai_brain_instance.auto_execute_purchase(auto_buy_opp)
                print(f"   Resultado da Auto-Compra: {purchase_status['status']} - {purchase_status['message']}")
            else:
                print("   Nenhuma oportunidade específica marcada para auto-compra encontrada para teste.")
        else:
            print("   Nenhuma oportunidade recomendada para auto-compra nos insights gerados.")
    else:
        print("\n   Nenhuma oportunidade encontrada para gerar insights ou testar auto-compra.")

    print("\n" + "=" * 50)
    print("✅ Testes do AI Arbitrage Brain Concluídos.")

