"""
GPAS 4.0 - Global Product Scraper
Attempts to scrape product information from global e-commerce sites for arbitrage opportunities.
"""

import requests
from bs4 import BeautifulSoup
import time
import json
from datetime import datetime
# import pandas as pd # Not strictly necessary for core scraping logic
from typing import Dict, List, Optional
import re

class ScraperEngine:
    """Scrapes product data from global e-commerce sites."""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

        # Target global sites
        self.target_sites = {
            'aliexpress': {
                'name': 'AliExpress.com',
                'base_url': 'https://www.aliexpress.com',
                'search_url': 'https://www.aliexpress.com/wholesale?SearchText={}',
                # Selectors are highly volatile and site-specific. These are placeholders.
                'product_item_selector': 'div[data-pl]', # Generic placeholder, needs refinement
                'price_selector': 'div[class*="product-price"] span[class*="price-value"], span[class*="snow-price"]', # Placeholder
                'title_selector': 'h1[class*="product-title"], a[class*="product-title-link"]', # Placeholder
                'currency_symbol': '$', # Assuming USD for now
                'currency_code': 'USD'
            },
            'amazon': {
                'name': 'Amazon.com',
                'base_url': 'https://www.amazon.com',
                'search_url': 'https://www.amazon.com/s?k={}',
                 # Selectors for Amazon are notoriously complex due to A/B testing and dynamic content.
                'product_item_selector': 'div[data-component-type="s-search-result"]', # Placeholder
                'price_selector': 'span.a-price-whole, span.a-offscreen', # Placeholder
                'title_selector': 'span.a-size-medium.a-color-base.a-text-normal, h2.a-size-mini a.a-link-normal', # Placeholder
                'currency_symbol': '$',
                'currency_code': 'USD'
            }
        }

        # Target products for MVP testing
        self.target_products = [
            "Xiaomi Mi Band 8",
            "Anker PowerCore 10000"
        ]

    def extract_price(self, price_text: str, currency_symbol: str) -> Optional[float]:
        """Extracts price from text, handling common formats."""
        if not price_text:
            return None
        try:
            # Remove currency symbol and thousand separators, then replace comma with dot for decimal
            cleaned_price_text = price_text.replace(currency_symbol, '').replace(',', '').strip()
            # More robust regex to find numbers, including those with a single decimal point
            price_match = re.search(r'(\d+\.?\d*)', cleaned_price_text)
            if price_match:
                return float(price_match.group(1))
            return None
        except Exception as e:
            print(f"Erro ao extrair preço do texto '{price_text}': {e}")
            return None

    def extract_title(self, product_element, title_selector: str) -> Optional[str]:
        """Extracts product title from a product HTML element."""
        try:
            title_el = product_element.select_one(title_selector)
            if title_el:
                return title_el.get_text(strip=True)
            return None
        except Exception as e:
            print(f"Erro ao extrair título: {e}")
            return None

    def scrape_site_for_product(self, site_key: str, product_name_query: str) -> List[Dict]:
        """Scrapes a specific site for a product query.
        Attempts to get data from the search results page directly.
        """
        site_config = self.target_sites.get(site_key)
        if not site_config:
            print(f"Configuração não encontrada para o site: {site_key}")
            return []

        products_found = []
        try:
            search_url = site_config['search_url'].format(requests.utils.quote(product_name_query))
            print(f"🔍 Buscando '{product_name_query}' em {site_config['name']}: {search_url}")

            response = self.session.get(search_url, timeout=20) # Increased timeout
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # Find product items on the search results page
            # This is highly dependent on the site's structure and the 'product_item_selector'
            product_elements = soup.select(site_config['product_item_selector'])
            if not product_elements:
                print(f"Nenhum elemento de produto encontrado para o seletor '{site_config['product_item_selector']}' em {site_config['name']}")

            for item_el in product_elements[:3]: # Process top 3 results for MVP
                title = self.extract_title(item_el, site_config['title_selector'])

                price_el = item_el.select_one(site_config['price_selector'])
                price_text = price_el.get_text(strip=True) if price_el else None
                price = self.extract_price(price_text, site_config['currency_symbol'])

                # Basic validation: if we have a title and price, and the query is in the title
                if title and price and product_name_query.lower().split(' ')[0] in title.lower(): # Check first word of query
                    product_data = {
                        'platform': site_config['name'],
                        'title': title,
                        'price': price,
                        'url': search_url, # For now, points to search URL, not specific product
                        'timestamp': datetime.now().isoformat(),
                        'currency': site_config['currency_code']
                    }
                    products_found.append(product_data)
                    print(f"✅ Encontrado em {site_config['name']}: {title} - {site_config['currency_symbol']}{price}")
                # else:
                #     print(f"   ℹ️ Item descartado em {site_config['name']}: Título='{title}', Preço='{price}'")

                if len(products_found) >= 1: # Get first valid product for MVP for simplicity
                    break

            return products_found

        except requests.exceptions.RequestException as e:
            print(f"❌ Erro de requisição ao buscar em {site_config['name']}: {e}")
            return []
        except Exception as e:
            print(f"❌ Erro geral ao buscar em {site_config['name']} para '{product_name_query}': {e}")
            return []

    def scrape_all_sites_for_product(self, product_name: str) -> List[Dict]:
        """Scrapes all configured sites for a specific product."""
        all_results = []
        print(f"\n🚀 MONITORANDO PREÇOS GLOBAIS PARA: {product_name}")
        print("=" * 60)

        for site_key in self.target_sites.keys():
            results = self.scrape_site_for_product(site_key, product_name)
            all_results.extend(results)
            time.sleep(random.randint(3, 7)) # Random delay between sites

        return all_results

    def calculate_arbitrage_opportunity(self, products: List[Dict], target_roi_percentage: float = 20.0) -> List[Dict]:
        """Calculates arbitrage opportunities from a list of scraped products.
        Assumes all prices are in USD for MVP or converted prior.
        """
        if len(products) < 2:
            return []

        opportunities = []

        # Separate by platform for clearer buy/sell logic
        # For MVP, let's assume AliExpress is source, Amazon is target if both present
        aliexpress_products = [p for p in products if p['platform'] == 'AliExpress.com']
        amazon_products = [p for p in products if p['platform'] == 'Amazon.com']

        if not aliexpress_products or not amazon_products:
            return [] # Need products from both for this specific arbitrage path

        for source_product in aliexpress_products:
            for target_product in amazon_products:
                # Basic title similarity check (can be much more sophisticated)
                # For now, just ensure it's the same product query
                # This logic needs to be improved for real-world scenarios

                source_price = source_product['price']
                target_price = target_product['price']

                if source_price is None or target_price is None or source_price == 0:
                    continue

                # Assuming prices are comparable (e.g., both USD)
                price_diff = target_price - source_price

                if price_diff <= 0: # No profit before costs
                    continue

                # Simplified cost calculation for MVP
                # These are rough estimates and vary wildly
                shipping_from_source = source_price * 0.10  # Estimate 10% for shipping from AliExpress
                amazon_fees_percentage = 0.15  # Amazon referral fee

                amazon_fees = target_price * amazon_fees_percentage
                estimated_total_costs = source_price + shipping_from_source + amazon_fees

                net_profit = target_price - estimated_total_costs

                if net_profit <= 0:
                    continue

                roi_on_investment = (net_profit / source_price) * 100 # ROI on initial product cost

                if roi_on_investment >= target_roi_percentage:
                    opportunities.append({
                        'buy_from_platform': source_product['platform'],
                        'buy_from_title': source_product['title'],
                        'buy_price': source_price,
                        'buy_url': source_product['url'],
                        'sell_on_platform': target_product['platform'],
                        'sell_on_title': target_product['title'],
                        'sell_price': target_price,
                        'sell_url': target_product['url'],
                        'estimated_net_profit': round(net_profit, 2),
                        'estimated_roi_percentage': round(roi_on_investment, 2),
                        'product_name_query': source_product.get('title', 'N/A'), # Or a common identifier
                        'timestamp': datetime.now().isoformat()
                    })

        return sorted(opportunities, key=lambda x: x['estimated_roi_percentage'], reverse=True)

    def run_scraping_cycle(self) -> Dict:
        """Executes a full scraping and arbitrage calculation cycle."""
        print("\n🔥 INICIANDO CICLO DE SCRAPING GLOBAL")
        print("🎯 Objetivo: Encontrar oportunidades de arbitragem globais (Prova de Conceito)")
        print("💰 ROI mínimo alvo: 20%")
        print("=" * 80)

        all_found_opportunities = []
        scraping_summary = {
            'timestamp': datetime.now().isoformat(),
            'products_scraped_details': [],
            'total_opportunities_found': 0,
            'best_opportunity_roi': 0.0
        }

        for product_query in self.target_products:
            print(f"\n📱 PRODUTO ALVO: {product_query}")

            # Scrape all configured sites for this product
            scraped_product_versions = self.scrape_all_sites_for_product(product_query)

            current_product_summary = {
                'product_query': product_query,
                'versions_found': len(scraped_product_versions),
                'opportunities_for_this_product': 0
            }

            if scraped_product_versions:
                # Calculate arbitrage opportunities
                opportunities = self.calculate_arbitrage_opportunity(scraped_product_versions)
                current_product_summary['opportunities_for_this_product'] = len(opportunities)

                if opportunities:
                    print(f"\n💰 OPORTUNIDADES ENCONTRADAS PARA {product_query}:")
                    for opp in opportunities:
                        print(f"  🛒 Comprar: {opp['buy_from_platform']} ({opp['buy_from_title']}) - ${opp['buy_price']:.2f}")
                        print(f"  💸 Vender: {opp['sell_on_platform']} ({opp['sell_on_title']}) - ${opp['sell_price']:.2f}")
                        print(f"  💵 Lucro Líquido Estimado: ${opp['estimated_net_profit']:.2f}")
                        print(f"  📈 ROI Estimado: {opp['estimated_roi_percentage']:.1f}%")
                        print(f"  🔗 URL Compra: {opp['buy_url']}")
                        print("  " + "-" * 50)

                    all_found_opportunities.extend(opportunities)

                    best_opp_roi = max(opp['estimated_roi_percentage'] for opp in opportunities)
                    if best_opp_roi > scraping_summary['best_opportunity_roi']:
                        scraping_summary['best_opportunity_roi'] = best_opp_roi
                else:
                    print(f"  ❌ Nenhuma oportunidade de arbitragem rentável encontrada para {product_query} com os dados atuais.")
            else:
                print(f"  ❌ {product_query} não encontrado em plataformas suficientes para análise.")

            scraping_summary['products_scraped_details'].append(current_product_summary)
            print("\n" + "=" * 60)
            time.sleep(random.randint(5, 10)) # Longer pause between different products

        scraping_summary['total_opportunities_found'] = len(all_found_opportunities)

        # Final summary
        print(f"\n🎯 RESUMO DO CICLO DE SCRAPING GLOBAL:")
        for detail in scraping_summary['products_scraped_details']:
            print(f"  📊 Produto: {detail['product_query']} - Versões Encontradas: {detail['versions_found']}, Oportunidades: {detail['opportunities_for_this_product']}")
        print(f"💰 Total de Oportunidades Encontradas: {scraping_summary['total_opportunities_found']}")
        print(f"🚀 Melhor ROI de Oportunidade: {scraping_summary['best_opportunity_roi']:.1f}%")

        # if all_found_opportunities:
        #     total_potential_profit = sum([opp['estimated_net_profit'] for opp in all_found_opportunities])
        #     print(f"💵 Lucro potencial total estimado (das encontradas): ${total_potential_profit:.2f}")

        return {'summary': scraping_summary, 'opportunities': all_found_opportunities}

# For testing the scraper directly
if __name__ == "__main__":
    import random # ensure random is imported if running directly
    engine = ScraperEngine()
    results = engine.run_scraping_cycle()
    # print("\nFull Results (JSON):")
    # print(json.dumps(results, indent=2))
